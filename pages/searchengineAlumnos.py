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
from streamlit_searchbox import st_searchbox

from streamlit_elements import elements, mui, html
from streamlit_elements import elements, sync, event


from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace


from modules import Dashboard,Editor, Card, DataGrid, Radar, Pie, Player

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
    top: 0;
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

def search_student(search: str)-> list[any]:
    """
    The function `search_student` searches for a student in the database based on the search parameter.

    :param search: The `search` parameter is a string that represents the student's name, email, or username.
    :return: The function `search_student` returns a list of dictionaries representing the students that match the search
    parameter.
    """
    search = search.upper()
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.data().query("Alumno", {
            "columns": [
                "id",
                "carreraAlumno",
                "plantelAlumno",
                "idcontrol",
                "curp.*"
            ],
            "filter": {
                    "$any": [
                    {"curp.curp": {"$contains": search}},
                    {"idcontrol": {"$contains": search}},
                    {"curp.nombre": {"$contains": search}},
                    {"curp.apellidoPaterno": {"$contains": search}},
                    {"curp.apellidoMaterno": {"$contains": search}},]


            }
    })
    #st.write(data)
    d = []

    for i in data['records']:
        d.append(','.join([i['idcontrol'],i['curp']['curp'],i['curp']['nombre'],i['curp']['apellidoPaterno'],i['curp']['apellidoMaterno']]))

    return d if search else []


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
            selected3 = option_menu(None, ["Inicio", "Alumnos",'Buscar Alumnos'],
                icons=['house', 'mortarboard', 'search'],
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


            st.title('Buscador de Alumnos :mag_right:')
            st.divider()

            #--------------------------------------------------

            r = st_searchbox(search_function=search_student,
            placeholder="Buscar Alumno(Nombre, Apellido, CURP, ID Control)",
            key='searchbox',clear_on_submit=True)

            if r != None:
                r
                data = r.split(',')
                st.session_state['Alumnos_Search'] = data[0]
                if usrdata['role'] in ['admin','maestro','orientacion','vinculacion']:
                    if st.button('Ver Perfil'):
                        switch_page('perfilAlumno')


            if "w" not in state:
                board = Dashboard()
                args = {}
                args["board"] = board
                w = SimpleNamespace(
                    dashboard=board,
                    editor=Editor(board, 0, 0, 6, 11,),
                    player=Player(board, 7, 0, 4, 10, minH=5),
                    pie=Pie(board, 6, 0, 6, 7, minW=3, minH=4),
                    radar=Radar(board, 12, 7, 3, 7, minW=2, minH=4),
                    card=Card(board, 6, 7, 3, 7, minW=2, minH=4),
                    data_grid=DataGrid(board, 6, 13, 6, 7, minH=4),
                )
                state.w = w

                w.editor.add_tab("Card content", Card.DEFAULT_CONTENT, "plaintext")
                w.editor.add_tab("Data grid", json.dumps(DataGrid.DEFAULT_ROWS, indent=2), "json")
                w.editor.add_tab("Radar chart", json.dumps(Radar.DEFAULT_DATA, indent=2), "json")
                w.editor.add_tab("Pie chart", json.dumps(Pie.DEFAULT_DATA, indent=2), "json")
            else:
                w = state.w

            with elements("demo"):
                event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

                with w.dashboard(rowHeight=57):
                    w.editor()
                    w.player()
                    w.pie(w.editor.get_content("Pie chart"))
                    w.radar(w.editor.get_content("Radar chart"))
                    w.card(w.editor.get_content("Card content"))
                    w.data_grid(w.editor.get_content("Data grid"))

            #--------------------------------------------------

