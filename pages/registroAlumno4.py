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
st.title('Registro de Alumno')
st.divider()
st.subheader('Registro Salud del Alumno')
cols = st.columns([0.4,0.6])

with cols[0]:
  st.write("**Número de Control** :",st.session_state.last_registered['idcontrol'])
with cols[1]:
  st.write("**CURP** :",st.session_state.last_registered["curp"])


st.divider()



salud_status = st.selectbox("¿El alumno tiene alguna enfermedad?",("Si","No"),index=1,help="Selecciona una opción")

if salud_status == 'Si':
    enfermedad_desc = st.text_area("Descripción de la enfermedad",help="Escribe la descripción de la enfermedad")

    padecimientos = st.text_area("Padecimientos",help="Escribe los padecimientos del alumno separados por comas")

    medicamentos = st.text_area("Medicamentos",help="Escribe los medicamentos del alumno separados por comas")

    impedimentos = st.text_area("Impedimentos",help="Escribe los impedimentos del alumno separados por comas")

else:
    enfermedad_desc = 'NONE'
    padecimientos = 'NONE'
    medicamentos = 'NONE'
    impedimentos = 'NONE'

tipo_sangre = st.selectbox("Tipo de sangre",("A+","A-","B+","B-","AB+","AB-","O+","O-"),index=0,help="Selecciona el tipo de sangre del alumno")



opcional_desc = st.text_area("Descripción opcional",help="Escribe una descripción opcional")



if salud_status == 'No':
    sttatus = False
    st.write("No se requiere información adicional")
else:
    sttatus = True

data_reg = {
'salud_status': sttatus,
'enfermedad_desc': enfermedad_desc.upper(),
'padecimientos': padecimientos.strip().split(','),
'medicamentos': medicamentos.strip().split(','),
'impedimentos': impedimentos.split(','),
'tipo_sangre': tipo_sangre,
'opcional_desc': opcional_desc
}


flag = False


butt = sac.buttons([
    sac.ButtonsItem(label='REGISTRAR',icon='cloud-haze2'),
], position='right', format_func='upper', align='center', size='large',
shape='round', return_index=True,index=1)


if butt == 0:
    with st.spinner("Registrando datos de salud del alumno..."):
        dr = reg_saludAlumno(data_reg,st.session_state.last_registered['curp'])

    if "message" in dr:
        st.error("Error al registrar los datos de salud del alumno")
        st.error(dr['message'])
    else:
        st.success("Datos de salud del alumno registrados exitosamente")
        st.json(dr)
        flag = True
        time.sleep(5)
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





