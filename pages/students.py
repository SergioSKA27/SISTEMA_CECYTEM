import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from streamlit_elements import elements, mui, html
from streamlit_elements import elements, sync, event
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_pandas_profiling import st_profile_report

if 'filters' not in st.session_state:
    st.session_state['filters'] = []

def posible_grouping(data):
    cols = []
    for col in data.columns:
        if data[col].dtype == 'object' and len(data[col].unique()) < 30:
            cols.append(col)
    return cols


#Student ID,student_name,gender,grade,school_name,reading_score,math_score
data = pd.read_csv('students_complete.csv')








fillter = st.multiselect('Selecciona los campos a mostrar',list(data.columns),placeholder='Selecciona los campos a mostrar')


pcols = st.multiselect('Selecciona los campos a agrupar',posible_grouping(data),placeholder='Selecciona los campos a agrupar')
if len(pcols) > 0:
    for d in data.groupby(pcols):
        st.write('Grupo: ' + str(d[0]))
        st.write(d[1])

st.write(len(data.groupby('school_name')))
if st.checkbox('Editar'):
    if len(fillter) == 0:
        st.data_editor(data,use_container_width=True)
    else:
        st.data_editor(data[fillter],use_container_width=True)
else:
    if len(fillter) == 0:
        st.dataframe(data,use_container_width=True)
    else:
        st.dataframe(data[fillter],use_container_width=True)



st.subheader('Graficas')


tipo = st.selectbox('Tipo de grafica',['Barra','Linea','Area','Dispersión','Torta','Histograma','Boxplot','Violin','3D','Mapa'])

if tipo == 'Barra':
    colum = st.multiselect('Columnas a graficar',list(data.columns)[2:],placeholder='Selecciona una columna',max_selections=2)
    with st.spinner('Generando grafica...',cache=True):
        if len(colum) > 1:
            fig = px.bar(data, x=colum[0],y=colum[1])
            st.plotly_chart(fig, use_container_width=True)



st.subheader('Reporte de Perfilamiento')
pr = data.profile_report()

st_profile_report(pr)
