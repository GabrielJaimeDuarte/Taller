# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 18:40:32 2025

@author: camic
"""

# app.py
import polars as pl
import streamlit as st
import plotly.express as px
import pandas as pd
import hvplot.pandas  # habilita .hvplot en DataFrames de pandas

from etl_polars import run_etl_excel

st.set_page_config(page_title="Dashboard Sensores (Excel)", layout="wide")
st.title("Dashboard | BD_SENSORES.xlsx — ETL + Visualización")
st.caption("ETL con Polars, gráficas con Plotly/hvPlot y tablero en Streamlit.")

# --- Barra lateral ---
st.sidebar.header("Parámetros")
data_path = st.sidebar.text_input("Ruta Excel", "data/BD_SENSORES.xlsx")
sheet = st.sidebar.text_input("Hoja (vacío = todas)", "")
z = st.sidebar.slider("Umbral z-score (outliers)", 1.0, 6.0, 3.0, 0.5)
win = st.sidebar.slider("Ventana de suavizado (rolling)", 3, 101, 5, 2)
fs = st.sidebar.number_input("Frecuencia de muestreo (Hz)", min_value=0.01, max_value=10000.0, value=1.0, step=0.01)
lib = st.sidebar.selectbox("Biblioteca de gráficos", ["Plotly", "hvPlot"])

@st.cache_data(show_spinner=False)
def load_df(path, sheet, z, win, fs):
    sh = sheet if sheet.strip() else None
    df = run_etl_excel(path, sheet=sh, z_thresh=z, smooth_window=win, fs=fs)
    return df

# --- Cargar y transformar ---
try:
    df_pl = load_df(data_path, sheet, z, win, fs)
except Exception as e:
    st.error(f"Error al cargar/transformar datos: {e}")
    st.stop()

st.subheader("Datos transformados (muestra)")
st.dataframe(df_pl.head(200).to_pandas())

# --- Selecciones para graficar ---
sheets = sorted(df_pl["__sheet__"].unique().to_list())
if not sheets:
    st.warning("No se encontraron hojas procesadas. Revisa ruta/hoja.")
    st.stop()

sel_sheet = st.selectbox("Hoja", sheets, index=0)
df_sh = df_pl.filter(pl.col("__sheet__") == sel_sheet)

canales = sorted(df_sh["canal"].unique().to_list())
sel_canales = st.multiselect("Canales", canales, default=canales[:3])
metric = st.selectbox("Métrica (eje Y)", ["valor", "valor_sm", "valor_mm"])

st.markdown("---")

# --- Gráficas ---
if not sel_canales:
    st.info("Selecciona al menos un canal.")
else:
    df_plot = df_sh.filter(pl.col("canal").is_in(sel_canales))[["t_s", "canal", metric]].to_pandas()
    if lib == "Plotly":
        fig = px.line(df_plot, x="t_s", y=metric, color="canal", title=f"{metric} vs t_s — Hoja {sel_sheet}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        hv = df_plot.hvplot.line(x="t_s", y=metric, by="canal", title=f"{metric} vs t_s — Hoja {sel_sheet}")
        st.bokeh_chart(hv, use_container_width=True)

st.markdown("---")
st.subheader("Descargas")
c1, c2 = st.columns(2)
with c1:
    if st.button("Exportar Parquet"):
        out = "data/etl_output.parquet"
        df_pl.write_parquet(out)
        st.success(f"Guardado {out}")
with c2:
    if st.button("Exportar CSV"):
        out = "data/etl_output.csv"
        df_pl.write_csv(out)
        st.success(f"Guardado {out}")
