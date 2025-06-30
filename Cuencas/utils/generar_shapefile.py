import geopandas as gpd
from shapely.geometry import box
import os
import zipfile
import time

def generar_shapefile_desde_bbox(minx, miny, maxx, maxy, carpeta_salida="data/outputs", nombre="cuenca"):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    nombre_base = os.path.join(carpeta_salida, nombre)
    geometria = box(minx, miny, maxx, maxy)
    gdf = gpd.GeoDataFrame({'nombre': [nombre]}, geometry=[geometria], crs="EPSG:4326")

    gdf.to_file(f"{nombre_base}.shp", driver="ESRI Shapefile")

    time.sleep(0.5)

    ruta_zip = f"{nombre_base}.zip"
    with zipfile.ZipFile(ruta_zip, 'w') as zipf:
        for ext in ['.shp', '.shx', '.dbf', '.cpg', '.prj']:
            archivo = f"{nombre_base}{ext}"
            if os.path.exists(archivo):
                zipf.write(archivo, os.path.basename(archivo))
                os.remove(archivo)

    return ruta_zip
