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
from streamlit_lottie import st_lottie
import datetime
from geopy.geocoders import Nominatim,Bing
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
import time
#Esta es la pagina de inicio, donde se muestra el contenido de la pagina visible para todos los usuarios


#Configuracion de la pagina
st.set_page_config(page_title="Perfil Alumno", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")
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
    data = xata.data().query("Alumno", {
            "columns": [
                "id",
                "carreraAlumno",
                "plantelAlumno",
                "idcontrol",
                "curp.*",
                "estatus.*",
                "seguro.*",
            ],
            "filter": {
                "idcontrol": record
            }
    })

    return data

def query_domicilioAlumno(record):
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.records().get("DomicilioAlumno", record)
    return data

def query_SaludAlumno(record):
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.records().get("SaludAlumno", record)
    return data

def query_procedenciaAlumno(record):
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.records().get("ProcedenciaAlumno", record)
    return data

def query_tutorAlumno(record):
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.records().get("TutorAlumno", record)
    return data


def delete_alumno(record):
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
                "idcontrol": record
            }
    })

    d1 = xata.records().delete("TutorAlumno", data['records'][0]['curp']['id_tutorAlumno']['id'])
    d2 = xata.records().delete("ProcedenciaAlumno", data['records'][0]['curp']['id_procedenciaAlumno']['id'])
    d3 = xata.records().delete("SaludAlumno", data['records'][0]['curp']['id_saludAlumno']['id'])
    d4 =xata.records().delete("DomicilioAlumno", data['records'][0]['curp']['id_domicilioAlumno']['id'])
    d5 =xata.records().delete("DocumentacionAlumno", data['records'][0]['curp']['id_documentosAlumno']['id'])
    d6 =xata.records().delete("DataAlumno", data['records'][0]['curp']['id'])
    d7 =xata.records().delete("EstatusAlumno", data['records'][0]['estatus']['id'])
    d8 =xata.records().delete("SeguroAlumno", data['records'][0]['seguro']['id'])
    d9 =xata.records().delete("Alumno", data['records'][0]['id'])

    return d1,d2,d3,d4,d5,d6,d7,d8,d9

#--------------------------------------------------

if "last_registered" not   in st.session_state:
    st.session_state.last_registered = {}
else:
    if "update" in  st.session_state.last_registered:
        st.session_state.last_registered['update'] = False
#--------------------------------------------------
#credenciales de la base de datos
data,xta = get_credentials()
credentials = credentials_formating(data['records'])
cookie_manager = get_manager()
query = query_Alumno(record=st.session_state['Alumnos_Search'])
query = query['records'][0]
dtaAlumno = query['curp']
domicilio = query_domicilioAlumno(dtaAlumno['id_domicilioAlumno']['id'])
salud = query_SaludAlumno(dtaAlumno['id_saludAlumno']['id'])
procencia = query_procedenciaAlumno(dtaAlumno['id_procedenciaAlumno']['id'])
tutor = query_tutorAlumno(dtaAlumno['id_tutorAlumno']['id'])
estatus = query['estatus']
seguro = query['seguro']
#--------------------------------------------------

#--------------------------------------------------
#Authentication
if "authentication_status" not in st.session_state:
    switch_page('Main')
