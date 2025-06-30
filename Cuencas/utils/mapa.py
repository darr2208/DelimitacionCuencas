import folium
from shapely.geometry import Point
import geopandas as gpd

def generar_mapa_cuenca(lat, lon, radio_km=1.0):
    m = folium.Map(
        location=[lat, lon],
        zoom_start=14,
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

    radio_grados = radio_km / 111.0
    punto = Point(lon, lat)
    gdf = gpd.GeoDataFrame(geometry=[punto.buffer(radio_grados)], crs="EPSG:4326")
    coords = list(gdf.iloc[0].geometry.exterior.coords)
    coords_latlon = [[latitud, longitud] for longitud, latitud in coords]

    folium.Polygon(
        locations=coords_latlon,
        color="#d00000",
        weight=4,
        fill=True,
        fill_color="#ff4d4d",
        fill_opacity=0.6,
        tooltip="Área simulada"
    ).add_to(m)

    folium.Marker(
        location=[lat, lon],
        popup="Punto de interés",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    return m
