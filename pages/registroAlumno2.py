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

def reg_basicdata(reg_data: dict, curp: str)->dict:
  """
  The `reg_basicdata` function updates the basic data of a student in a database using their CURP (Unique Population
  Registry Code).

  :param reg_data: The `reg_data` parameter is a dictionary that contains the basic data of a student. It includes the
  following keys:
  :type reg_data: dict
  :param curp: The parameter "curp" is a string that represents the CURP (Clave Única de Registro de Población) of a
  person. CURP is a unique identification number assigned to each Mexican citizen and residents
  :type curp: str
  :return: the updated data of the student with the specified CURP (Clave Única de Registro de Población).
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
        "curp": curp
    }
  })
  data = xata.records().update("DataAlumno", iid['records'][0]['id'],{
    "nombre": reg_data["nombre"],
    "apellidoPaterno": reg_data["apellidoPaterno"],
    "apellidoMaterno": reg_data["apellidoMaterno"],
    "fechaNacimiento": reg_data["fechaNacimiento"],
    "estadoNacimiento": reg_data["estadoNacimiento"],
    "sexo": reg_data["sexo"],
    "nacionalidad": reg_data["nacionalidad"],
    "estadoCivil": reg_data["estadoCivil"],
    "telefono": reg_data["telefono"],
    "celular": reg_data["celular"],
    "correoe_p": reg_data["correoe_p"],
    "correoe_i": reg_data["correoe_i"],
    "curp": curp,
    "id_tutorAlumno": iid['records'][0]['id_tutorAlumno']['id'],
    "id_domicilioAlumno": iid['records'][0]['id_domicilioAlumno']['id'],
    "id_saludAlumno": iid['records'][0]['id_saludAlumno']['id'],
    "id_documentosAlumno": iid['records'][0]['id_documentosAlumno']['id'],
    "id_procedenciaAlumno": iid['records'][0]['id_procedenciaAlumno']['id']
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
st.subheader('Registro Datos Básicos del Alumno')
cols = st.columns([0.4,0.6])

with cols[0]:
  st.write("Número de Control :",st.session_state.last_registered['idcontrol'])
with cols[1]:
  st.write("CURP :",st.session_state.last_registered["curp"])



nombre = st.text_input("Nombre(s)*",placeholder="Nombre(s)",help="Ingrese el nombre del alumno")

cols2 = st.columns([0.5,0.5])

with cols2[0]:
  apellidop = st.text_input("Apellido Paterno*",placeholder="Apellido Paterno",help="Ingrese el apellido paterno del alumno")
with cols2[1]:
  apellidom = st.text_input("Apellido Materno*",placeholder="Apellido Materno",help="Ingrese el apellido materno del alumno")

fecha_nacimiento = st.date_input("Fecha de Nacimiento*",help="Ingrese la fecha de nacimiento del alumno",min_value=datetime.date(1900, 1, 1))
  #st.write(type(datetime.datetime.combine(fecha_nacimiento, datetime.datetime.min.time())))

estado_nacimiento = st.selectbox("Estado de Nacimiento*",
  ["Aguascalientes",
  "Baja California",
  "Baja California Sur",
  "Campeche","Chiapas",
  "Chihuahua",
  "Ciudad de México",
  "Coahuila",
  "Colima",
  "Durango",
  "Estado de México",
  "Guanajuato",
  "Guerrero",
  "Hidalgo",
  "Jalisco",
  "Michoacán",
  "Morelos",
  "Nayarit",
  "Nuevo León",
  "Oaxaca",
  "Puebla",
  "Querétaro",
  "Quintana Roo",
  "San Luis Potosí",
  "Sinaloa",
  "Sonora",
  "Tabasco",
  "Tamaulipas",
  "Tlaxcala",
  "Veracruz",
  "Yucatán",
  "Zacatecas",
  "Otro"]
  ,help="Seleccione el estado de nacimiento del alumno",placeholder="Estado de México",index=10)

nacionalidad = st.selectbox("Nacionalidad*",["Mexicana","Extranjera"],help="Seleccione la nacionalidad del alumno",placeholder="Mexicana/Extranjera")

sexo = st.selectbox("Sexo*",["Masculino","Femenino"],help="Seleccione el sexo del alumno")

estado_civil = st.selectbox("Estado Civil*",["Soltero(a)","Casado(a)","Divorciado(a)","Viudo(a)","Unión Libre"],help="Seleccione el estado civil del alumno")


#enfermedad = st.selectbox("¿Padece alguna enfermedad crónica?",["Si","No"],help="Seleccione si el alumno padece alguna enfermedad crónica",placeholder="Si/No",index=1)

telefono = st.text_input("Telefono*",placeholder="Telefono",help="Ingrese el telefono del tutor del alumno")

celular = st.text_input("Celular",placeholder="Celular",help="Ingrese el celular del tutor del alumno")

correo_personal = st.text_input("Correo Personal*",placeholder="Correo Personal",help="Ingrese el correo personal del alumno")

correo_institucional = st.text_input("Correo Institucional*",placeholder="Correo Institucional",help="Ingrese el correo institucional del alumno")


datar = {
'nombre': nombre,
'apellidoPaterno': apellidop,
'apellidoMaterno': apellidom,
'fechaNacimiento': datetime.datetime(
    fecha_nacimiento.year,
    fecha_nacimiento.month,
    fecha_nacimiento.day,
    0,0,0,3).strftime("%Y-%m-%dT%H:%M:%SZ"),
'estadoNacimiento': estado_nacimiento,
'sexo': sexo,
'nacionalidad': nacionalidad,
'estadoCivil': estado_civil,
'telefono': telefono,
'celular': celular,
'correoe_p': correo_personal,
'correoe_i': correo_institucional
}
flag = False

if st.button("Registrar"):
  with st.spinner("Registrando datos básicos del alumno..."):
    r = reg_basicdata(datar,st.session_state.last_registered["curp"])

  if "message" in r:
    st.error("Error al registrar los datos básicos del alumno")
    st.error(r["message"])
  else:
    st.success("Datos básicos del alumno registrados con éxito")
    st.json(r)
    flag = True

    time.sleep(5)
    switch_page("registroAlumno3")




if flag:

    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        subtitle='Registro Básico',
        description='Registra los datos básicos del alumno',
        disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 2',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 3'),

        sac.StepsItem(title='Paso4'),

        ], format_func='title',index=2)

    #time.sleep(5)
    switch_page("registro_tutor")



else:
    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        subtitle='Registro Básico',
        description='Registra los datos básicos del alumno',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 2'),

        sac.StepsItem(title='Paso 3'),

        sac.StepsItem(title='Paso4',),

        ], format_func='title',index=1)





