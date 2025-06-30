import folium
from shapely.geometry import Polygon
import geopandas as gpd
from folium.plugins import Draw

def generar_mapa_cuenca(lat, lon, geojson_data=None):
    m = folium.Map(
        location=[lat, lon],
        zoom_start=15,
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
        coords = [
            [lat + 0.002, lon - 0.002],
            [lat + 0.002, lon + 0.002],
            [lat, lon + 0.003],
            [lat - 0.002, lon + 0.002],
            [lat - 0.002, lon - 0.002],
            [lat, lon - 0.003],
            [lat + 0.002, lon - 0.002]
        ]
        poly = Polygon(coords)
        gdf = gpd.GeoDataFrame(index=[0], geometry=[poly], crs="EPSG:4326")
        geojson_data = gdf.__geo_interface__

    folium.GeoJson(
        geojson_data,
        name='Cuenca simulada',
        style_function=lambda x: {
            'fillColor': '#ff69b4',
            'color': '#ff1493',
            'weight': 5,
            'fillOpacity': 0.5
        },
        tooltip='Cuenca simulada'
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    return m
