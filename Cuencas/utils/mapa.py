import folium
from folium import Polygon, Marker, FeatureGroup
import math

def generar_mapa_cuenca(lat, lon, radio_km=2.0):
    m = folium.Map(
        location=[lat, lon],
        zoom_start=13,
        control_scale=True,
        tiles=None
    )

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='ESRI',
        name='Satélite'
    ).add_to(m)

    folium.TileLayer(
        tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attr='OpenTopoMap',
        name='Topografía'
    ).add_to(m)

    delta = radio_km / 111

    coords = [
        [lat + delta * 0.9, lon],
        [lat + delta * 0.5, lon + delta * 0.6],
        [lat + delta * 0.1, lon + delta * 1.1],
        [lat - delta * 0.3, lon + delta * 0.8],
        [lat - delta * 0.8, lon + delta * 0.3],
        [lat - delta * 0.9, lon],
        [lat - delta * 0.5, lon - delta * 0.6],
        [lat - delta * 0.1, lon - delta * 1.1],
        [lat + delta * 0.3, lon - delta * 0.8],
        [lat + delta * 0.8, lon - delta * 0.3],
        [lat + delta * 0.9, lon]
    ]

    grupo = FeatureGroup(name='Cuenca simulada')

    Polygon(
        locations=coords,
        color="#006400",
        weight=3,
        fill=True,
        fill_color="#00cc66",
        fill_opacity=0.5,
        tooltip="Cuenca simulada"
    ).add_to(grupo)

    Marker(
        location=[lat, lon],
        popup="Punto de interés",
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(grupo)

    grupo.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    return m
