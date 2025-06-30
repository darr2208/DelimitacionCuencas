import folium
from folium.plugins import Draw
import geopandas as gpd
from shapely.geometry import Polygon

def generar_mapa_cuenca(lat, lon, geojson_data=None):
    m = folium.Map(
        location=[lat, lon],
        zoom_start=13,
        tiles=None,
        control_scale=True
    )

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='ESRI World Imagery',
        name='Satélite',
        overlay=False,
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attr='OpenTopoMap',
        name='Topografía',
        overlay=False,
        control=True
    ).add_to(m)

    if geojson_data is None:
        buffer = 0.015
        coords = [
            [lat - buffer, lon - buffer],
            [lat - buffer, lon + buffer],
            [lat + buffer, lon + buffer],
            [lat + buffer, lon - buffer],
            [lat - buffer, lon - buffer]
        ]
        poly = Polygon(coords)
        gdf = gpd.GeoDataFrame(index=[0], geometry=[poly], crs="EPSG:4326")
        geojson_data = gdf.__geo_interface__

    folium.GeoJson(
        geojson_data,
        name='Delimitación de Cuenca',
        style_function=lambda x: {
            'fillColor': '#4da7db',
            'color': '#1768ac',
            'weight': 2,
            'fillOpacity': 0.45
        },
        tooltip='Cuenca simulada'
    ).add_to(m)

    Draw(
        export=True,
        filename='cuenca_dibujada.geojson',
        position='topleft'
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    return m
