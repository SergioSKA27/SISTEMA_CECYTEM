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
#Esta es la pagina de inicio, donde se muestra el contenido de la pagina visible para todos los usuarios


#Configuracion de la pagina
st.set_page_config(page_title="Inicio", page_icon=":house:", layout="wide", initial_sidebar_state="collapsed")
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


#--------------------------------------------------
#credenciales de la base de datos
data,xta = get_credentials()
#data
credentials = credentials_formating(data['records'])
cookie_manager = get_manager()


st.session_state


#--------------------------------------------------
#Authentication
if "authentication_status" not in st.session_state  :
    switch_page('Main')
else:
# el usuario debe estar autenticado para acceder a esta página
    if st.session_state["authentication_status"]:




            # Add on_change callback
            def on_change(key):
                selection = st.session_state[key]
                st.write(f"Selection changed to {selection}")
            # CSS style definitions
            selected3 = option_menu(None, ["Inicio", "Alumnos",  "Profesores", 'Perfil'],
                icons=['house', 'cloud-upload', "list-task", 'gear'],
                menu_icon="cast", default_index=0, orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "25px"},
                    "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "green"},
                },on_change=on_change,key='menu'
            )


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

            authenticator.logout('Cerrar Sesión', 'main', key='unique_key')
            sac.alert(message=f'Bienvenido {st.session_state.name}',
            description=f'Tu rol actual es {usrdata["role"]} ', banner=True, icon=True, closable=True, height=100)
            st.toast(f'Bienvenido {st.session_state["name"]}',icon='👋')
            st.title('Sistema de Administración Escolar CECYTEM')
            st_lottie('https://lottie.host/204fe26b-ee80-4dfe-b95c-e1bcabbcf8ef/11JlAAyTKa.json')

            # Herramientas de desarrollador disponibles solo para el administrador
            #if usrdata['role'] == 'admin':
            #  if st.checkbox('Developer Tools'):

            #    st.subheader("All Cookies:")
            #    cookies = cookie_manager.get_all()
            #    st.write(cookies)

            #    c1, c2, c3 = st.columns(3)

            #    with c1:
            #        st.subheader("Get Cookie:")
            #        cookie = st.text_input("Cookie", key="0")
            #        clicked = st.button("Get")
            #        if clicked:
            #            value = cookie_manager.get(cookie=cookie)
            #            st.write(value)
            #    with c2:
            #        st.subheader("Set Cookie:")
            #        cookie = st.text_input("Cookie", key="1")
            #        val = st.text_input("Value")
            #        if st.button("Add"):
            #            cookie_manager.set(cookie, val) # Expires in a day by default
            #    with c3:
            #        st.subheader("Delete Cookie:")
            #        cookie = st.text_input("Cookie", key="2")
            #        if st.button("Delete"):
            #            cookie_manager.delete(cookie)

            #    st.subheader("Session State:")
            #    st.divider()
            #    st.session_state



