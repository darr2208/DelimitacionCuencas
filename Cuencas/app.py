import streamlit as st
import os
import base64
from utils.calculos import calcular_parametros
from utils.exportar_excel import exportar_a_excel
from utils.generar_shapefile import generar_shapefile_desde_bbox
from utils.mapa import generar_mapa_cuenca

st.set_page_config(layout="wide", page_title="Delimitador de Cuencas", page_icon="🌎")
with open("assets/estilo.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.image("data/logo_institucional.png", use_column_width=False)
with col2:
    st.image("data/logo2.png", use_column_width=False)

st.title("Delimitador de Cuencas Hidrográficas")
st.markdown("Simulación de delimitación y cálculo de parámetros morfométricos")

with st.form("formulario"):
    st.subheader("Ingrese coordenadas")
    minx = st.number_input("Longitud mínima (minx)", value=-74.1, format="%.6f")
    maxx = st.number_input("Longitud máxima (maxx)", value=-73.9, format="%.6f")
    miny = st.number_input("Latitud mínima (miny)", value=4.6, format="%.6f")
    maxy = st.number_input("Latitud máxima (maxy)", value=4.8, format="%.6f")
    submit = st.form_submit_button("Simular delimitación y calcular")

if submit:
    df_param, df_alturas = calcular_parametros(minx, miny, maxx, maxy)
    archivo_excel = exportar_a_excel(df_param, df_alturas)
    archivo_shp = generar_shapefile_desde_bbox(minx, miny, maxx, maxy)

    st.success("Cálculos realizados con éxito.")
    st.subheader("Mapa de la cuenca")
    mapa = generar_mapa_cuenca((miny + maxy) / 2, (minx + maxx) / 2)
    st.components.v1.html(mapa._repr_html_(), height=500)

    st.subheader("Tabla de parámetros calculados")
    st.dataframe(df_param, use_container_width=True)
    st.subheader("Tabla de clases altitudinales")
    st.dataframe(df_alturas, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        with open(archivo_excel, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="parametros.xlsx">📥 Descargar Excel</a>'
            st.markdown(href, unsafe_allow_html=True)

    with col4:
        with open(archivo_shp, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/zip;base64,{b64}" download="cuenca.zip">📥 Descargar Shapefile</a>'
            st.markdown(href, unsafe_allow_html=True)
