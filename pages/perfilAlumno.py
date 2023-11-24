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
import datetime
#Esta es la pagina de inicio, donde se muestra el contenido de la pagina visible para todos los usuarios


#Configuracion de la pagina
st.set_page_config(page_title="Inicio", page_icon=":house:", layout="wide", initial_sidebar_state="collapsed")
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

@st.cache_data
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




def query_Alumno(record='NULL'):
    """
    The function `query_Alumnos` retrieves the information of all the students from a database.
    :return: The function `query_Alumnos` returns the information of all the students.
    """
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    ch = xata.records().get("Alumno",'rec_clfinfmsc66ps4cfg2bg')

    return ch

def query_dataAlumno(record):
    """
    The function `query_Alumnos` retrieves the information of all the students from a database.
    :return: The function `query_Alumnos` returns the information of all the students.
    """
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    ch = xata.records().get("DataAlumno",record)

    return ch
#-------



query = query_Alumno()




dtaAlumno = query_dataAlumno(query['curp']['id'])



#--------------------------------------------------

st.title('Perfil del Alumno')

st.divider()

st.subheader("Datos de Control")
cols0 = st.columns([0.5,0.5])

with cols0[0]:
    st.write("**Numero de Control:** ",query['idcontrol'])

with cols0[1]:
    st.write("**CURP:** ",dtaAlumno['curp'])


st.write("**Plantel:** ",query['plantelAlumno'])
st.write("**Carrera:** ",query['carreraAlumno'])

st.divider()

st.subheader("Datos Generales del Alumno")

st.write("**Nombre:** ",dtaAlumno['nombre'])
st.write("**Apellido Paterno:** ",dtaAlumno['apellidoPaterno'])
st.write("**Apellido Materno:** ",dtaAlumno['apellidoMaterno'])

cols1 = st.columns([0.5,0.5])
with cols1[0]:
    st.write("**Fecha de Nacimiento:** ",dtaAlumno['fechaNacimiento'][:10])
with cols1[1]:
    st.write("**Estado de Nacimiento:** ",dtaAlumno['estadoNacimiento'])

cols2 = st.columns([0.5,0.5])

with cols2[0]:
    st.write("**Sexo:** ",dtaAlumno['sexo'])

with cols2[1]:
    st.write("**Nacionalidad:** ",dtaAlumno['nacionalidad'])

st.write("**Estado Civil:** ",dtaAlumno['estadoCivil'])
st.write("**Telefono:** ",dtaAlumno['telefono'])
st.write("**Celular:** ",dtaAlumno['celular'])
st.write("**Correo Personal:** ",dtaAlumno['correoe_p'])
st.write("**Correo Institucional:** ",dtaAlumno['correoe_i'])



if st.checkbox("raw data"):
    st.write(query)
    st.write(dtaAlumno)
