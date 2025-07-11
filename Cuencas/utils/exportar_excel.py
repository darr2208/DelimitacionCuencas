import pandas as pd
import os

def exportar_a_excel(df_parametros, df_alturas, carpeta_salida="data/outputs", nombre_archivo="parametros.xlsx"):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    if not nombre_archivo.endswith(".xlsx"):
        nombre_archivo += ".xlsx"

    ruta = os.path.join(carpeta_salida, nombre_archivo)

    df_parametros["Parámetro"] = df_parametros["Parámetro"].astype(str)
    df_parametros["Clasificación"] = df_parametros["Clasificación"].astype(str)

    with pd.ExcelWriter(ruta, engine='openpyxl') as writer:
        df_parametros.to_excel(writer, index=False, sheet_name='Parámetros Morfométricos')
        df_alturas.to_excel(writer, index=False, sheet_name='Clases Altitudinales')

    return ruta
