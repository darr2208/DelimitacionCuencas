import folium
import geopandas as gpd
from shapely.geometry import Point
from folium.plugins import Draw

def generar_mapa_cuenca(lat, lon, radio_km=1.0):
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

    radio_grados = radio_km / 111

    centro = Point(lon, lat)
    gdf = gpd.GeoDataFrame(index=[0], geometry=[centro.buffer(radio_grados)], crs="EPSG:4326")
    geojson_data = gdf.__geo_interface__

    folium.GeoJson(
        geojson_data,
        name='Cuenca simulada',
        style_function=lambda x: {
            'fillColor': '#e60000',     # Rojo fuerte
            'color': '#990000',         # Borde más oscuro
            'weight': 4,                # Borde grueso
            'fillOpacity': 0.7          # Más opaco para visibilidad
        },
        tooltip='Cuenca simulada'
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    return m
