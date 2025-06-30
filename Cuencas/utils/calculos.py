import random
import math
import pandas as pd

def calcular_parametros(minx, miny, maxx, maxy):
    area_km2 = round(abs((maxx - minx) * (maxy - miny) * 111 * 111), 2)
    area_ha = round(area_km2 * 100, 2)
    perimetro_km = round(2 * (abs(maxx - minx) + abs(maxy - miny)) * 111, 2)
    ic = round(perimetro_km / (2 * math.sqrt(math.pi * area_km2)), 2)
    tipo = "Alargada" if ic > 1.5 else "Compacta"
    longitud_cuenca = round(math.sqrt(area_km2) * random.uniform(1.1, 1.5), 2)
    ff = round(area_km2 / (longitud_cuenca ** 2), 2)
    forma_cuenca = "Elongada" if ff < 0.3 else "Intermedia"
    cp_l = round(longitud_cuenca * random.uniform(0.8, 1.2), 2)
    cp = round(cp_l * random.uniform(0.85, 1.1), 2)
    fs = round(cp / cp_l, 2)
    clasif_fs = "Rectilínea" if fs < 1.2 else "Sinuosa"
    long_total_cauces = round(area_km2 * random.uniform(1.2, 2.5), 2)
    densidad_drenaje = round(long_total_cauces / area_km2, 2)
    clasif_dd = "Baja" if densidad_drenaje < 1 else "Media-Alta"
    cota_min = random.randint(100, 500)
    cota_max = cota_min + random.randint(500, 1500)
    dif_altura = cota_max - cota_min
    num_drenajes = int(area_km2 * random.uniform(1.5, 3.5))
    densidad_corrientes = round(num_drenajes / area_km2, 2)
    slope_deg = round(random.uniform(2, 25), 2)
    slope_pct = round(math.tan(math.radians(slope_deg)) * 100, 2)

    tiempos = {
        'Giandotti': round((0.00013 * (area_km2 ** 0.77) * (dif_altura ** -0.385)), 2),
        'Bransby-Williams': round((0.304 * (area_km2 ** 0.5) + 0.305), 2),
        'California Culvert Practice': round((0.87 * (longitud_cuenca ** 0.77) * (slope_deg ** -0.385)), 2),
        'Clark': round(random.uniform(1.5, 3.5), 2),
        'Passini': round(random.uniform(0.8, 2.5), 2),
        'Pilgrim y Mcdermott': round(random.uniform(1.1, 3.2), 2),
        'Valencia y Zuluaga': round(random.uniform(1.3, 2.8), 2),
        'Kirpich': round((0.01947 * (longitud_cuenca ** 0.77) * (slope_pct ** -0.385)), 2),
        'Temez': round(random.uniform(2, 5), 2)
    }
    tiempos['Promedio'] = round(sum(tiempos.values()) / len(tiempos), 2)

    datos = [
        ("Área (km2)", area_km2, ""),
        ("Área (ha)", area_ha, ""),
        ("Perímetro (km)", perimetro_km, ""),
        ("Índice de Compacidad", ic, ""),
        ("Tipo según IC", None, tipo),
        ("Longitud de la Cuenca (km)", longitud_cuenca, ""),
        ("Factor de Forma", ff, ""),
        ("Forma de la Cuenca", None, forma_cuenca),
        ("Longitud CP_L (km)", cp_l, ""),
        ("Longitud CP (km)", cp, ""),
        ("Factor de Sinuosidad", fs, ""),
        ("Clasificación Sinuosidad", None, clasif_fs),
        ("Longitud Total de Cauces (km)", long_total_cauces, ""),
        ("Densidad de Drenaje", densidad_drenaje, ""),
        ("Clasificación Drenaje", None, clasif_dd),
        ("Cota Mínima (msnm)", cota_min, ""),
        ("Cota Máxima (msnm)", cota_max, ""),
        ("Diferencia de Altura (m)", dif_altura, ""),
        ("Número de Drenajes", num_drenajes, ""),
        ("Densidad de Corrientes", densidad_corrientes, ""),
        ("Pendiente (°)", slope_deg, ""),
        ("Pendiente (%)", slope_pct, "")
    ] + [(k, v, "") for k, v in tiempos.items()]

    df = pd.DataFrame(datos, columns=["Parámetro", "Valor", "Clasificación"])

    alturas = []
    for i in range(5):
        alt_min = cota_min + i * (dif_altura // 5)
        alt_max = alt_min + (dif_altura // 5)
        altura_media = (alt_min + alt_max) // 2
        area_clase = round(area_km2 * random.uniform(0.1, 0.3), 2)
        area_m2 = round(area_clase * 1e6, 2)
        area_pct = round((area_clase / area_km2) * 100, 2)
        area_acum = round(sum([a[4] for a in alturas]) + area_clase, 2)
        area_acum_pct = round((area_acum / area_km2) * 100, 2)
        alturas.append([
            alt_min,
            alt_max,
            altura_media,
            area_m2,
            area_clase,
            area_acum,
            area_acum_pct,
            area_pct
        ])

    df_alturas = pd.DataFrame(alturas, columns=[
        "Limite Inferior", "Limite Superior", "Altura Media de Clase",
        "Area (M2)", "Area (Km2)", "Area Acumulada (Km2)",
        "Área Acumulada (%)", "Area % de cada clase"
    ])

    return df, df_alturas
