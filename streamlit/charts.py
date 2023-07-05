import streamlit as st
import pandas as pd
import numpy as np

cantidad_por_tipo = {'Americano': 40000, 'Mozzarella': 10000, 'Lite Line': 20000}
st.title('Producto Almacenado:tada:')

st.sidebar.header('Opciones')
st.sidebar.subheader('Seleccione las opciones:')
st.sidebar.slider(label='Edad', min_value=1, max_value=110)
st.sidebar.subheader('Seleccione un tipo:')
st.sidebar.selectbox(label='Tipo:', options=['Americano','Mozzarella','Lite line'])
st.sidebar.select_slider('Pick a size', ['S', 'M', 'L'])
st.sidebar.radio('Pick one', ['cats', 'dogs'])
st.sidebar.button('Click me')

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Capacidad del almacén", value='75%', delta='454')
    st.metric(label="Capacidad del almacén", value='75%', delta='454')
with col2:
    st.subheader('Bar Chart')
    st.write("Este es un ejemplo para ver como se ve streamlit")
    st.bar_chart(cantidad_por_tipo)

st.line_chart(np.random.randn(30, 2))