else:
# el usuario debe estar autenticado para acceder a esta página
    if st.session_state["authentication_status"]:

            usrdata = get_current_user_info(st.session_state['username'])

            #usrdata
            #--------------------------------------------------
            with open('config.yaml') as file:
                config = yaml.load(file, Loader=SafeLoader)

            authenticator = stauth.Authenticate(
                {'usernames':credentials},
                config['cookie']['name'],
                config['cookie']['key'],
                config['cookie']['expiry_days'],
                config['preauthorized']
            )
            logcols = st.columns([0.2,0.6,0.2])
            with logcols[0]:
                backpp = sac.buttons([
                    sac.ButtonsItem(label='REGRESAR',icon='skip-backward-btn'),
                ], position='left', format_func='upper', align='center', size='large',
                shape='round', return_index=True,index=1)

                if backpp == 0:
                    switch_page('searchengineAlumnos')
            with logcols[-1]:
                authenticator.logout('Cerrar Sesión', 'main', key='unique_key')

            if usrdata['role'] in ['vinculacion','maestro','orientacion','admin']:

                st.title('Perfil del Alumno')
                st.divider()
                st.subheader("Datos de Control")
                cols0 = st.columns([0.5,0.5])
                with cols0[0]:
                    st.write("**Numero de Control:** ",query['idcontrol'])
                    st.write("**Plantel:** ",query['plantelAlumno'])
                with cols0[1]:
                    st.write("**CURP:** ",dtaAlumno['curp'])
                    st.write("**Carrera:** ",query['carreraAlumno'])
                    if usrdata['role'] in ['admin','orientacion']:
                        editst = 1
                        #Editar Informacion solo con permisos de administrador o orientacion
                        editarst = sac.buttons([
                            sac.ButtonsItem(label='EDITAR',icon='pencil-square'),
                        ], position='right', format_func='upper', align='right', size='large',
                        shape='round', return_index=True,index=editst,key='regstatus')

                        if editarst == 0:
                            st.session_state.last_registered['idcontrol'] = query['idcontrol']
                            st.session_state.last_registered['curp'] = dtaAlumno['curp']
                            st.session_state.last_registered['id'] = query['id']
                            st.session_state.last_registered['update'] = True
                            st.session_state.dataupdate = estatus
                            switch_page('modify_status')

                if estatus['current_status']:
                    st.write("**Estatus:**  :green[Activo]")
                else:
                    st.write("**Estatus:**  :red[Inactivo]")




                st.divider()
                st.subheader("Datos Generales del Alumno")
                colssH = st.columns([0.5,0.5])
                with colssH[0]:
                    if dtaAlumno['sexo'] == 'MASCULINO':
                        st_lottie('https://lottie.host/9938284c-32ae-42f7-8fdd-adaddffcc181/ZHy4Apg1Cy.json')
                    elif dtaAlumno['sexo'] == 'FEMENINO':
                        st_lottie('https://lottie.host/daf2c1f3-9914-46aa-b31f-cb9dc068eb4a/q2WitBc7Ux.json')
                    else:
                        st_lottie("https://lottie.host/b3da4593-d31b-4d9b-814d-e1986f879001/4ialEEEG8M.json")
                with colssH[1]:

                    if usrdata['role'] in ['admin','orientacion']:
                        edit0 = 1
                        #Editar Informacion solo con permisos de administrador o orientacion
                        editar2 = sac.buttons([
                            sac.ButtonsItem(label='EDITAR',icon='pencil-square'),
                        ], position='right', format_func='upper', align='right', size='large',
                        shape='round', return_index=True,index=edit0)

                        if editar2 == 0:
                            st.session_state.last_registered['idcontrol'] = query['idcontrol']
                            st.session_state.last_registered['curp'] = dtaAlumno['curp']
                            st.session_state.last_registered['id'] = query['id']
                            st.session_state.last_registered['update'] = True
                            st.session_state.dataupdate = dtaAlumno
                            switch_page('registroAlumno2')

                    st.write("**Nombre:** ",dtaAlumno['nombre'])
                    st.write("**Apellido Paterno:** ",dtaAlumno['apellidoPaterno'])
                    st.write("**Apellido Materno:** ",dtaAlumno['apellidoMaterno'])
                    st.write("**Sexo:** ",dtaAlumno['sexo'])
                    st.write("**Fecha de Nacimiento:** ",dtaAlumno['fechaNacimiento'][:10])
                    st.write("**Estado de Nacimiento:** ",dtaAlumno['estadoNacimiento'])
                    st.write("**Nacionalidad:** ",dtaAlumno['nacionalidad'])
                    st.write("**Estado Civil:** ",dtaAlumno['estadoCivil'])
                    st.write("**Telefono:** ",dtaAlumno['telefono'])
                    st.write("**Celular:** ",dtaAlumno['celular'])
                    st.write("**Correo Personal:** ",dtaAlumno['correoe_p'])
                    st.write("**Correo Institucional:** ",dtaAlumno['correoe_i'])


                #--------------------------------------------------

                st.divider()
                st.subheader("Datos de Domicilio")
                colsdom = st.columns([0.5,0.5])
                with colsdom[0]:
                    st.write("**Calle:** ",domicilio['calle'])
                    st.write("**Numero Exterior:** ",domicilio['num_ext'])
                    st.write("**Numero Interior:** ",domicilio['num_int'])
                    st.write("**Colonia:** ",domicilio['colonia'])
                    st.write("**Localidad:** ",domicilio['localidad'])
                    st.write("**Municipio:** ",domicilio['municipio'])
                    st.write("**Estado:** ",domicilio['estado'])
                    st.write("**Codigo Postal:** ",domicilio['codigoP'])
                    st.write("**Referencia 1:** ",domicilio['calle_ref1'])
                    st.write("**Referencia 2:** ",domicilio['calle_ref2'])
                    st.write("**Descripcion:** ",domicilio['opcional_ref'])



                direccion = domicilio['calle'] +" " + domicilio['localidad']  + " " + domicilio['codigoP'] + " " + domicilio['municipio'] + " " + domicilio['estado']

                with colsdom[1]:
                    if usrdata['role'] in ['admin','orientacion']:
                        edit1 = 1
                        #Editar Informacion solo con permisos de administrador o orientacion
                        editar3 = sac.buttons([
                            sac.ButtonsItem(label='EDITAR',icon='pencil-square'),
                        ], position='right', format_func='upper', align='right', size='large',
                        shape='round', return_index=True,index=edit1,key='regdom')

                        if editar3 == 0:
                            st.session_state.last_registered['idcontrol'] = query['idcontrol']
                            st.session_state.last_registered['curp'] = dtaAlumno['curp']
                            st.session_state.last_registered['id'] = query['id']
                            st.session_state.last_registered['update'] = True
                            st.session_state.dataupdate = domicilio
                            switch_page('registroAlumno3')
                    try:
                        #geolocator = Nominatim(user_agent="RegistroAlumno")
                        geolocator = Bing(api_key=st.secrets['db']['bing'])
                        location = geolocator.geocode(direccion,include_neighborhood=True)
                        st.write(location.address)
                        #st.write((location.latitude, location.longitude))
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
                #--------------------------------------------------
                st.divider()
                st.subheader("Datos de Salud")

                if usrdata['role'] in ['admin','orientacion']:
                    edit2 = 1
                    #Editar Informacion solo con permisos de administrador o orientacion
                    editar4 = sac.buttons([
                        sac.ButtonsItem(label='EDITAR',icon='pencil-square'),
                    ], position='right', format_func='upper', align='center', size='large',
                    shape='round', return_index=True,index=edit2,key='regsalud')

                    if editar4 == 0:
                        st.session_state.last_registered['idcontrol'] = query['idcontrol']
                        st.session_state.last_registered['curp'] = dtaAlumno['curp']
                        st.session_state.last_registered['id'] = query['id']
                        st.session_state.last_registered['update'] = True
                        st.session_state.dataupdate = salud
                        switch_page('registroAlumno4')

                if salud['salud_status']:
                    st.write("**Padece alguna enfermedad:**  SI")
                    st.write("**Descripción de la enfermedad:** ",salud['enfermedad_desc'])
                    st.write("**Padecimientos:** ",",".join(salud['padecimientos']))
                    st.write("**Medicamentos:** ",",".join(salud['medicamentos']))
                    st.write("**Impedimentos:** ",",".join(salud['impedimentos']))
                else:
                    st.write("**Padece alguna enfermedad:**  NO")
                st.write("**Tipo de Sangre:** ",salud['tipo_sangre'])
                st.write("**Notas adicionales:** ",salud['opcional_desc'])


                #--------------------------------------------------
                st.divider()
                st.subheader("Datos de Procedencia")
                if usrdata['role'] in ['admin','orientacion']:
                    edit3 = 1
                    #Editar Informacion solo con permisos de administrador o orientacion
                    editar5 = sac.buttons([
                        sac.ButtonsItem(label='EDITAR',icon='pencil-square'),
                    ], position='right', format_func='upper', align='center', size='large',
                    shape='round', return_index=True,index=edit3,key='regproc')

                    if editar5 == 0:
                        st.session_state.last_registered['idcontrol'] = query['idcontrol']
                        st.session_state.last_registered['curp'] = dtaAlumno['curp']
                        st.session_state.last_registered['id'] = query['id']
                        st.session_state.last_registered['update'] = True
                        st.session_state.dataupdate = procencia
                        switch_page('registroAlumno5')

                colsproc = st.columns([0.5,0.5])
                with colsproc[0]:
                    st.write("**Clave CENEVAL:** ",procencia['claveCeneval'])
                    st.write("**Secundaria de Procedencia:** ",procencia['secundariaProcedencia'])
                    st.write("**Promedio de Secundaria:** ",procencia['promedioSecundaria'])
                with colsproc[1]:
                    st.write("**Estancia en Secundaria(Años):** ",procencia['estanciaSecundaria_years'])
                    st.write("**Intentos de Aceptación:** ",procencia['intentosAceptacion'])
                    st.write("**Puntaje de Ingreso:** ",procencia['puntajeIngreso'])
                #--------------------------------------------------
                st.divider()
                st.subheader("Datos del Tutor")
                if usrdata['role'] in ['admin','orientacion']:
                    edit4 = 1
                    #Editar Informacion solo con permisos de administrador o orientacion
                    editar6 = sac.buttons([
                        sac.ButtonsItem(label='EDITAR',icon='pencil-square'),
                    ], position='right', format_func='upper', align='center', size='large',
                    shape='round', return_index=True,index=edit4,key='regtutor')

                    if editar6 == 0:
                        st.session_state.last_registered['idcontrol'] = query['idcontrol']
                        st.session_state.last_registered['curp'] = dtaAlumno['curp']
                        st.session_state.last_registered['id'] = query['id']
                        st.session_state.last_registered['update'] = True
                        st.session_state.dataupdate = tutor
                        switch_page('registro_tutor')

                st.write("**Nombre:** ",tutor['nombre'])
                st.write("**Apellido Paterno:** ",tutor['apellidoPaterno'])
                st.write("**Apellido Materno:** ",tutor['apellidoMaterno'])
                st.write("**CURP:** ",tutor['curp'])
                st.write("**Telefono:** ",tutor['telefono'])
                st.write("**Celular:** ",tutor['celular'])

                st.divider()
                st.subheader("Datos del Seguro")
                if usrdata['role'] in ['admin','orientacion']:
                    editseg = 1
                    #Editar Informacion solo con permisos de administrador o orientacion
                    editarseg = sac.buttons([
                        sac.ButtonsItem(label='EDITAR',icon='pencil-square'),
                    ], position='right', format_func='upper', align='center', size='large',
                    shape='round', return_index=True,index=editseg,key='editseg')

                    if editarseg == 0:
                        st.session_state.last_registered['idcontrol'] = query['idcontrol']
                        st.session_state.last_registered['curp'] = dtaAlumno['curp']
                        st.session_state.last_registered['id'] = query['id']
                        st.session_state.last_registered['update'] = True
                        st.session_state.dataupdate = seguro
                        switch_page('modify_seguro')

                st.write("**Numero de Seguro:** ",seguro['no_seguro'])
                st.write("**Tipo de Seguro:** ",seguro['tipo_seguro'])
                st.write("**Proveedor de Seguro:** ",seguro['provedor'])

                if st.checkbox("raw data"):
                    st.write(query)
                    st.write(dtaAlumno)
                    st.write(domicilio)
                    st.write(salud)
                    st.write(procencia)
                    st.write(tutor)

                if usrdata['role'] in ['admin','orientacion']:

                    with st.form(key='my_form'):
                        st.subheader(":red_circle:  :red[Eliminar Alumno]")
                        st.warning("¿Estas seguro de eliminar este alumno?")
                        r1 = st.checkbox("Si, eliminar")
                        st.error("Esta accion no se puede deshacer todos los datos del alumno seran eliminados y no se podran recuperar 🚨, ¿Esta Seguro?")
                        r2 = st.checkbox("Estoy seguro")
                        if st.form_submit_button(":red[Eliminar]") and r1 and r2:
                            d = delete_alumno(query['idcontrol'])
                            st.success("Alumno Eliminado")
                            for i in d:
                                st.write(i)
                            with st.spinner("Redireccionando..."):
                                time.sleep(5)
                                switch_page('searchengineAlumnos')


    else:
        switch_page('Main')
