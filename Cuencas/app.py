import streamlit as st
from utils.calculos import calcular_parametros
from utils.exportar_excel import exportar_a_excel
from utils.generar_shapefile import generar_shapefile_desde_bbox
from utils.mapa import generar_mapa_cuenca
from streamlit_folium import st_folium
import os

st.set_page_config(page_title="Delimitador de Cuencas", layout="wide")

st.markdown("<link rel='stylesheet' href='assets/estilo.css'>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.image("data/logo_1.png", use_container_width=True)
with col2:
    st.image("data/logo_2.png", use_container_width=True)

st.title("Simulador de Delimitación de Cuencas Hidrográficas")

lat = st.number_input("Latitud", value=4.60971, format="%.6f")
lon = st.number_input("Longitud", value=-74.08175, format="%.6f")

if st.button("Simular delimitación"):
    buffer = 0.015
    minx, miny = lon - buffer, lat - buffer
    maxx, maxy = lon + buffer, lat + buffer

    df_param, df_alturas = calcular_parametros(minx, miny, maxx, maxy)
    excel_path = exportar_a_excel(df_param, df_alturas)
    shp_path = generar_shapefile_desde_bbox(minx, miny, maxx, maxy)

    st.subheader("Visualización de la Cuenca")
    mapa = generar_mapa_cuenca(lat, lon)
    st_folium(mapa, width=1000, height=500)

    st.subheader("Parámetros Calculados")
    st.dataframe(df_param, use_container_width=True)

    st.subheader("Clases Altitudinales")
    st.dataframe(df_alturas, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        with open(excel_path, "rb") as f:
            st.download_button("📥 Descargar Excel", f, file_name="parametros.xlsx")
    with col2:
        with open(shp_path, "rb") as f:
            st.download_button("📥 Descargar Shapefile (.zip)", f, file_name="cuenca.zip")

