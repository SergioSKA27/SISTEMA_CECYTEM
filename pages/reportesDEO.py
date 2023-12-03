import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import yaml
from yaml.loader import SafeLoader
from streamlit_option_menu import option_menu
import extra_streamlit_components as stx
from streamlit_lottie import st_lottie
import datetime
import pandas as pd
import numpy as np
import json
from mitosheet.streamlit.v1 import spreadsheet

# License: BSD 3-Clause

#Sistema de Gestión y Análisis CECYTEM

#Copyright (c) 2023 Sergio Demis Lopez Martinez

#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:

#1. Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.

#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

#3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


#Configuración de la página
st.set_page_config(page_title="Buscador de Alumnos", page_icon=":mag_right:", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    [data-testid="collapsedControl"] {
        display: none
    }
    .st-emotion-cache-1t2qdok {
    width: 1189px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 0rem;
    }

    .st-emotion-cache-z5fcl4 {
    width: 100%;
    padding: 0rem 0rem 0rem;
    padding-right: 1rem;
    padding-left: 1rem;
    min-width: auto;
    max-width: initial;
    top: 0px;
    }
</style>
""",unsafe_allow_html=True)

#--------------------------------------------------
#Funciones
def get_credentials():
  """
  The function `get_credentials` retrieves credentials data from a database using an API key and database URL.
  :return: The function `get_credentials` returns the data retrieved from the XataClient API.
  """
  xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
  data = xata.data().query("Credentials", {
    "columns": [
        "id",
        "username",
        "email",
        "password",
        "avatar",
        "name",
        "role"
    ],
  })
  return data,xata

@st.cache_data
def credentials_formating(credentials):
  """
  The function `credentials_formating` takes a list of dictionaries representing credentials and returns a formatted
  dictionary with usernames as keys and corresponding password, email, and name as values.

  :param credentials: The parameter "credentials" is a list of dictionaries. Each dictionary represents a set of
  credentials and has the following keys: 'username', 'password', 'email', and 'name'
  :return: a dictionary where the keys are the usernames from the input credentials list, and the values are dictionaries
  containing the password, email, and name for each username.
  """
  c = {}
  for credential in credentials:
    c[credential['username']] = {'password': credential['password'], 'email': credential['email'],'name': credential['name']}

  return c

def get_current_user_info(usrname):
    """
    The function `get_current_user_info` retrieves the information of the current user based on their username from a
    database.

    :param usrname: The `usrname` parameter is the username of the user whose information you want to retrieve
    :return: The function `get_current_user_info` returns the information of the current user specified by the `usrname`
    parameter.
    """
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    ch = xata.data().query("Credentials",{"filter": {"username": usrname}})
    return ch['records'][0]

def get_manager():
    """
    The function `get_manager` returns a `CookieManager` object with the key 'MyCookieManager'.
    :return: an instance of the `CookieManager` class with the key set to 'MyCookieManager'.
    """
    return stx.CookieManager(key='MyCookieManager')

def get_all_students():
    """
    The function `get_all_students` retrieves all the students from a database.
    :return: The function `get_all_students` returns a list of dictionaries representing the students in the database.
    """
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.data().query("Alumno", {
            "columns": [
                "id",
                "carreraAlumno",
                "plantelAlumno",
                "idcontrol",
                "curp.curp"
            ],
    })
    for i in data['records']:
        i['curp'] = i['curp']['curp']
    return data


def reg_calificacion(id_alumno,calificacion,asignatura,grupo,semestre,evaluacion):
    """
    The function `reg_calificacion` registers a grade for a student in a database.

    :param id_alumno: The `id_alumno` parameter is the id of the student whose grade you want to register.
    :param calificacion: The `calificacion` parameter is the grade you want to register.
    :param asignatura: The `asignatura` parameter is the subject of the grade you want to register.
    :param grupo: The `grupo` parameter is the group of the student whose grade you want to register.
    :return: The function `reg_calificacion` returns the response from the XataClient API.
    """
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.records().insert("Calificacion", {
    "semestre": semestre,
    "grupo": grupo,
    "asignatura": asignatura.upper(),
    "evaluacion": evaluacion,
    "calificacion": calificacion,
    "num_control": id_alumno
    })

# Add on_change callback
def on_change(key):
    st.session_state.Alumnos_options = key
    selection = st.session_state['Alumnos_options']
    st.write(f"Selection changed to {selection}")

#--------------------------------------------------
#credenciales de la base de datos
data,xta = get_credentials()
#data
credentials = credentials_formating(data['records'])
cookie_manager = get_manager()


if "Alumnos_search" not in st.session_state:
    st.session_state['Alumnos_search'] = None

#--------------------------------------------------
#Authentication
if "authentication_status" not in st.session_state  :
    switch_page('Main')
else:
# el usuario debe estar autenticado para acceder a esta página
    if st.session_state["authentication_status"]:

            usrdata = get_current_user_info(st.session_state['username'])

            #usrdata
            #--------------------------------------------------
            with open('config.yaml') as file:
                config = yaml.load(file, Loader=SafeLoader)

            authenticator = stauth.Authenticate(
                {'usernames':credentials},
                config['cookie']['name'],
                config['cookie']['key'],
                config['cookie']['expiry_days'],
                config['preauthorized']
            )
            st_lottie("https://lottie.host/b7ef026c-555f-42ba-8c63-d34ab2c09d34/ZozkKz25so.json",width=300,height=200,speed=1)
            logcols = st.columns([0.2,0.6,0.2])
            with logcols[0]:
                backpp = sac.buttons([
                    sac.ButtonsItem(label='REGRESAR',icon='skip-backward-btn'),
                ], position='left', format_func='upper', align='center', size='large',
                shape='round', return_index=True,index=1)

                if backpp == 0:
                    switch_page('AlumnosHome')

            with logcols[-1]:
                authenticator.logout('Cerrar Sesión', 'main', key='unique_key')
            # CSS style definitions
            selected3 = option_menu(None, ["Inicio", "Alumnos",'Reportes DEO'],
                icons=['house', 'mortarboard', 'file-earmark-bar-graph'],
                menu_icon="cast", default_index=2, orientation="vertical",
                styles={
                    "container": {"padding": "0!important", "background-color": "#e6f2f0"},
                    "icon": {"color": "#175947", "font-size": "25px"},
                    "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#FBA1A1"},
                    "nav-link-selected": {"background-color": "#FBC5C5"},
                },key='menu'
            )
            if selected3 == 'Inicio':
                switch_page('Inicio')
            elif selected3 == 'Alumnos':
                switch_page('AlumnosHome')

            #--------------------------------------------------
            #Student ID,student_name,gender,grade,school_name,reading_score,math_score
            excelf = st.file_uploader("Subir Reporte de Alumnos de DEO",type=['csv','xlsx'])

            if excelf is not None:
                try:
                    data = pd.read_excel(excelf)
                except:
                    data = pd.read_csv(excelf)



                # Display the dataframe in a Mito spreadsheet, no puede tener mas de 1500 filas
                final_dfs, code = spreadsheet(data)
                st.warning('No se pueden subir mas de 100 registros a la vez, recomendamos subir los registros por grupos')
                if st.button('Subir Calificaciones'):
                    with st.spinner('Subiendo Calificaciones...'):
                        for i in range(len(data)):
                            reg_calificacion(str(data['No de control'][i]),int(data['Calificación'][i]),data['Asignatura'][i],int(data['Grupo'][i]),int(data['Semestre'][i]),data['Evaluación'][i])
                        st.success('Calificaciones subidas con éxito :heart:')

                # Display the final dataframes created by editing the Mito component
                # This is a dictionary from dataframe name -> dataframe
                #st.write(final_dfs)

                # Display the code that corresponds to the script
                #st.code(code)
                st.subheader('Registros por Agrupación')
                st.divider()
                group = []
                agrupar_por_grupo = st.checkbox('Agrupar por grupo')
                agrupar_por_asignatura = st.checkbox('Agrupar por asignatura')
                agrupar_por_alumno = st.checkbox('Agrupar por alumno')

                if agrupar_por_grupo:
                    group.append('Grupo')
                if agrupar_por_asignatura:
                    group.append('Asignatura')
                if agrupar_por_alumno:
                    group.append('Alumno')


                if len(group) > 0:
                    gr = data.groupby(group)

                    dfs = []

                    for i in gr:
                        dfs.append(i[1])

                    daf = sac.pagination(total=len(dfs), align='center', circle=True, jump=True, show_total=True,page_size=1)
                    df = dfs[daf-1]
                    st.write(df)

                    if st.button('Subir Calificaciones',key='subir'):
                        with st.spinner('Subiendo Calificaciones...'):
                            for i in range(len(df)):
                                data = df.iloc[i]
                                reg_calificacion(str(data['No de control']),int(data['Calificación']),data['Asignatura'],int(data['Grupo']),int(data['Semestre']),data['Evaluación'])
                            st.success('Calificaciones subidas con éxito :hugging_face:')
