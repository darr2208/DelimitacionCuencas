import streamlit as st
import folium
from folium import Marker
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import numpy as np

def generar_mapa_y_cuenca(lat, lon, buffer_km=2.0):
    m = folium.Map(location=[lat, lon], zoom_start=13, tiles="OpenTopoMap")
    Marker([lat, lon], tooltip="Punto de interés").add_to(m)

    radius_m = buffer_km * 1000
    folium.Circle(
        location=[lat, lon],
        radius=radius_m,
        color="blue",
        fill=True,
        fill_opacity=0.3,
        tooltip=f"Área simulada (radio: {buffer_km} km)"
    ).add_to(m)

    st_folium(m, width=700, height=450)

    fig, ax = plt.subplots(figsize=(6, 6))
    np.random.seed(0)
    for i in range(20):
        x = np.linspace(0, 1, 100)
        y = np.sin(x * 2 * np.pi * (i + 1) / 10) / (i + 1)
        ax.plot(x + i * 0.02, y + i * 0.01, color='skyblue')

    theta = np.linspace(0, 2 * np.pi, 100)
    r = 0.4 + 0.1 * np.sin(3 * theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    ax.plot(x, y, color='cyan', lw=2)

    ax.set_title("Cuenca simulada")
    ax.axis("off")
    st.pyplot(fig)
