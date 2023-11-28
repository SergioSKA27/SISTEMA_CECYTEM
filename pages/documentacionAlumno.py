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
import base64
import urllib


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

    data = xata.records().update("DocumentacionAlumno", iid['records'][0]['id_documentosAlumno']['id'],{
    "acta_nacimientoAlumno": {
        "base64Content": "SGVsbG8gV29ybGQ=",
        "enablePublicUrl": False,
        "mediaType": "application/octet-stream",
        "name": "upload.txt",
        "signedUrlTimeout": 300
    },
    "certificado_secundariaAlumno": {
        "base64Content": "SGVsbG8gV29ybGQ=",
        "enablePublicUrl": False,
        "mediaType": "application/octet-stream",
        "name": "upload.txt",
        "signedUrlTimeout": 300
    },
    "comprobante_domAlumno": {
        "base64Content": "SGVsbG8gV29ybGQ=",
        "enablePublicUrl": False,
        "mediaType": "application/octet-stream",
        "name": "upload.txt",
        "signedUrlTimeout": 300
    },
    "certificado_saludAlumno": {
        "base64Content": "SGVsbG8gV29ybGQ=",
        "enablePublicUrl": False,
        "mediaType": "application/octet-stream",
        "name": "upload.txt",
        "signedUrlTimeout": 300
    },
    "fotos_Alumno": [
        {
            "base64Content": "SGVsbG8gV29ybGQ=",
            "enablePublicUrl": False,
            "mediaType": "application/octet-stream",
            "name": "upload.txt",
            "signedUrlTimeout": 300
        }
    ],
    "solicitud_inscAlumno": {
        "base64Content": "SGVsbG8gV29ybGQ=",
        "enablePublicUrl": False,
        "mediaType": "application/octet-stream",
        "name": "upload.txt",
        "signedUrlTimeout": 300
    },
    "recibo_preinscAlumno": {
        "base64Content": "SGVsbG8gV29ybGQ=",
        "enablePublicUrl": False,
        "mediaType": "application/octet-stream",
        "name": "upload.txt",
        "signedUrlTimeout": 300
    },
    "recibo_inscAlumno": {
        "base64Content": "SGVsbG8gV29ybGQ=",
        "enablePublicUrl": False,
        "mediaType": "application/octet-stream",
        "name": "upload.txt",
        "signedUrlTimeout": 300
    },
    "ine_tutorAlumno": {
        "base64Content": "SGVsbG8gV29ybGQ=",
        "enablePublicUrl": False,
        "mediaType": "application/octet-stream",
        "name": "upload.txt",
        "signedUrlTimeout": 300
    },
    "carta_constAlumno": {
        "base64Content": "SGVsbG8gV29ybGQ=",
        "enablePublicUrl": False,
        "mediaType": "application/octet-stream",
        "name": "upload.txt",
        "signedUrlTimeout": 300
    },
    "id_documentosAlumno": "string"
})



#--------------------------------------------------
#Verificación de ultimo registro
if "last_registered" not in st.session_state or "idcontrol" not in st.session_state.last_registered:
  switch_page("registroAlumno1")




#--------------------------------------------------
#Contenido de la página
st.title('Registro de Alumno')
st.divider()
st.subheader('Registro Documentación del Alumno')
cols = st.columns([0.4,0.6])

with cols[0]:
  st.write("Número de Control :",st.session_state.last_registered['idcontrol'])
with cols[1]:
  st.write("CURP :",st.session_state.last_registered["curp"])


st.divider()


st.write("Ingresa el acta de nacimiento del alumno")
formatacta = st.selectbox("Formato de acta de nacimiento",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")
acta_nacimiento = st.file_uploader("Acta de Nacimiento",type=['pdf','png','jpg','jpeg'])



if formatacta == 'pdf' and acta_nacimiento is not None:
    try:
        acta_nacimientoAlumno = acta_nacimiento.read()
        acta_nacimientoAlumno = base64.b64encode(acta_nacimientoAlumno).decode('utf-8')
        acta_nacimientoAlumno = f"data:application/pdf;base64,{acta_nacimientoAlumno}"
        pdf_display = f'<iframe  src="{acta_nacimientoAlumno}" width="700" height="600" type="application/pdf"></iframe>'
        st.write('Preview del archivo pdf:')
        st.markdown(pdf_display, unsafe_allow_html=True)
    except:
        st.error("El archivo no es un pdf o está dañado")

st.write("Ingresa el certificado de secundaria del alumno")
formatacertificadoSec = st.selectbox("Formato de certificado de secundaria",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")
filecertificado_secundariaAlumno = st.file_uploader("Certificado de Secundaria",type=['pdf','png','jpg','jpeg'])
