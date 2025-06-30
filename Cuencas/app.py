import streamlit as st
import os
import base64
import pandas as pd
from utils.calculos_aproximados import calcular_parametros
from utils.exportar_excel import exportar_parametros_excel
from utils.generar_shapefile import generar_shapefile
from utils.mapa import mostrar_mapa

with open("assets/estilo.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def mostrar_logos():
    def codificar_logo(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    logo_izq = os.path.join("data", "lLOGO 1.png")
    logo_der = os.path.join("data", "LOGO 2.png")

    if os.path.exists(logo_izq):
        st.markdown(f'<img src="data:image/png;base64,{codificar_logo(logo_izq)}" class="logo-izq">', unsafe_allow_html=True)
    if os.path.exists(logo_der):
        st.markdown(f'<img src="data:image/png;base64,{codificar_logo(logo_der)}" class="logo-der">', unsafe_allow_html=True)

mostrar_logos()

st.markdown('<div class="titulo-principal">Simulación de Delimitación de Cuencas</div>', unsafe_allow_html=True)

punto = mostrar_mapa()

if punto:
    st.success("Punto seleccionado correctamente. Iniciando simulación...")
    tabla_parametros, poligono = calcular_parametros(punto)

    st.markdown('<div class="tabla-resultados">', unsafe_allow_html=True)
    st.dataframe(tabla_parametros, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    ruta_excel = os.path.join("data", "outputs", "parametros.xlsx")
    exportar_parametros_excel(tabla_parametros, ruta_excel)

    ruta_shp = os.path.join("data", "outputs", "cuenca.zip")
    generar_shapefile(poligono, ruta_shp)

    with open(ruta_excel, "rb") as f:
        b64_excel = base64.b64encode(f.read()).decode()
        href_excel = f'<a href="data:application/octet-stream;base64,{b64_excel}" download="parametros.xlsx">📥 Descargar Excel</a>'
        st.markdown(href_excel, unsafe_allow_html=True)

    with open(ruta_shp, "rb") as f:
        b64_shp = base64.b64encode(f.read()).decode()
        href_shp = f'<a href="data:application/zip;base64,{b64_shp}" download="cuenca.zip">📥 Descargar Shapefile</a>'
        st.markdown(href_shp, unsafe_allow_html=True)
else:
    st.info("Selecciona un punto sobre el mapa para iniciar.")
