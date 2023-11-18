import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import extra_streamlit_components as stx
import datetime
#Configuracion de la pagina
st.set_page_config(page_title="Login", page_icon=":lock:", layout="wide", initial_sidebar_state="collapsed")



#--------------------------------------------------
#Funciones
@st.cache_resource
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

def get_manager():
    return stx.CookieManager(key='MyCookieManager')


#--------------------------------------------------
#Estilos de la pagina
st.markdown('''
<style>
body {
background-color: #e5e5f7;

}

[data-testid="collapsedControl"] {
        display: none
    }

#MainMenu, header, footer {visibility: hidden;}

.bg {
  animation:slide 20s ease-in-out infinite alternate;
  background-image: linear-gradient(315deg, #aee1f9 0%, #f6ebe6 74%);
  bottom:0;
  left:-50%;
  opacity:.5;
  position:fixed;
  right:-50%;
  top:0;
  z-index:0;
}

.bg2 {
  animation-direction:alternate-reverse;
  animation-duration:15s;
}

.bg3 {
  animation-duration:17s;
}

@keyframes slide {
  0% {
    transform:translateX(-25%);
  }
  100% {
    transform:translateX(25%);
  }
}
</style>


<div class="bg"></div>
<div class="bg bg2"></div>
<div class="bg bg3"></div>
''',unsafe_allow_html=True)
#--------------------------------------------------
#credenciales de la base de datos
data,xta = get_credentials()
credentials = credentials_formating(data['records'])
#--------------------------------------------------
# Mensaje de bienvenida
sac.alert(message='Bienvenido al Sistema de Gestion y Analisis CECYTEM',
description='Si no tienes usuario y contraseña, contacta con el administrador.', banner=True, icon=True, closable=True, height=100)

cookie_manager = get_manager()

#--------------------------------------------------
# Banner principal de la pagina
cols1 = st.columns([.5,.5])
with cols1[0]:
    '### Colegio de Estudios Científicos y Tecnológicos del Estado de México'
    st.image("rsc/back1.jpg",use_column_width=True)
#--------------------------------------------------
# Formulario de inicio de sesion
with cols1[1]:
  #Cargamos el archivo de configuracion
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
  # Creamos el objeto de autenticacion
    authenticator = stauth.Authenticate(
        {'usernames':credentials},
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
  # Creamos el formulario de inicio de sesion
    authenticator.login('Login', 'main')
  # Si el usuario se ha autenticado correctamente, mostramos un mensaje de bienvenida y cambiamos de pagina a Home
    if st.session_state["authentication_status"] or cookie_manager.get('username') is not None:
        authenticator.logout('Logout', 'main', key='unique_key')
        st.toast(f'Bienvenido {st.session_state["name"]}',icon='🔓')
        cookie_manager.set('username', st.session_state['username'])
        switch_page('Inicio')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Por favor, introduce tu usuario y contraseña')

#--------------------------------------------------
# Pie de pagina
sac.tags([
    sac.Tag(label='Contacto', icon='person-lines-fill',
    color='cyan', link='https://ant.design/components/tag'),
    sac.Tag(label='Página Oficial CECYTEM', icon='mortarboard-fill',
    color='blue', link='https://cecytem.edomex.gob.mx/'),
    sac.Tag(label='Facebook', icon='facebook',
    color='geekblue', link='https://www.facebook.com/cecytem.edomex'),

], format_func='title', align='center',)

