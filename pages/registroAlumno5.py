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
import requests

#Configuracion de la pagina
st.set_page_config(page_title="Registro de Alumno", page_icon=":clipboard:", layout="wide", initial_sidebar_state="collapsed")

#Configuracion de la pagina
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
    }
</style>
""",unsafe_allow_html=True)




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

def reg_procedenciaAlumno(reg_data,curpAlumno):
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


    data = xata.records().update("ProcedenciaAlumno",iid['records'][0]['id_procedenciaAlumno']['id'] ,
    {
    "claveCeneval": reg_data['claveCeneval'],
    "puntajeIngreso": reg_data['puntajeIngreso'],
    "secundariaProcedencia": reg_data['secundariaProcedencia'],
    "estanciaSecundaria_years": reg_data['estanciaSecundaria_years'],
    "promedioSecundaria": reg_data['promedioSecundaria'],
    "intentosAceptacion": reg_data['intentosAceptacion'],
    "id_procedenciaAlumno": iid['records'][0]['id_procedenciaAlumno']['id']
    })

    return data




#--------------------------------------------------
#Verificación de ultimo registro
if "last_registered" not in st.session_state or "idcontrol" not in st.session_state.last_registered:
  switch_page("registroAlumno1")




#--------------------------------------------------
#Contenido de la página
if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  backpp = sac.buttons([
                    sac.ButtonsItem(label='REGRESAR',icon='skip-backward-btn'),
                ], position='left', format_func='upper', align='center', size='large',
                shape='round', return_index=True,index=1)

  if backpp == 0:
    st.session_state.last_registered['update'] = False
    st.session_state.dataupdate = {}
    switch_page('perfilAlumno')

else:
  indexb = 1
  backpp = sac.buttons([
      sac.ButtonsItem(label='DETENER REGISTRO',
      icon='sign-stop'),
  ], position='left', format_func='upper', align='center', size='large',
  shape='round', return_index=True,index=indexb)

  if backpp == 0:
    st.write("Los datos registrados hasta el momento no se perderán, y podrán ser modificados en cualquier momento, en el perfil del alumno.")
    st.write("¿Desea detener el registro del alumno?")
    opc = st.radio("Seleccione una opción",["Si","No"],index=1)

    if opc == "Si":
      switch_page('AlumnosHome')
    else:
      indexb = 1


st.title('Registro de Alumno')
st.divider()
st.subheader('Registro Procedencia del Alumno')
cols = st.columns([0.4,0.6])

with cols[0]:
  st.write("**Número de Control** :",st.session_state.last_registered['idcontrol'])
with cols[1]:
  st.write("**CURP** :",st.session_state.last_registered["curp"])


st.divider()



if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  claveCeneval = st.text_input("Clave Ceneval",help="Ingrese la clave Ceneval del alumno", placeholder="ej. 123456789",value=st.session_state.dataupdate['claveCeneval'])
else:
  claveCeneval = st.text_input("Clave Ceneval",help="Ingrese la clave Ceneval del alumno", placeholder="ej. 123456789")

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  puntajeIngreso = st.number_input("Puntaje de Ingreso",help="Ingrese el puntaje de ingreso del alumno", placeholder="ej. 100",min_value=0,max_value=200,value=st.session_state.dataupdate['puntajeIngreso'])
else:
  puntajeIngreso = st.number_input("Puntaje de Ingreso",help="Ingrese el puntaje de ingreso del alumno", placeholder="ej. 100",min_value=0,max_value=200)

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  secundariaProcedencia = st.text_input("Secundaria de Procedencia",help="Ingrese la secundaria de procedencia del alumno", placeholder="ej. Secundaria 1",value=st.session_state.dataupdate['secundariaProcedencia'])
else:
  secundariaProcedencia = st.text_input("Secundaria de Procedencia",help="Ingrese la secundaria de procedencia del alumno", placeholder="ej. Secundaria 1")

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  estaciaSecundaria_years = st.number_input("Años de Estancia en Secundaria",help="Ingrese los años de estancia en secundaria del alumno", placeholder="ej. 3",min_value=0,max_value=10,value=st.session_state.dataupdate['estanciaSecundaria_years'])
else:
  estaciaSecundaria_years = st.number_input("Años de Estancia en Secundaria",help="Ingrese los años de estancia en secundaria del alumno", placeholder="ej. 3",min_value=0,max_value=10)

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  promedioSecundaria = st.number_input("Promedio de Secundaria",help="Ingrese el promedio de secundaria del alumno", placeholder="ej. 9.5",min_value=5,max_value=10,value=st.session_state.dataupdate['promedioSecundaria'],step=1)
else:
  promedioSecundaria = st.number_input("Promedio de Secundaria",help="Ingrese el promedio de secundaria del alumno", placeholder="ej. 9.5",min_value=5.0,max_value=10.0)



if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  intentosAceptacion = st.number_input("Intentos de Aceptación",help="Ingrese los intentos de aceptación del alumno", placeholder="ej. 1",min_value=0,max_value=10,value=st.session_state.dataupdate['intentosAceptacion'])
else:
  intentosAceptacion = st.number_input("Intentos de Aceptación",help="Ingrese los intentos de aceptación del alumno", placeholder="ej. 1",min_value=0,max_value=10)


data_reg = {'claveCeneval': claveCeneval,
'puntajeIngreso': puntajeIngreso,
'secundariaProcedencia': secundariaProcedencia.upper(),
'estanciaSecundaria_years': estaciaSecundaria_years,
'promedioSecundaria': promedioSecundaria,
'intentosAceptacion': intentosAceptacion}


flag = False

regi = 1
butt = sac.buttons([
    sac.ButtonsItem(label='REGISTRAR',icon='cloud-haze2'),
], position='right', format_func='upper', align='center', size='large',
shape='round', return_index=True,index=regi)



if butt == 0:
  with st.spinner("Registrando datos de procedencia del alumno... 🌐"):
    dr = reg_procedenciaAlumno(data_reg,st.session_state.last_registered['curp'])

    if 'message' in dr:
      st.error('Error al registrar los datos de procedencia del alumno 😥')
      st.error(dr['message'])
    else:
        st.success('Datos de procedencia del alumno registrados con éxito 😄')
        flag = True
        st.json(dr)
        if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
          st.session_state.last_registered['update'] = False
          st.session_state.dataupdate = {}
          switch_page('perfilAlumno')
        else:
          with st.spinner("Redireccionando..."):
            time.sleep(5)
            switch_page("registro_tutor")



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

        ], format_func='title',index=5)



else:
    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        description='Registro Básico',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 2',description='Datos Personales',disabled=True,icon='check2-square'),

       sac.StepsItem(title='Paso 3',disabled=True,icon='check2-square',
       description='Domicilio'),

        sac.StepsItem(title='Paso4',disabled=True,icon='check2-square',description='Salud'),

        sac.StepsItem(title='Paso5',disabled=False,icon='layer-backward',subtitle='Procedencia',
        description='Registra los datos de procedencia del alumno'),

        sac.StepsItem(title='Paso6',disabled=True,icon='person-bounding-box'),

        sac.StepsItem(title='Paso7',disabled=True,icon='file-earmark-text'),

        ], format_func='title',index=4)






