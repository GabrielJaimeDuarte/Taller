# Taller – Búsquedas, Laberintos y ETL con Visualización Interactiva

Este repositorio contiene tres componentes fundamentales del taller académico, combinando algoritmos de búsqueda, resolución de laberintos y un pipeline ETL con visualización interactiva:

1. **Taller_Punto_1.py** – Búsqueda en grafos (BFS, DFS, UCS) con visualización paso a paso.  
2. **Punto2_Taller/** – ETL con Polars + visualización con hvPlot y Plotly + dashboard interactivo con Streamlit.  
3. **Taller_Punto_3.py** – Resolución visual de laberintos mediante BFS y Matplotlib.

---

##  Resumen por Punto

### 1. `Taller_Punto_1.py` – Búsqueda y Visualización en Grafos

- Construye un árbol dirigido con costos (`tree_with_costs`) y su versión no ponderada (`tree`).
- Implementa y visualiza tres algoritmos clásicos de búsqueda:
  - **BFS**: garantiza el camino más corto en pasos.
  - **DFS**: explora en profundidad, sin garantizar camino más corto.
  - **UCS (Uniform Cost Search)**: encuentra el camino de menor costo considerando los pesos en aristas.
- Utiliza **NetworkX** para modelar grafos ([NetworkX](https://en.wikipedia.org/wiki/NetworkX) :contentReference[oaicite:0]{index=0}) y **Matplotlib** para visualizar en tiempo real cada paso: nodos visitados, frontera, nodo actual y camino hacia el objetivo.
- Al finalizar, imprime en la consola una comparación clara de eficiencia, caminos y costos de los tres algoritmos.

# Punto 2 — ETL + Visualización + Dashboard (Taller)

Este proyecto resuelve el **Punto 2** del taller: implementar un **ETL** con **Polars**, realizar **gráficas** con **hvPlot** y **Plotly**, y desplegar un **dashboard en Streamlit** para analizar la base real `BD_SENSORES.xlsx`.

---

## 🔎 ¿Qué se hizo y por qué?

- **Extracción (E):** Se cargó `BD_SENSORES.xlsx` y se etiquetó cada fila con `__sheet__` (nombre de hoja) para saber su origen.
- **Transformación (T):**
  - Se convirtieron valores de texto con unidades (p. ej. `"0.55 V"`) a **float** para poder analizarlos.
  - Se cambió de **formato ancho → largo**: ahora hay una columna **`canal`** (la columna original 1..60) y **`valor`** (la lectura).
  - **Limpieza de calidad:** se eliminaron **nulos** y **outliers** por **z-score** (por hoja/canal) para mejorar la señal.
  - **Suavizado**: se creó **`valor_sm`** con media móvil centrada (reduce ruido).
  - **Normalización**: se creó **`valor_mm`** en rango **0–1** (facilita comparar canales de distinta magnitud).
  - **Tiempo sintético**: **`t_s`** = `muestra / fs` (si no se conoce la frecuencia, `fs=1.0` por defecto).
- **Carga (L) + Visualización:** Se guardan resultados en **CSV/Parquet** y se visualizan en un **dashboard Streamlit** interactivo para explorar hojas, canales y métricas.

Este flujo deja los datos **limpios, comparables y visualizables**, cumpliendo el objetivo del punto.

---

## 🗂️ Estructura del proyecto
Punto2_Taller/
├─ app.py
├─ etl_polars.py
├─ requirements.txt
└─ data/
└─ BD_SENSORES.xlsx


---

## ⚙️ Requisitos

- Python 3.10+  
- Dependencias (se instalan con `requirements.txt`):
  - polars, pandas, plotly, hvplot, bokeh, streamlit, openpyxl

Instala con:
```bash
pip install -r requirements.txt


▶️ Cómo ejecutar
1) ETL por consola (opcional)

Ejecuta el pipeline y guarda un Parquet con todo procesado:
python etl_polars.py --path "data/BD_SENSORES.xlsx" --out "data/etl_output.parquet"

Opciones útiles:

# Procesar una hoja específica (ej. SENP1), z-score y ventana:
python etl_polars.py --path "data/BD_SENSORES.xlsx" --sheet "SENP1" --z 3.0 --win 5 --fs 1.0 --out "data/etl_output.parquet"

2) Dashboard

Lanza la interfaz web:
python -m streamlit run app.py


🖥️ ¿Qué se ve en el Dashboard?

Panel lateral (configuración):

Ruta Excel: data/BD_SENSORES.xlsx

Hoja: vacía = todas, o el nombre (p. ej. SENP1, EMG, etc.)

Umbral z-score (outliers): filtra lecturas atípicas por hoja/canal.

Ventana de suavizado: tamaño de la media móvil centrada (reduce ruido).

Frecuencia de muestreo (fs): calcula t_s = muestra / fs (en segundos).

Biblioteca de gráficas: Plotly (con botón a PNG) o hvPlot.

Vista de datos transformados (tabla):

Columnas principales: muestra, __sheet__, Usuario (si existe), canal, valor, valor_sm, valor_mm, t_s.

Controles de análisis:

Hoja a analizar.

Canales (uno o varios) para comparar.

Métrica (Y):

valor → señal limpia (sin nulos/outliers).

valor_sm → señal suavizada (menos ruido).

valor_mm → señal normalizada (0–1) para comparar escalas.

Gráfica interactiva:

Zoom, panning, hover y (en Plotly) exportar PNG.

Descargas:

Exportar Parquet/CSV con los datos ya transformados.

✅ ¿Qué se logró?

Un pipeline ETL robusto con Polars: limpia nulos, filtra outliers, suaviza y normaliza por hoja/canal, además de añadir tiempo t_s.

Un dashboard interactivo en Streamlit para:

Explorar hojas y canales con distintas métricas (crudo, suavizado, normalizado).

Ajustar parámetros de pre/procesamiento sin tocar código.

Exportar datos listos para informes o análisis posteriores.

Entrega reproducible y clara que cumple el Punto 2: ETL con Polars + hvPlot/Plotly + Streamlit.

🔧 Parámetros (explicados rápido)

z-score (outliers): umbral típico 3.0. Baja a 2.5 si ves picos indeseados; sube a 3.5–4 si elimina demasiado.

Ventana (suavizado): 5–11 suelen funcionar bien. Mayor = más suave; menor = más detalle.

fs (Hz): si conoces la frecuencia real de muestreo, úsala para que t_s esté en segundos reales.

🧩 Notas técnicas

En Polars 1.7.1 se evitó is_numeric; se parsean columnas Utf8 con unidades a float.

Polars advierte deprecations:

with_row_count → se podría migrar a with_row_index.

melt → se podría migrar a unpivot.

No afecta el resultado actual; es una mejora futura.

🆘 Solución de problemas (FAQ)

No veo la gráfica / sale vacía:
Verifica que elegiste una Hoja real y al menos un Canal.

No abre Streamlit al ejecutar:
Usa python -m streamlit run app.py (evita problemas de PATH).

Quiero más suavizado pero sin perder forma:
Sube la ventana poco a poco (5 → 7 → 11).

Necesito comparar formas ignorando amplitud:
Usa valor_mm (normalizado 0–1) y superpone varios canalé


🧪 Comandos rápidos
# Instalar dependencias
pip install -r requirements.txt

# ETL (todas las hojas)
python etl_polars.py --path "data/BD_SENSORES.xlsx" --out "data/etl_output.parquet"

# ETL (una hoja específica)
python etl_polars.py --path "data/BD_SENSORES.xlsx" --sheet "SENP1" --z 3.0 --win 5 --fs 1.0 --out "data/etl_output.parquet"

# Dashboard interactivo
python -m streamlit run app.py
### 3. `Taller_Punto_3.py` – Resolución y Visualización de Laberintos

- Representa un laberinto como matriz de 0 y 1 (0 = camino, 1 = obstáculo).
- Invierte la matriz para adecuarla al algoritmo de BFS.
- Ejecuta BFS para encontrar un camino desde `(12, 0)` hasta `(0, 29)`.
- Visualiza:
  - Laberinto original.
  - Laberinto invertido.
  - Camino encontrado sobre el laberinto invertido, usando Matplotlib.

