# etl_polars.py
import polars as pl
import pandas as pd

def _excel_to_polars(path: str, sheet: str | None = None) -> pl.DataFrame:
    """
    Lee Excel a Polars. Si no se da 'sheet', concatena todas las hojas
    y añade '__sheet__' para saber de dónde viene cada fila.
    """
    if sheet is None:
        xls = pd.ExcelFile(path)
        frames = []
        for sh in xls.sheet_names:
            df = pd.read_excel(path, sheet_name=sh, header=0)
            df["__sheet__"] = sh
            frames.append(pl.from_pandas(df))
        return pl.concat(frames, how="vertical_relaxed")
    else:
        df = pd.read_excel(path, sheet_name=sheet, header=0)
        df["__sheet__"] = sheet
        return pl.from_pandas(df)

def _unit_str_to_float_expr(col: str) -> pl.Expr:
    """
    Convierte strings con unidades (p. ej., '0.55 V' o '1,23 mV') a float.
    - Extrae el número con punto o coma.
    - Reemplaza coma decimal por punto.
    """
    return (
        pl.col(col)
        .cast(pl.Utf8, strict=False)
        .str.extract(r"([-+]?\d+(?:[.,]\d+)?)", group_index=1)  # 12 / 12.3 / 12,3
        .str.replace(",", ".")
        .cast(pl.Float64, strict=False)
    )

def _coerce_numeric_columns(df: pl.DataFrame, skip_cols=("__sheet__", "Usuario")) -> pl.DataFrame:
    """
    Polars 1.7.1: sin is_numeric. Convertimos SOLO columnas de tipo texto (Utf8)
    que típicamente traen valores con unidades ('0.55 V') a float.
    """
    out = df
    for c, t in zip(out.columns, out.dtypes):
        if c in skip_cols:
            continue
        if t == pl.Utf8:  # solo intentamos parsear texto
            out = out.with_columns(_unit_str_to_float_expr(c).alias(c))
    return out

def melt_wide(df: pl.DataFrame, id_cols=("__sheet__", "Usuario")) -> pl.DataFrame:
    """
    Pasa de ancho a largo:
      - 'muestra' = índice de fila (0,1,2,...)
      - 'canal'   = nombre de la columna (1..60)
      - 'valor'   = lectura numérica
    Mantiene '__sheet__' (y 'Usuario' si existe).
    """
    ids = [c for c in id_cols if c in df.columns]
    df = df.with_row_count("muestra")
    value_cols = [c for c in df.columns if c not in ids + ["muestra"]]
    long = df.melt(
        id_vars=["muestra"] + ids,
        value_vars=value_cols,
        variable_name="canal",
        value_name="valor",
    ).with_columns(pl.col("canal").cast(pl.Utf8))
    return long

def clean_long(long: pl.DataFrame, z: float = 3.0, smooth: int = 5) -> pl.DataFrame:
    """
    Limpieza y features por grupo (__sheet__, canal):
    - Quita nulos.
    - Filtra outliers por |z| <= z (z-score por grupo).
    - Aplica suavizado rolling centrado (media móvil).
    - Normaliza min–max por grupo.
    """
    out = long.drop_nulls(subset=["valor"])

    # z-score por grupo
    out = out.with_columns(
        (
            (pl.col("valor") - pl.col("valor").mean().over(["__sheet__", "canal"])) /
            pl.col("valor").std().over(["__sheet__", "canal"])
        ).alias("z")
    )
    out = out.filter((pl.col("z").abs() <= z) | pl.col("z").is_null()).drop("z")

    # suavizado rolling por grupo
    out = out.sort(["__sheet__", "canal", "muestra"]).with_columns(
        pl.col("valor").rolling_mean(window_size=smooth, center=True)
        .over(["__sheet__", "canal"])
        .alias("valor_sm")
    )

    # min–max por grupo
    out = out.with_columns(
        (
            (pl.col("valor") - pl.min("valor").over(["__sheet__", "canal"])) /
            (pl.max("valor").over(["__sheet__", "canal"]) - pl.min("valor").over(["__sheet__", "canal"]))
        ).alias("valor_mm")
    )
    return out

def run_etl_excel(
    path: str,
    sheet: str | None = None,
    z_thresh: float = 3.0,
    smooth_window: int = 5,
    fs: float = 1.0,
) -> pl.DataFrame:
    """
    Pipeline completo:
      1) Leer Excel (una hoja o todas)
      2) Parsear unidades -> float (para columnas de texto)
      3) Ancho -> largo
      4) Limpieza + outliers + suavizado + min–max
      5) t_s = muestra / fs
    """
    df = _excel_to_polars(path, sheet=sheet)
    df = _coerce_numeric_columns(df)
    long = melt_wide(df, id_cols=("__sheet__", "Usuario"))
    long = clean_long(long, z=z_thresh, smooth=smooth_window)
    long = long.with_columns((pl.col("muestra").cast(pl.Float64) / fs).alias("t_s"))
    return long

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="ETL para BD_SENSORES.xlsx (Excel -> largo, limpieza y features)")
    ap.add_argument("--path", type=str, default="data/BD_SENSORES.xlsx", help="Ruta al Excel")
    ap.add_argument("--sheet", type=str, default=None, help="Nombre de hoja (vacío = todas)")
    ap.add_argument("--z", type=float, default=3.0, help="Umbral z-score para outliers")
    ap.add_argument("--win", type=int, default=5, help="Ventana de suavizado (rolling)")
    ap.add_argument("--fs", type=float, default=1.0, help="Frecuencia de muestreo (Hz) para t_s")
    ap.add_argument("--out", type=str, default="data/etl_output.parquet", help="Salida Parquet")
    args = ap.parse_args()

    out_df = run_etl_excel(
        args.path,
        sheet=(args.sheet or None),
        z_thresh=args.z,
        smooth_window=args.win,
        fs=args.fs,
    )
    out_df.write_parquet(args.out)
    print(f"[OK] Guardado: {args.out}")
