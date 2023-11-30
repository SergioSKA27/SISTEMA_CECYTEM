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
st.subheader('Registro Datos Básicos del Alumno')
cols = st.columns([0.4,0.6])

with cols[0]:
  st.write("**Número de Control** :",st.session_state.last_registered['idcontrol'])
with cols[1]:
  st.write("**CURP** :",st.session_state.last_registered["curp"])


if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  nombre = st.text_input("Nombre(s)*",placeholder="Nombre(s)",help="Ingrese el nombre del alumno",value=st.session_state.dataupdate['nombre'])
else:
  nombre = st.text_input("Nombre(s)*",placeholder="Nombre(s)",help="Ingrese el nombre del alumno")

cols2 = st.columns([0.5,0.5])

with cols2[0]:
  if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:

    apellidop = st.text_input("Apellido Paterno*",placeholder="Apellido Paterno",help="Ingrese el apellido paterno del alumno",value=st.session_state.dataupdate['apellidoPaterno'])
  else:
    apellidop = st.text_input("Apellido Paterno*",placeholder="Apellido Paterno",help="Ingrese el apellido paterno del alumno")

with cols2[1]:
  if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:

    apellidom = st.text_input("Apellido Materno*",placeholder="Apellido Materno",help="Ingrese el apellido materno del alumno",value=st.session_state.dataupdate['apellidoMaterno'])
  else:
    apellidom = st.text_input("Apellido Materno*",placeholder="Apellido Materno",help="Ingrese el apellido materno del alumno")

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  fecha_nacimiento = datetime.datetime.strptime(st.session_state.dataupdate['fechaNacimiento'],"%Y-%m-%dT%H:%M:%SZ").date()
  st.write("**Fecha de Nacimiento** :",fecha_nacimiento)
else:
  fecha_nacimiento = st.date_input("Fecha de Nacimiento*",help="Ingrese la fecha de nacimiento del alumno",min_value=datetime.date(1900, 1, 1))
  #st.write(type(datetime.datetime.combine(fecha_nacimiento, datetime.datetime.min.time())))


