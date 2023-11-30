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

def reg_saludAlumno(reg_data,curpAlumno):
    """
    The function `reg_saludAlumno` updates the health information of a student in a database using their CURP (Unique
    Population Registry Code).

    :param reg_data: The `reg_data` parameter is a dictionary that contains the updated health information of the student.
    It includes the following keys:
    :param curpAlumno: The curpAlumno parameter is the CURP (Clave Única de Registro de Población) of the student. It is a
    unique identifier for individuals in Mexico
    :return: the updated data of the "SaludAlumno" record.
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

    data = xata.records().update("SaludAlumno",iid['records'][0]['id_saludAlumno']['id'] ,
    {
        "salud_status": reg_data['salud_status'],
        "enfermedad_desc": reg_data['enfermedad_desc'],
        "padecimientos": reg_data['padecimientos'],
        "medicamentos": reg_data['medicamentos'],
        "tipo_sangre": reg_data['tipo_sangre'],
        "opcional_desc": reg_data['opcional_desc'],
        "id_saludAlumno": iid['records'][0]['id_saludAlumno']['id'],
        "impedimentos": reg_data['impedimentos'],
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
st.subheader('Registro Salud del Alumno')
cols = st.columns([0.4,0.6])
#--
with cols[0]:
  st.write("**Número de Control** :",st.session_state.last_registered['idcontrol'])
with cols[1]:
  st.write("**CURP** :",st.session_state.last_registered["curp"])


st.divider()


if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
    salud_status = st.selectbox("¿El alumno tiene alguna enfermedad?",("Si","No"),help="Selecciona una opción",index=[True,False].index(st.session_state.dataupdate['salud_status']))
else:
    salud_status = st.selectbox("¿El alumno tiene alguna enfermedad?",("Si","No"),index=1,help="Selecciona una opción")


if salud_status == 'Si':
    if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
        enfermedad_desc = st.text_area("Descripción de la enfermedad",help="Escribe la descripción de la enfermedad",value=st.session_state.dataupdate['enfermedad_desc'])
    else:
        enfermedad_desc = st.text_area("Descripción de la enfermedad",help="Escribe la descripción de la enfermedad")

    if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
        padecimientos = st.text_area("Padecimientos",help="Escribe los padecimientos del alumno separados por comas",value=','.join(st.session_state.dataupdate['padecimientos']))
    else:
        padecimientos = st.text_area("Padecimientos",help="Escribe los padecimientos del alumno separados por comas")

    if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
        medicamentos = st.text_area("Medicamentos",help="Escribe los medicamentos del alumno separados por comas",value=','.join(st.session_state.dataupdate['medicamentos']))
    else:
        medicamentos = st.text_area("Medicamentos",help="Escribe los medicamentos del alumno separados por comas")

    if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
        impedimentos = st.text_area("Impedimentos",help="Escribe los impedimentos del alumno separados por comas",value=','.join(st.session_state.dataupdate['impedimentos']))

else:
    enfermedad_desc = 'NONE'
    padecimientos = 'NONE'
    medicamentos = 'NONE'
    impedimentos = 'NONE'

if "update" in st.session_state.last_registered and st.session_state.last_registered['update'] and st.session_state.dataupdate['tipo_sangre'] != '---':
    tipo_sangre = st.selectbox("Tipo de sangre",("A+","A-","B+","B-","AB+","AB-","O+","O-"),help="Selecciona el tipo de sangre del alumno",
    index=["A+","A-","B+","B-","AB+","AB-","O+","O-"].index(st.session_state.dataupdate['tipo_sangre']))
else:
    tipo_sangre = st.selectbox("Tipo de sangre",("A+","A-","B+","B-","AB+","AB-","O+","O-"),index=0,help="Selecciona el tipo de sangre del alumno")

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
    opcional_desc = st.text_area("Descripción opcional",help="Escribe una descripción opcional",value=st.session_state.dataupdate['opcional_desc'])
else:
    opcional_desc = st.text_area("Descripción opcional",help="Escribe una descripción opcional")


if salud_status == 'No':
    sttatus = False
    st.write("No se requiere información adicional")
else:
    sttatus = True

data_reg = {
'salud_status': sttatus,
'enfermedad_desc': enfermedad_desc.upper(),
'padecimientos': padecimientos.upper().split(','),
'medicamentos': medicamentos.upper().split(','),
'impedimentos': impedimentos.upper().split(','),
'tipo_sangre': tipo_sangre,
'opcional_desc': opcional_desc
}


flag = False


regi = 1
butt = sac.buttons([
    sac.ButtonsItem(label='REGISTRAR',icon='cloud-haze2'),
], position='right', format_func='upper', align='center', size='large',
shape='round', return_index=True,index=regi)


if butt == 0:
    with st.spinner("Registrando datos de salud del alumno... 🌐"):
        dr = reg_saludAlumno(data_reg,st.session_state.last_registered['curp'])

    if "message" in dr:
        st.error("Error al registrar los datos de salud del alumno 😥")
        st.error(dr['message'])
    else:
        st.success("Datos de salud del alumno registrados exitosamente 😄")
        st.json(dr)
        if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
            st.session_state.last_registered['update'] = False
            st.session_state.dataupdate = {}
            switch_page('perfilAlumno')
        else:
            flag = True
            with st.spinner("Redireccionando... "):
                time.sleep(2)
                switch_page("registroAlumno5")




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

        sac.StepsItem(title='Paso5',disabled=True,icon='layer-backward'),

        sac.StepsItem(title='Paso6',disabled=True,icon='person-bounding-box'),

        sac.StepsItem(title='Paso7',disabled=True,icon='file-earmark-text'),

        ], format_func='title',index=4)



else:
    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        description='Registro Básico',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 2',description='Datos Personales',disabled=True,icon='check2-square'),

       sac.StepsItem(title='Paso 3',disabled=True,icon='check2-square',
       description='Domicilio'),

        sac.StepsItem(title='Paso4',disabled=False,icon='lungs',subtitle='Salud',
        description='Registra los datos de salud del alumno'),

        sac.StepsItem(title='Paso5',disabled=True,icon='layer-backward'),

        sac.StepsItem(title='Paso6',disabled=True,icon='person-bounding-box'),

        sac.StepsItem(title='Paso7',disabled=True,icon='file-earmark-text'),

        ], format_func='title',index=3)





