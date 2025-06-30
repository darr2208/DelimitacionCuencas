import folium
from folium.plugins import Draw
import geopandas as gpd
from shapely.geometry import Polygon

def generar_mapa_cuenca(lat, lon, geojson_data=None):
    m = folium.Map(
        location=[lat, lon],
        zoom_start=14,
        tiles=None,
        control_scale=True
    )

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='ESRI World Imagery',
        name='Satélite'
    ).add_to(m)

    folium.TileLayer(
        tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attr='OpenTopoMap',
        name='Topografía'
    ).add_to(m)

    if geojson_data is None:
        delta_lat = 0.01
        delta_lon = 0.015
        coords = [
            [lat, lon - delta_lon],
            [lat - delta_lat, lon],
            [lat, lon + delta_lon],
            [lat + delta_lat, lon],
            [lat, lon - delta_lon]
        ]
        poly = Polygon(coords)
        gdf = gpd.GeoDataFrame(index=[0], geometry=[poly], crs="EPSG:4326")
        geojson_data = gdf.__geo_interface__

    folium.GeoJson(
        geojson_data,
        name='Cuenca simulada',
        style_function=lambda x: {
            'fillColor': '#4da7db',
            'color': '#1768ac',
            'weight': 2,
            'fillOpacity': 0.3
        },
        tooltip='Delimitación automática'
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    return m
