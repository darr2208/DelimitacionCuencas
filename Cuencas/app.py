import streamlit as st
from utils.calculos import calcular_parametros
from utils.exportar_excel import exportar_a_excel
from utils.generar_shapefile import generar_shapefile_desde_bbox
from utils.mapa import generar_mapa_cuenca
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Delimitación de Cuencas", page_icon="🌎")

with open("assets/estilo.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

col1, col2, _ = st.columns([1, 1, 6])
with col1:
    st.image("data/logo1.png", use_container_width=True)
with col2:
    st.image("data/logo2.png", use_container_width=True)

st.markdown("<h1 style='text-align: center; color: #114B5F;'>Simulación de Delimitación de Cuencas Hidrográficas</h1>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.header("Coordenadas del Punto Central")
lat = st.sidebar.number_input("Latitud", value=4.65, format="%.6f")
lon = st.sidebar.number_input("Longitud", value=-74.05, format="%.6f")

if st.sidebar.button("Simular Delimitación"):
    buffer = 0.02
    minx, miny = lon - buffer, lat - buffer
    maxx, maxy = lon + buffer, lat + buffer

    df_parametros, df_alturas = calcular_parametros(minx, miny, maxx, maxy)
    ruta_excel = exportar_a_excel(df_parametros, df_alturas)
    ruta_shapefile = generar_shapefile_desde_bbox(minx, miny, maxx, maxy)

    geojson_data = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [minx, miny], [maxx, miny], [maxx, maxy], [minx, maxy], [minx, miny]
                ]]
            }
        }]
    }

    mapa = generar_mapa_cuenca(lat, lon, geojson_data)
    st.markdown("### Mapa de la Cuenca")
    components.html(mapa._repr_html_(), height=500)

    st.markdown("### Parámetros Morfométricos Calculados")
    st.dataframe(df_parametros, use_container_width=True)

    st.markdown("### Clases Altitudinales")
    st.dataframe(df_alturas, use_container_width=True)

    st.markdown("### Archivos Exportables")
    st.download_button("📥 Descargar Excel", data=open(ruta_excel, "rb").read(), file_name="parametros.xlsx")
    st.download_button("📥 Descargar Shapefile ZIP", data=open(ruta_shapefile, "rb").read(), file_name="cuenca.zip")
else:
    st.info("Ingresa las coordenadas y presiona 'Simular Delimitación' para iniciar.")

