import streamlit as st
import os
from PIL import Image
from utils.calculos import calcular_parametros
from utils.exportar_excel import exportar_a_excel
from utils.generar_shapefile import generar_shapefile_desde_bbox
from utils.mapa import generar_mapa_y_cuenca

st.set_page_config(page_title="Delimitador de Cuencas", layout="wide")

if os.path.exists("assets/estilo.css"):
    with open("assets/estilo.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
logo1_path = "data/logo1.png"
logo2_path = "data/logo2.png"

with col1:
    if os.path.exists(logo1_path):
        st.image(Image.open(logo1_path), use_column_width=True)

with col2:
    if os.path.exists(logo2_path):
        st.image(Image.open(logo2_path), use_column_width=True)

st.title("Simulador de Parámetros Morfométricos de Cuencas")

lat = st.number_input("Latitud (Centro)", value=9.761395, format="%.6f")
lon = st.number_input("Longitud (Centro)", value=-75.056792, format="%.6f")
buffer = st.slider("Tamaño del área (km)", min_value=0.5, max_value=5.0, value=2.0, step=0.1)
nombre_archivo = st.text_input("Nombre del archivo exportado", value="cuenca")

if st.button("Generar Parámetros"):
    delta = buffer / 111
    minx = lon - delta
    maxx = lon + delta
    miny = lat - delta
    maxy = lat + delta

    df_param, df_alturas = calcular_parametros(minx, miny, maxx, maxy)

    st.success("Parámetros calculados correctamente.")

    st.subheader("Resultados Generales")
    st.dataframe(df_param, use_container_width=True)

    st.subheader("Clases Altitudinales")
    st.dataframe(df_alturas, use_container_width=True)

    ruta_excel = exportar_a_excel(df_param, df_alturas, nombre_archivo + ".xlsx")
    ruta_zip = generar_shapefile_desde_bbox(minx, miny, maxx, maxy, nombre_archivo)

    with open(ruta_excel, "rb") as f:
        st.download_button("📄 Descargar parámetros (Excel)", data=f, file_name=nombre_archivo + ".xlsx")

    with open(ruta_zip, "rb") as f:
        st.download_button("🗂️ Descargar cuenca (Shapefile .zip)", data=f, file_name=nombre_archivo + ".zip")

    st.subheader("Visualización de la Cuenca")
    generar_mapa_y_cuenca(lat, lon, buffer_km=buffer)
