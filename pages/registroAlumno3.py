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
from geopy.geocoders import Nominatim,Bing
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl


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


def reg_domicilio(reg_data,curpAlumno):
    """
    The function `reg_domicilio` registers the address of a student in a database.

    :param reg_data: The `reg_data` parameter is a dictionary that contains the address of a student. It includes the
    following keys:
    :type reg_data: dict
    :return: The function `reg_domicilio` returns the information of the address registered.
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
        "id_procedenciaAlumno",
        "estatus",
        "seguro"
    ],
    "filter": {
        "curp.curp": curpAlumno
    }
  })
    data = xata.records().update("DomicilioAlumno",iid['records'][0]['id_domicilioAlumno']['id'], {
    "calle": reg_data['calle'],
    "num_int": reg_data['num_int'],
    "num_ext": reg_data['num_ext'],
    "colonia": reg_data['colonia'],
    "codigoP": reg_data['codigoP'],
    "localidad": reg_data['localidad'],
    "municipio": reg_data['municipio'],
    "estado": reg_data['estado'],
    "calle_ref1": reg_data['calle_ref1'],
    "calle_ref2": reg_data['calle_ref2'],
    "opcional_ref": reg_data['opcional_ref'],
    "id_domicilioAlumno": iid['records'][0]['id_domicilioAlumno']['id'],
    })


    return data

def formatear_direccion(direccion):
    # Reemplaza los espacios en blanco con el símbolo '+' para la URL
    direccion_formateada = '+'.join(direccion.split())

    # URL de la API de geocodificación de Google Maps
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={direccion_formateada}?sensor=false'

    return url




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
st.subheader('Registro Domicilio del Alumno')
cols = st.columns([0.4,0.6])

with cols[0]:
  st.write("**Número de Control** :",st.session_state.last_registered['idcontrol'])
with cols[1]:
  st.write("**CURP** :",st.session_state.last_registered["curp"])



if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  calle = st.text_input("Calle*",help="Ingrese el nombre de la calle",placeholder="Ej. Av. 20 de Noviembre",value=st.session_state.dataupdate['calle'])
else:
  calle = st.text_input("Calle*",help="Ingrese el nombre de la calle",placeholder="Ej. Av. 20 de Noviembre")
cols = st.columns([0.6,0.4])

with cols[0]:
  if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
    num_ext = st.number_input("Número Exterior*",help="Ingrese el número exterior",min_value=0,value=st.session_state.dataupdate['num_ext'])
  else:
    num_ext = st.number_input("Número Exterior*",help="Ingrese el número exterior",placeholder="Ej. 123",min_value=0)
with cols[1]:
  if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
    num_int = st.number_input("Número Interior",help="Ingrese el número interior",min_value=0,value=st.session_state.dataupdate['num_int'])
  else:
    num_int = st.number_input("Número Interior",help="Ingrese el número interior",placeholder="Ej. 123",min_value=0)

cols = st.columns([0.6,0.4])

with cols[0]:
  if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
    colonia = st.text_input("Colonia*",help="Ingrese el nombre de la colonia",value=st.session_state.dataupdate['colonia'])
  else:
    colonia = st.text_input("Colonia*",help="Ingrese el nombre de la colonia",placeholder="Ej. Centro")
with cols[1]:
  if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
    codigoP = st.text_input("Código Postal*",help="Ingrese el código postal",value=st.session_state.dataupdate['codigoP'])
  else:
    codigoP = st.text_input("Código Postal*",help="Ingrese el código postal",placeholder="Ej. 39000")

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  localidad = st.text_input("Localidad",help="Ingrese el nombre de la localidad",placeholder="Ej. Centro",value=st.session_state.dataupdate['localidad'])
else:
  localidad = st.text_input("Localidad",help="Ingrese el nombre de la localidad",placeholder="Ej. Centro")

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  mun = st.text_input("Municipio*",help="Ingrese el nombre del municipio",placeholder="Ej. Chilpancingo de los Bravo",value=st.session_state.dataupdate['municipio'])
else:
  mun = st.text_input("Municipio*",help="Ingrese el nombre del municipio",placeholder="Ej. Chilpancingo de los Bravo")




estados = [
"Aguascalientes",
"Baja California",
"Baja California Sur",
"Campeche","Chiapas",
"Chihuahua",
"Ciudad de México",
"Coahuila","Colima",
"Durango",
"Estado de México",
"Guanajuato",
"Guerrero","Hidalgo",
"Jalisco","Michoacán",
"Morelos","Nayarit",
"Nuevo León","Oaxaca",
"Puebla","Querétaro",
"Quintana Roo",
"San Luis Potosí",
"Sinaloa","Sonora",
"Tabasco","Tamaulipas",
"Tlaxcala","Veracruz",
"Yucatán","Zacatecas"]

estados = [estado.upper() for estado in estados]
if "update" in st.session_state.last_registered and st.session_state.last_registered['update'] and st.session_state.dataupdate['estado'] != "---":
  estado = st.selectbox("Estado",options=estados,help="Seleccione el estado",index=estados.index(st.session_state.dataupdate['estado']))
else:
  estado = st.selectbox("Estado",options=estados,help="Seleccione el estado",index=10)

direccion = f'{calle},{localidad},{codigoP},{mun},{estado}'

try:
    #geolocator = Nominatim(user_agent="RegistroAlumno")
    geolocator = Bing(api_key=st.secrets['db']['bing'])
    location = geolocator.geocode(direccion,include_neighborhood=True)
    st.write(location.address)
    st.write((location.latitude, location.longitude))

    config = {
    "version": "v1",
    "config": {
        "mapState": {
            "bearing": 0,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "pitch": 0,
            "zoom": len(location.address.split(","))*4.5,
        },

    },
}
    map_1 = KeplerGl(theme="light")
    map_1.config = config

    keplergl_static(map_1)
except:
    st.write("No se pudo obtener la ubicación")


if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  calleref1 = st.text_input("Calle de Referencia 1",help="Ingrese el nombre de la calle de referencia 1",placeholder="Ej. Av. 20 de Noviembre",value=st.session_state.dataupdate['calle_ref1'])
else:
  calleref1 = st.text_input("Calle de Referencia 1",help="Ingrese el nombre de la calle de referencia 1",placeholder="Ej. Av. 20 de Noviembre")

if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  calleref2 = st.text_input("Calle de Referencia 2",help="Ingrese el nombre de la calle de referencia 2",placeholder="Ej. Av. 20 de Noviembre",value=st.session_state.dataupdate['calle_ref2'])
else:
  calleref2 = st.text_input("Calle de Referencia 2",help="Ingrese el nombre de la calle de referencia 2",placeholder="Ej. Av. 20 de Noviembre")


if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
  referecia_ad = st.text_area("Referencia Adicional",help="Ingrese una referencia adicional",placeholder="Ej. Entre las calles 20 de Noviembre y 5 de Mayo",value=st.session_state.dataupdate['opcional_ref'])
else:
  referecia_ad = st.text_area("Referencia Adicional",help="Ingrese una referencia adicional",placeholder="Ej. Entre las calles 20 de Noviembre y 5 de Mayo")

flag = False


regi = 1
butt = sac.buttons([
    sac.ButtonsItem(label='REGISTRAR',icon='cloud-haze2'),
], position='right', format_func='upper', align='center', size='large',
shape='round', return_index=True,index=regi)



if butt == 0:
    datareg = {
    'calle': calle.upper(),
    'num_ext': num_ext,
    'colonia': colonia.upper(),
    'codigoP': codigoP.strip(),
    'localidad': localidad.upper(),
    'municipio': mun.upper(),
    'estado': estado.upper(),
    'calle_ref1': calleref1.upper(),
    'calle_ref2': calleref2.upper(),
    'num_int': num_int,
    'opcional_ref': referecia_ad
    }
    with st.spinner("Registrando domicilio... 🌐"):
      dat = reg_domicilio(datareg,st.session_state.last_registered["curp"])
    if "message" in dat:
      st.error("No se pudo registrar el domicilio 😥")
      st.error(dat["message"])
    else:
      st.success("Domicilio registrado con éxito 😄")
      flag = True
      st.json(dat)
      time.sleep(5)
      if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
        st.session_state.last_registered['update'] = False
        st.session_state.dataupdate = {}
        switch_page('perfilAlumno')
      else:
        with st.spinner("Redireccionando..."):
          time.sleep(2)
          switch_page("registroAlumno4")


if flag:

    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        subtitle='Datos Básicos',
        disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 2',subtitle='Datos Personales',
        description='Registra los datos personales del alumno',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 3',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso4',disabled=True,icon='lungs'),

        sac.StepsItem(title='Paso5',disabled=True,icon='layer-backward'),

        sac.StepsItem(title='Paso6',disabled=True,icon='person-bounding-box'),

        sac.StepsItem(title='Paso7',disabled=True,icon='file-earmark-text'),

        ], format_func='title',index=3)



else:
    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        description='Registro Básico',disabled=True,icon='check2-square'),

        sac.StepsItem(title='Paso 2',description='Datos Personales',disabled=True,icon='check2-square'),

       sac.StepsItem(title='Paso 3',disabled=False,icon='pin-map',
       subtitle='Domicilio',description='Registra el domicilio del alumno'),

        sac.StepsItem(title='Paso4',disabled=True,icon='lungs'),

        sac.StepsItem(title='Paso5',disabled=True,icon='layer-backward'),

        sac.StepsItem(title='Paso6',disabled=True,icon='person-bounding-box'),

        sac.StepsItem(title='Paso7',disabled=True,icon='file-earmark-text'),

        ], format_func='title',index=2)





