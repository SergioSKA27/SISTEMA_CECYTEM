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
    top: 0;
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


def modify_status(curp,datareg):
    """
    The function `modify_status` modifies the status of a user in the database.

    :param record: The `record` parameter is a dictionary containing the information of the user whose status you want to
    modify.
    :return: The function `modify_status` returns a boolean value indicating whether the status of the user was modified
    successfully.
    """
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.data().query("Alumno", {
            "columns": [
                "id",
                "carreraAlumno",
                "plantelAlumno",
                "idcontrol",
                "curp.*",
                "estatus.id",
                "seguro.id",
            ],
            "filter": {
                "curp.curp": curp
            }
    })
    datar = xata.records().update("EstatusAlumno", data['records'][0]['estatus']['id'], {
    "current_status": datareg['current_status'],
    "tipoBaja": datareg['tipoBaja'],
    "causas": datareg['causas'],
    "periodos_baja": datareg['periodos_baja'],
    })
    return datar

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



st.markdown("<h1>CAMBIO DE ESTATUS ALUMNO</h1>", unsafe_allow_html=True)
st.divider()


if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
    currents = st.checkbox("¿El alumno se encuentra actualmente inscrito?",value=str(st.session_state.dataupdate['current_status']))
else:
    currents = st.checkbox("¿El alumno se encuentra actualmente inscrito?",value=True)

if not currents:
    if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
        tipoBaja = st.radio("Tipo de baja",options=["Temporal","Definitiva"])
    else:
        tipoBaja = st.radio("Tipo de baja",options=["Temporal","Definitiva"],index=0)

    if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
        causas = st.text_area("Causas de la baja",value=','.join(st.session_state.dataupdate['causas']),help="Separa las causas con una coma")
    else:
        causas = st.text_area("Causas de la baja",help="Separa las causas con una coma")

    if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
        periodos_baja = st.text_area("Periodos de baja",value=','.join(st.session_state.dataupdate['periodos_baja']),help="Separa los periodos con una coma")
    else:
        periodos_baja = st.text_area("Periodos de baja",help="Separa los periodos con una coma")

    if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
        if st.button("Actualizar"):
            datareg = {
                "current_status": currents,
                "tipoBaja": tipoBaja,
                "causas": causas.split(','),
                "periodos_baja": periodos_baja.split(',')
            }
            datareg
            modify_status(st.session_state.last_registered['curp'],datareg)
            st.session_state.last_registered['update'] = False
            st.session_state.dataupdate = {}
            switch_page('perfilAlumno')
    else:
        if st.button("Registrar"):
            datareg = {
                "current_status": currents,
                "tipoBaja": tipoBaja,
                "causas": causas,
                "periodos_baja": periodos_baja,
            }
            modify_status(st.session_state.last_registered['curp'],datareg)
            switch_page('registroAlumno1')
