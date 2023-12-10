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
from streamlit_elements import elements, mui, html
from streamlit_elements import elements, sync, event
import json

from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace


from modules import Dashboard,Editor, Card, DataGrid, Radar, Pie, Player,Bar
import asyncio
import concurrent.futures
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






#Esta es la pagina de inicio, donde se muestra el contenido de la pagina visible para todos los usuarios


#Configuracion de la pagina
st.set_page_config(page_title="Alumnos", page_icon="rsc/Logos/cecytem-logo.png", layout="wide", initial_sidebar_state="collapsed")

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
    top: 0;
    }
</style>
""",unsafe_allow_html=True)
#--------------------------------------------------
#Funciones

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
                "curp.curp",
                "estatus.current_status",
            ]
    })
    for i in data['records']:
        i['curp'] = i['curp']['curp']
        i['estatus'] = i['estatus']['current_status']
    return data

async def get_all_students_async():
    loop = asyncio.get_event_loop()

    with concurrent.futures.ThreadPoolExecutor() as pool:
        data = await loop.run_in_executor(pool, get_all_students)

        return data



#--------------------------------------------------

cookie_manager = get_manager()


#st.session_state
if "Alumnos_options" not in st.session_state or st.session_state.Alumnos_options != None:
    st.session_state.Alumnos_options = None

#--------------------------------------------------
#Authentication
if "authentication_status" not in st.session_state  :
    switch_page('Main')
else:
# el usuario debe estar autenticado para acceder a esta página
    if st.session_state["authentication_status"]:



           #--------------------------------------------------
            #Navbar
            # CSS style definitions
            selected3 = option_menu(None, ["Inicio", "Alumnos",  "Profesores","Vinculación", "Orientación",st.session_state.username,"Cerrar Sesión"],
                icons=['house', 'mortarboard', "easel2", 'link', 'compass', 'person-heart','door-open'],
                menu_icon="cast", default_index=1, orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#e6f2f0"},
                    "icon": {"color": "#1B7821", "font-size": "20px"},
                    "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#4F758C"},
                    "nav-link-selected": {"background-color": "#0F4C59"},
                },key='menu'
            )
            if selected3 == 'Inicio':
                switch_page('Inicio')
            elif selected3 == st.session_state.username:
                switch_page('Perfil')

            elif selected3 == 'Cerrar Sesión':
                st.session_state["authentication_status"] = False
                st.session_state["username"] = None
                st.session_state["name"] = None
                st.session_state["role"] = None
                st.session_state["record_id"] = None
                switch_page('Login')


            #-------------------------------------------------
            st.title("Alumnos")
            st.markdown("En esta sección se pueden registrar alumnos, buscarlos y buscar grupos")

            options = option_menu(None, ['',"Registrar Alumno","Buscar Alumno","Buscar grupo","Estadísticas","Reportes DEO"],
                icons=['house-gear-fill','person-plus', 'search', "ui-checks-grid","graph-up-arrow","file-earmark-bar-graph"],
                menu_icon="cast", default_index=0, orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#e6f2f0"},
                    "icon": {"color": "#FFFFFF", "font-size": "25px"},
                    "nav-link": {"font-size": "20px", "text-align": "center", "margin":"0px", "--hover-color": "#4F758C"},
                    "nav-link-selected": {"background-color": "#0F4C59"},
                },key='options'
            )

            if options == "Registrar Alumno" :
                if st.session_state['role'] in ['orientacion','admin']:
                    switch_page('registroAlumno1')
                else:
                    st.warning("No tienes permisos para acceder a esta sección")


            if options == "Buscar Alumno" :
                if st.session_state['role'] in ['orientacion','admin','vinculacion','profesor']:
                    switch_page('searchengineAlumnos')
                else:
                    st.warning("No tienes permisos para acceder a esta sección")


            if options == "Reportes DEO" :
                if st.session_state['role'] in ['orientacion','admin','profesor']:
                    switch_page('reportesDEO')
                else:
                    st.warning("No tienes permisos para acceder a esta sección")
            #-------------------------------------------------
            #Obtener datos de la base de datos
            stdudents =asyncio.run(get_all_students_async())['records']
            df = pd.DataFrame(stdudents)
            del df['id'], df['xata']

            active = len(df[df['estatus'] == True])
            inactive = len(df[df['estatus'] == False])
            #-------------------------------------------------
            #Metricas
            metriccols = st.columns(3)
            with metriccols[0]:
                st.metric(label="Alumnos registrados", value=len(get_all_students()['records']), delta=1)
            with metriccols[1]:
                st.metric(label="Alumnos activos", value=active)
            with metriccols[2]:
                st.metric(label="Alumnos inactivos", value=inactive)


            #st.dataframe(df,use_container_width=True)
            #stdudents
            #-------------------------------------------------
            #Dashboard
            if "k" not in state:
                board = Dashboard()
                args = {}
                args["board"] = board
                k = SimpleNamespace(
                    dashboard=board,
                    pie=Pie(board, 8, 0, 4, 7, minW=3, minH=4),
                    radar=Radar(board, 0, 4, 6, 7, minW=2, minH=4),
                    card=Card(board, 6, 4, 6, 7, minW=2, minH=4),
                    data_grid=DataGrid(board, 0, 0, 8, 7, minH=4),
                    barplot=Bar(board, 0, 12, 8, 7, minH=4),
                )
                state.k = k

            else:
                k = state.k

            with elements("demo"):
                event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
                piedata = [
                    { "id": "Estudiantes Activos", "label": "Activos", "value":active, "color": "hsl(128, 70%, 50%)" },
                    { "id": "Estudiantes Inactivos", "label": "Inactivos", "value": inactive, "color": "hsl(322, 70%, 50%)"},
                    ]
                radardata =[
                    { "taste": "fruity", "chardonay": 93, "carmenere": 61, "syrah": 114 },
                    { "taste": "bitter", "chardonay": 91, "carmenere": 37, "syrah": 72 },
                    { "taste": "heavy", "chardonay": 56, "carmenere": 95, "syrah": 99 },
                    { "taste": "strong", "chardonay": 64, "carmenere": 90, "syrah": 30 },
                    { "taste": "sunny", "chardonay": 119, "carmenere": 94, "syrah": 103 },
                    ]

                columnas = [
                    { "field": 'idcontrol', "headerName": 'ID', "width": 90 },
                    { "field": 'plantelAlumno', "headerName": 'PLANTEL', "width": 200, "editable": False, },
                    { "field": 'carreraAlumno', "headerName": 'CARRERA', "width": 250, "editable": False, },
                    { "field": 'curp', "headerName": 'CURP',  "width": 120, "editable": False, },
                    { "field": 'estatus', "headerName": 'ESTATUS', "width": 110, "editable": False, "type": "boolean"},
                    ]

                with k.dashboard(rowHeight=57):
                    k.pie(json.dumps(piedata),title='Alumnos Activos e Inactivos')
                    k.radar(json.dumps(radardata))
                    k.card('HI','https://www.certus.edu.pe/blog/wp-content/uploads/2020/09/que-es-data-analytics-importancia-1-1200x720.jpg')
                    k.data_grid(json.dumps(stdudents),columnas,title='Alumnos')

