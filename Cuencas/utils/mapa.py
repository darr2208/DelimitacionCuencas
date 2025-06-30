import folium
from folium import Marker
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def generar_mapa_y_cuenca(lat, lon, buffer_km=2.0):
    m = folium.Map(location=[lat, lon], zoom_start=13, tiles="OpenStreetMap")
    Marker([lat, lon], tooltip="Punto de interés").add_to(m)
    folium.Circle(
        location=[lat, lon],
        radius=buffer_km * 1000,
        color="blue",
        fill=True,
        fill_opacity=0.3,
        tooltip=f"Área simulada (radio: {buffer_km} km)"
    ).add_to(m)
    st_folium(m, width=700, height=450)

    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    theta = np.linspace(0, 2 * np.pi, 100)
    r = 0.4 + 0.1 * np.sin(3 * theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    ax.plot(x, y, color='cyan', linewidth=2)

    np.random.seed(42)
    for _ in range(30):
        x0, y0 = np.random.uniform(-0.3, 0.3, 2)
        dx, dy = np.random.uniform(-0.05, 0.05, 2)
        ax.plot([x0, x0 + dx], [y0, y0 + dy], color='white', linewidth=0.8)

    ax.set_facecolor('black')
    ax.set_title(f"Cuenca simulada en ({lat}, {lon})", fontsize=12)
    ax.axis("off")
    st.pyplot(fig)


