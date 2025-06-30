import folium
from folium import Marker, FeatureGroup, Polygon
import math

def generar_mapa_cuenca(lat, lon, radio_km=2.0, puntos=30):
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
    coords = []

    for i in range(puntos):
        ang = 2 * math.pi * i / puntos
        r_factor = 1 + 0.3 * math.sin(3 * ang)  # deformación irregular
        lat_i = lat + r_factor * delta * math.cos(ang)
        lon_i = lon + r_factor * delta * math.sin(ang) / math.cos(math.radians(lat))
        coords.append([lat_i, lon_i])

    coords.append(coords[0])

    grupo = FeatureGroup(name='Cuenca simulada')

    Polygon(
        locations=coords,
        color="#0044cc",
        weight=3,
        fill=True,
        fill_color="#3399ff",
        fill_opacity=0.5,
        tooltip="Cuenca simulada"
    ).add_to(grupo)

    Marker(
        location=[lat, lon],
        popup="Punto de interés",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(grupo)

    grupo.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    return m
