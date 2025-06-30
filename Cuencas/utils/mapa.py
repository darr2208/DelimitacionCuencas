import folium
from shapely.geometry import Polygon
import geopandas as gpd

def generar_mapa_cuenca(lat, lon, km2=3):
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

    lado_km = km2 ** 0.5
    delta_lat = lado_km / 111
    delta_lon = lado_km / (111 * abs(math.cos(math.radians(lat))) + 1e-6)

    coords = [
        [lat + delta_lat / 2, lon - delta_lon / 2],
        [lat + delta_lat / 2, lon + delta_lon / 2],
        [lat - delta_lat / 2, lon + delta_lon / 2],
        [lat - delta_lat / 2, lon - delta_lon / 2],
        [lat + delta_lat / 2, lon - delta_lon / 2]
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
            'weight': 4,
            'fillOpacity': 0.6
        },
        tooltip='Cuenca simulada'
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    return m