estados =  ["Aguascalientes",
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

estados = list(map(lambda x: x.upper(),estados))

if "update" in st.session_state.last_registered and st.session_state.last_registered['update'] and st.session_state.dataupdate['estadoNacimiento'] != "---":
  estado_nacimiento = st.selectbox("Estado de Nacimiento*",estados,help="Seleccione el estado de nacimiento del alumno",placeholder="Estado de México",index=estados.index(st.session_state.dataupdate['estadoNacimiento']) )
else:
  estado_nacimiento = st.selectbox("Estado de Nacimiento*",estados,help="Seleccione el estado de nacimiento del alumno",placeholder="Estado de México")

if "update" in st.session_state.last_registered and st.session_state.last_registered['update'] and st.session_state.dataupdate['nacionalidad'] != "---":
  nacionalidad = st.selectbox("Nacionalidad*",["MEXICANA","EXTRANJERA"],help="Seleccione la nacionalidad del alumno",placeholder="Mexicana/Extranjera",index=["MEXICANA","EXTRANJERA"].index(st.session_state.dataupdate['nacionalidad']))
else:
  nacionalidad = st.selectbox("Nacionalidad*",["MEXICANA","EXTRANJERA"],help="Seleccione la nacionalidad del alumno",placeholder="Mexicana/Extranjera")

if "update" in st.session_state.last_registered and st.session_state.last_registered['update'] and st.session_state.dataupdate['sexo'] != "---":
  sexo = st.selectbox("Sexo*",["MASCULINO","FEMENINO"],help="Seleccione el sexo del alumno",placeholder="Masculino/Femenino",index=["MASCULINO","FEMENINO"].index(st.session_state.dataupdate['sexo']))
else:
  sexo = st.selectbox("Sexo*",["Masculino","Femenino"],help="Seleccione el sexo del alumno")




if "update" in st.session_state.last_registered and st.session_state.last_registered['update'] and st.session_state.dataupdate['estadoCivil'] != "---":
  estado_civil = st.selectbox("Estado Civil*",["SOLTERO(A)","CASADO(A)","DIVORCIADO(A)","VIUDO(A)","UNIÓN LIBRE"],help="Seleccione el estado civil del alumno",placeholder="Soltero(a)/Casado(a)/Divorciado(a)/Viudo(a)/Unión Libre",index=["SOLTERO(A)","CASADO(A)","DIVORCIADO(A)","VIUDO(A)","UNIÓN LIBRE"].index(st.session_state.dataupdate['estadoCivil']))
else:
  estado_civil = st.selectbox("Estado Civil*",["SOLTERO(A)","CASADO(A)","DIVORCIADO(A)","VIUDO(A)","UNIÓN LIBRE"],help="Seleccione el estado civil del alumno",placeholder="Soltero(a)/Casado(a)/Divorciado(a)/Viudo(a)/Unión Libre")


#enfermedad = st.selectbox("¿Padece alguna enfermedad crónica?",["Si","No"],help="Seleccione si el alumno padece alguna enfermedad crónica",placeholder="Si/No",index=1)

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  telefono = st.text_input("Telefono*",placeholder="Telefono",help="Ingrese el telefono del tutor del alumno",max_chars=10,value=st.session_state.dataupdate['telefono'])
else:
  telefono = st.text_input("Telefono*",placeholder="Telefono",help="Ingrese el telefono del tutor del alumno",max_chars=10)

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  celular = st.text_input("Celular",placeholder="Celular",help="Ingrese el celular del tutor del alumno",max_chars=10,value=st.session_state.dataupdate['celular'])
else:
  celular = st.text_input("Celular",placeholder="Celular",help="Ingrese el celular del tutor del alumno",max_chars=10)

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  correo_personal = st.text_input("Correo Personal*",placeholder="Correo Personal",help="Ingrese el correo personal del alumno",value=st.session_state.dataupdate['correoe_p'])
else:
  correo_personal = st.text_input("Correo Personal*",placeholder="Correo Personal",help="Ingrese el correo personal del alumno")

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  correo_institucional = st.text_input("Correo Institucional*",placeholder="Correo Institucional",help="Ingrese el correo institucional del alumno",value=st.session_state.dataupdate['correoe_i'])
else:
  correo_institucional = st.text_input("Correo Institucional*",placeholder="Correo Institucional",help="Ingrese el correo institucional del alumno")

datar = {
'nombre': nombre.upper(),
'apellidoPaterno': apellidop.upper().strip(),
'apellidoMaterno': apellidom.upper().strip(),
'fechaNacimiento': datetime.datetime(
    fecha_nacimiento.year,
    fecha_nacimiento.month,
    fecha_nacimiento.day,
    0,0,0,3).strftime("%Y-%m-%dT%H:%M:%SZ"),
'estadoNacimiento': estado_nacimiento.upper(),
'sexo': sexo.upper(),
'nacionalidad': nacionalidad.upper(),
'estadoCivil': estado_civil.upper(),
'telefono': telefono.strip(),
'celular': celular.strip(),
'correoe_p': correo_personal.strip(),
'correoe_i': correo_institucional.strip(),
}
flag = False

butt = sac.buttons([
    sac.ButtonsItem(label='REGISTRAR',icon='cloud-haze2'),
], position='right', format_func='upper', align='center', size='large',
shape='round', return_index=True,index=1)



if butt == 0:
  with st.spinner("Registrando datos básicos del alumno..."):
    r = reg_basicdata(datar,st.session_state.last_registered["curp"])

  if "message" in r:
    st.error("Error al registrar los datos básicos del alumno")
    st.error(r["message"])
  else:
    st.success("Datos básicos del alumno registrados con éxito")
    st.json(r)
    flag = True
    if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
      switch_page("perfilAlumno")
    else:
      with st.spinner("Redireccionando a la siguiente página..."):
        time.sleep(3)
        switch_page("registroAlumno3")




if flag:

    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        subtitle='Datos Básicos',
        disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 2',subtitle='Datos Personales',
        description='Registra los datos personales del alumno',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 3',disabled=True,icon='pin-map'),

        sac.StepsItem(title='Paso4',disabled=True,icon='lungs'),

        sac.StepsItem(title='Paso5',disabled=True,icon='layer-backward'),

        sac.StepsItem(title='Paso6',disabled=True,icon='person-bounding-box'),

        sac.StepsItem(title='Paso7',disabled=True,icon='file-earmark-text'),

        ], format_func='title',index=2)



else:
    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        description='Datos Básicos',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 2',subtitle='Datos Personales',
        description='Registra los datos personales del alumno',disabled=False,icon='person-lines-fill'),

       sac.StepsItem(title='Paso 3',disabled=True,icon='pin-map'),

        sac.StepsItem(title='Paso4',disabled=True,icon='lungs'),

        sac.StepsItem(title='Paso5',disabled=True,icon='layer-backward'),

        sac.StepsItem(title='Paso6',disabled=True,icon='person-bounding-box'),

        sac.StepsItem(title='Paso7',disabled=True,icon='file-earmark-text'),

        ], format_func='title',index=1)





