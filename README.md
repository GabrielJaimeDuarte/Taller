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


### 3. `Taller_Punto_3.py` – Resolución y Visualización de Laberintos

- Representa un laberinto como matriz de 0 y 1 (0 = camino, 1 = obstáculo).
- Invierte la matriz para adecuarla al algoritmo de BFS.
- Ejecuta BFS para encontrar un camino desde `(12, 0)` hasta `(0, 29)`.
- Visualiza:
  - Laberinto original.
  - Laberinto invertido.
  - Camino encontrado sobre el laberinto invertido, usando Matplotlib.

