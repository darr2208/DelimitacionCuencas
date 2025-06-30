import streamlit as st
import folium
from folium import Marker
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import numpy as np

# 1. Input coordenada
lat = st.number_input("Latitud", value=6.25184)
lon = st.number_input("Longitud", value=-75.56359)

# 2. Mapa interactivo
st.write("### Mapa del punto")
m = folium.Map(location=[lat, lon], zoom_start=14, tiles="OpenTopoMap")
Marker([lat, lon], tooltip="Punto de interés").add_to(m)
st_folium(m, width=700, height=400)

# 3. Simulación de cuenca abajo (imagen tipo red hídrica)
st.write("### Simulación de cuenca generada")
fig, ax = plt.subplots(figsize=(6.5, 6.5))

# Simulación: líneas aleatorias como "ríos"
np.random.seed(0)
for i in range(20):
    x = np.linspace(0, 1, 100)
    y = np.sin(x * 2 * np.pi * (i+1)/10) / (i+1)
    ax.plot(x + i * 0.02, y + i * 0.01, color='skyblue')

# Representar contorno tipo cuenca
theta = np.linspace(0, 2 * np.pi, 100)
r = 0.4 + 0.1 * np.sin(3 * theta)
x = r * np.cos(theta)
y = r * np.sin(theta)
ax.plot(x, y, color='cyan', lw=2)

ax.set_title("Cuenca simulada desde coordenada")
ax.axis('off')
st.pyplot(fig)
