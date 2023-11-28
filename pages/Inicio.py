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
from mitosheet.streamlit.v1 import spreadsheet

#Esta es la pagina de inicio, donde se muestra el contenido de la pagina visible para todos los usuarios


#Configuracion de la pagina
st.set_page_config(page_title="Inicio", page_icon=":house:", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    [data-testid="collapsedControl"] {
        display: none
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


# Add on_change callback
def on_change(key):
    selection = st.session_state[key]
    st.write(f"Selection changed to {selection}")


@st.cache_data
def runballoons():
    """
    The function `runballoons` runs the balloons animation on the page.
    """
    st.balloons()
#--------------------------------------------------
#credenciales de la base de datos
data,xta = get_credentials()

credentials = credentials_formating(data['records'])
cookie_manager = get_manager()

#--------------------------------------------------
#variables de Session State
if "ballons" not in st.session_state:
    st.session_state.ballons = True





#--------------------------------------------------
#Authentication
if "authentication_status" not in st.session_state  :
    switch_page('Main')
else:
# el usuario debe estar autenticado para acceder a esta página
    if st.session_state["authentication_status"]:
            #--------------------------------------------------
            #Ballons
            if st.session_state.ballons:
                runballoons()
                st.session_state.ballons = False

            #--------------------------------------------------
            #usrdata
            usrdata = get_current_user_info(st.session_state['username'])
            #--------------------------------------------------
            #Configuracion de Credentials
            with open('config.yaml') as file:
                config = yaml.load(file, Loader=SafeLoader)

            authenticator = stauth.Authenticate(
                {'usernames':credentials},
                config['cookie']['name'],
                config['cookie']['key'],
                config['cookie']['expiry_days'],
                config['preauthorized']
            )

            #--------------------------------------------------
            #Log out button
            logcols = st.columns([0.8,0.2])
            with logcols[-1]:
                authenticator.logout('Cerrar Sesión', 'main', key='unique_key')



            #--------------------------------------------------
            #Navbar
            # CSS style definitions
            selected3 = option_menu(None, ["Inicio", "Alumnos",  "Profesores","Vinculación", "Orientación","Perfil"],
                icons=['house', 'mortarboard', "easel2", 'link', 'compass', 'person-heart'],
                menu_icon="cast", default_index=0, orientation="vertical",
                styles={
                    "container": {"padding": "0!important", "background-color": "#e6f2f0"},
                    "icon": {"color": "#175947", "font-size": "25px"},
                    "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#FBA1A1"},
                    "nav-link-selected": {"background-color": "#FBC5C5"},
                },on_change=on_change,key='menu'
            )
            if selected3 == 'Alumnos':
                switch_page('AlumnosHome')
            elif selected3 == 'Perfil':
                switch_page('Perfil')
            #--------------------------------------------------
            #Contenido de la pagina
            sac.alert(message=f'Bienvenido {st.session_state.name}',
            description=f'Tu rol actual es {usrdata["role"]} ', banner=True, icon=True, closable=True, height=100)
            st.toast(f'Bienvenido {st.session_state["name"]}',icon='👋')
            st.title('Sistema de Administración Escolar CECYTEM')
            st_lottie('https://lottie.host/204fe26b-ee80-4dfe-b95c-e1bcabbcf8ef/11JlAAyTKa.json',key='mainbanner')
