import streamlit as st
from utils.calculos import calcular_parametros
from utils.exportar_excel import exportar_a_excel
from utils.generar_shapefile import generar_shapefile_desde_bbox
from utils.mapa import generar_mapa_cuenca
from streamlit_folium import st_folium
from PIL import Image

st.set_page_config(page_title="Delimitación de Cuencas", layout="wide")
st.markdown('<link rel="stylesheet" href="assets/estilo.css">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.image("data/logo_1.png", use_column_width=True)
with col2:
    st.markdown("<h1 style='text-align: center;'>Simulador de Parámetros Morfométricos</h1>", unsafe_allow_html=True)
with col3:
    st.image("data/logo_2.png", use_column_width=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### Selecciona una ubicación para simular la delimitación de la cuenca:")

lat = st.number_input("Latitud (ej. 5.07)", value=5.07, format="%.6f")
lon = st.number_input("Longitud (ej. -75.52)", value=-75.52, format="%.6f")

if st.button("Simular delimitación"):
    buffer = 0.015
    minx = lon - buffer
    maxx = lon + buffer
    miny = lat - buffer
    maxy = lat + buffer

    df_parametros, df_alturas = calcular_parametros(minx, miny, maxx, maxy)
    excel_path = exportar_a_excel(df_parametros, df_alturas)
    zip_path = generar_shapefile_desde_bbox(minx, miny, maxx, maxy)
    mapa = generar_mapa_cuenca(lat, lon)

    st.markdown("### Mapa de la Cuenca Simulada")
    st_folium(mapa, width=1200, height=600)

    st.markdown("### Parámetros Morfométricos")
    st.dataframe(df_parametros, use_container_width=True)

    st.markdown("### Clases Altitudinales")
    st.dataframe(df_alturas, use_container_width=True)

    col_desc1, col_desc2 = st.columns(2)
    with col_desc1:
        with open(excel_path, "rb") as f:
            st.download_button("📊 Descargar Excel", f, file_name="parametros.xlsx")
    with col_desc2:
        with open(zip_path, "rb") as f:
            st.download_button("📁 Descargar Shapefile (ZIP)", f, file_name="cuenca.zip")
