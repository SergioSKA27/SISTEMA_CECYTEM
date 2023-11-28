import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import uuid

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import uuid
import time
import datetime


#Configuracion de la pagina
st.set_page_config(page_title="Registro de Alumno", page_icon=":clipboard:", layout="wide", initial_sidebar_state="collapsed")



st.markdown("""
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mosk:wght@400;700&display=swap">
<style>
    h1 {
      text-align: center;
      font-family: 'Mosk';
      color: #333;
      font-size: 5.5rem;
    }
</style>
    """, unsafe_allow_html=True)

#--------------------------------------------------
#Funciones

def get_credentials()->dict:
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
  return data

@st.cache_data
def credentials_formating(credentials: list[dict])->dict[str,dict[str,str]]:
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

def get_current_user_info(usrname: str) -> dict:
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


def reg_tutor(data,curpAlumno):
    """
    The function `reg_tutor` registers a new tutor in the database.

    :param data: The `data` parameter is a dictionary containing the information of the tutor to be registered.
    :return: The function `reg_tutor` returns the information of the tutor registered.
    """
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    iid  = xata.data().query("DataAlumno", {
    "columns": [
        "id",
        "curp",
        "id_tutorAlumno",
        "id_domicilioAlumno",
        "id_saludAlumno",
        "id_documentosAlumno",
        "id_procedenciaAlumno"
    ],
    "filter": {
        "curp": curpAlumno
    }
  })
    data = xata.records().update("TutorAlumno", iid['records'][0]['id_tutorAlumno']['id'],
    {
    "nombre": data['nombre'],
    "apellidoPaterno": data['apellidoPaterno'],
    "apellidoMaterno": data['apellidoMaterno'],
    "id_tutorAlumno": iid['records'][0]['id_tutorAlumno']['id'],
    "curp": data['curp'],
    })

    return data


#-------------------------------------------------
#Variables de Sesión
if 'curp' not in st.session_state:
    st.session_state.curp = ''

#--------------------------------------------------
#Verificación de ultimo registro
if "last_registered" not in st.session_state or "idcontrol" not in st.session_state.last_registered:
  switch_page("registroAlumno1")


#--------------------------------------------------
#Contenido de la página
st.title('Registro de Alumno')
st.divider()
st.subheader('Registro Datos Básicos del Tutor')
cols = st.columns([0.4,0.6])

with cols[0]:
  st.write("**Número de Control** :",st.session_state.last_registered['idcontrol'])
with cols[1]:
  st.write("**CURP** :",st.session_state.last_registered["curp"])

nombre_completo = st.text_input("Nombre(s)*",placeholder="Nombre(s)",help="Ingrese el nombre(s) del tutor")
cols2 = st.columns([0.5,0.5])

with cols2[0]:
    apellidop = st.text_input("Apellido Paterno*",placeholder="Apellido Paterno",help="Ingrese el apellido paterno del tutor")
with cols2[1]:
    apellidom = st.text_input("Apellido Materno*",placeholder="Apellido Materno",help="Ingrese el apellido materno del tutor")

crp = st.text_input("CURP*",placeholder="CURP",help="Ingrese el CURP del tutor",max_chars=18)
cols3 = st.columns([0.5,0.5])
with cols3[0]:
    telefono = st.text_input("Telefono*",placeholder="Telefono",help="Ingrese el telefono del tutor",max_chars=10)

with cols3[1]:
    celular = st.text_input("Celular",placeholder="Celular",help="Ingrese el celular del tutor",max_chars=10)


flag = False

butt = sac.buttons([
    sac.ButtonsItem(label='REGISTRAR',icon='cloud-haze2'),
], position='right', format_func='upper', align='center', size='large',
shape='round', return_index=True,index=1)



if butt == 0:
    data = {
        "nombre": nombre_completo.upper(),
        "apellidoPaterno": apellidop.upper().strip(),
        "apellidoMaterno": apellidom.upper().strip(),
        "curp": crp.upper().strip(),
        "telefono": telefono.strip(),
        "celular": celular.strip(),
    }
    with st.spinner('Registrando tutor...'):
      data = reg_tutor(data,st.session_state.last_registered['curp'])

    if 'message' in data:
        st.error('Error al registrar el tutor')
        st.error(data['message'])
    else:
        st.json(data)
        st.success('Tutor registrado con éxito')
        flag = True
        with st.spinner('Redireccionando...'):
          time.sleep(2)
          switch_page('documentacionAlumno')

if flag:

    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        subtitle='Datos Básicos',
        disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 2',subtitle='Datos Personales',
        description='Registra los datos personales del alumno',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 3',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso4',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso5',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso6',disabled=True,icon='person-bounding-box'),

        sac.StepsItem(title='Paso7',disabled=True,icon='file-earmark-text'),

        ], format_func='title',index=6)



else:
    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        description='Registro Básico',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 2',description='Datos Personales',disabled=True,icon='check2-square'),

       sac.StepsItem(title='Paso 3',disabled=True,icon='check2-square',
       description='Domicilio'),

        sac.StepsItem(title='Paso4',disabled=True,icon='check2-square',description='Salud'),

        sac.StepsItem(title='Paso5',disabled=True,icon='layer-backward',description='Procedencia'),

        sac.StepsItem(title='Paso6',disabled=True,icon='person-bounding-box',subtitle='Tutor',
        description='Registra los datos del tutor del alumno'),

        sac.StepsItem(title='Paso7',disabled=True,icon='file-earmark-text'),

        ], format_func='title',index=5)






