import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
from streamlit_lottie import st_lottie
import uuid
import time

flag = False

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


#--------------------------------------------------


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

def register_Alumno(reg_data:dict)->tuple[bool,dict]:
    """
    The `register_Alumno` function registers a new student by creating records for the student's documents, background
    information, health information, address, tutor information, and the student's own information.

    :param reg_data: The `reg_data` parameter is a dictionary that contains the registration data for an Alumno (student).
    It includes the following keys:
    :type reg_data: dict
    :return: The function `register_Alumno` returns a tuple containing a boolean value and a dictionary. The boolean value
    indicates whether the registration was successful or not. The dictionary contains the data of the registered student.
    """

    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])

    idtutor = uuid.uuid4().hex
    iddomicilio = uuid.uuid4().hex
    idsalud = uuid.uuid4().hex
    iddocumentos = uuid.uuid4().hex
    idprocedencia = uuid.uuid4().hex

    dataestatus = xata.records().insert("EstatusAlumno", {
    "current_status": True,
    "tipoBaja": "NO APLICA",
    "causas": [
        "NO APLICA"
    ],
    "periodos_baja": [
        "NO APLICA"
    ]
    })

    dataSeguro = xata.records().insert("SeguroAlumno", {
    "tipo_seguro": "---",
    "no_seguro": "---",
    "provedor": "---"
    })

    dataDocumentos = xata.records().insert("DocumentacionAlumno", {
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
      "id_documentosAlumno": iddocumentos
  })

    dataProcedencia = xata.records().insert("ProcedenciaAlumno", {
        "claveCeneval": "---",
        "puntajeIngreso": 3,
        "secundariaProcedencia": "---",
        "estanciaSecundaria_years": 3,
        "promedioSecundaria": 6.0,
        "intentosAceptacion": 1,
        "id_procedenciaAlumno": idprocedencia
    })

    dataSalud = xata.records().insert("SaludAlumno", {
        "salud_status": False,
        "enfermedad_desc": "---",
        "padecimientos": [
            "---"
        ],
        "medicamentos": [
            "---"
        ],
        "tipo_sangre": "---",
        "opcional_desc": "---",
        "id_saludAlumno": idsalud,
        "impedimentos": [
        "---"
        ]
    })

    dataDomicilio = xata.records().insert("DomicilioAlumno", {
        "calle": "---",
        "num_int": 3,
        "num_ext": 3,
        "colonia": "---",
        "codigoP": "---",
        "localidad": "---",
        "municipio": "---",
        "estado": "---",
        "calle_ref1": "---",
        "calle_ref2": "---",
        "opcional_ref": "---",
        "id_domicilioAlumno": iddomicilio
    })

    dataTutor = xata.records().insert("TutorAlumno", {
        "nombre": "---",
        "apellidoPaterno": "---",
        "apellidoMaterno": "---",
        "curp": "---",
        "id_tutorAlumno": idtutor,
        "telefono": "string",
        "celular": "string"
	  })

    dataAlumno = xata.records().insert("DataAlumno", {
        "nombre": "---",
        "apellidoPaterno": "---",
        "apellidoMaterno": "---",
        "fechaNacimiento": "2000-01-01T00:00:00Z",
        "estadoNacimiento": "---",
        "sexo": "---",
        "nacionalidad": "---",
        "estadoCivil": "---",
        "telefono": "---",
        "celular": "---",
        "correoe_p": "a@b.com",
        "correoe_i": "a@b.com",
        "curp": reg_data['curp'],
        "id_tutorAlumno": dataTutor['id'],
        "id_domicilioAlumno": dataDomicilio['id'],
        "id_saludAlumno": dataSalud['id'],
        "id_documentosAlumno": dataDocumentos['id'],
        "id_procedenciaAlumno": dataProcedencia['id']
	    })

    data = xata.records().insert("Alumno", {
        "carreraAlumno": reg_data['carreraAlumno'],
        "plantelAlumno": reg_data['plantelAlumno'],
        "idcontrol": reg_data['idcontrol'],
        "curp": dataAlumno['id'],
        "estatus": dataestatus['id'],
        "seguro": dataSeguro['id'],
	  })


    return  data

def validar_datos(reg_data: dict)->tuple[bool,str]:
    """
    Valida los datos de un estudiante con estándares usuales.

    Args:
    - reg_data (dict): Un diccionario con los datos del estudiante.

    Returns:
    - bool: True si los datos son válidos, False de lo contrario.
    - str: Mensaje indicando el motivo de la invalidez si es False.
    """
    # Verificar que la carrera y el plantel sean cadenas no vacías
    if not reg_data["carreraAlumno"].strip() or not reg_data["plantelAlumno"].strip():
        return False, "Carrera y plantel no pueden estar vacíos."

    # Verificar que la CURP tenga la longitud correcta
    if len(reg_data["curp"]) != 18:
        return False, "La CURP debe tener 18 caracteres."

    # Verificar que el número de control tenga longitud 14
    if len(reg_data["idcontrol"]) != 14:
        return False, "El número de control debe tener longitud 14."

    # Si todas las verificaciones pasan, los datos son válidos
    return True, "Datos válidos."


#--------------------------------------------------
#Variables de Sesión


if "last_registered" not in st.session_state:
  st.session_state.last_registered = {}


#--------------------------------------------------
#Contenido de la página



#--------------------------------------------------
#Boton de regresar a la pagina anterior
colsb = st.columns([0.2,0.6,0.2])

with colsb[0]:
  indx0 = 1
  backpp = sac.buttons([
      sac.ButtonsItem(label='REGRESAR',icon='skip-backward-btn'),
  ], position='left', format_func='upper', align='center', size='large',
  shape='round', return_index=True,index=indx0)

  if backpp == 0:
    switch_page('AlumnosHome')


#--------------------------------------------------
st.title('Registro de Alumno')
st.divider()
st.subheader('Datos Básicos')
#--------------------------------------------------
#Registro Numero de Control
autog = st.checkbox("Generar numero de control automaticamente",help="Si se activa esta opción, el numero de control se generará aleatoriamente")
cols1 = st.columns([0.4,0.6])
checksum =  0
with cols1[0]:
    control_number = st.text_input("Numero de Control",max_chars=14,
    help="Ingrese el numero de control del alumno",value="")

if len(control_number) < 14 and len(control_number) != 0:
  st.error("El numero de control debe tener 14 caracteres")
else:
  checksum += 1

#--------------------------------------------------
#Registro CURP
with cols1[1]:
  curp = st.text_input("CURP*",placeholder="CURP",max_chars=18,help="Ingrese el CURP del alumno",value="")

if len(curp) < 18 and len(curp) != 0:
  st.error("El CURP no puede estar vacio")
else:
  checksum += 1
#--------------------------------------------------
#Registro Plantel
cols2 = st.columns([0.4,0.6])
with cols2[0]:
  plantel = st.text_input("Plantel*",placeholder="Plantel",help="Ingrese el plantel del alumno",value="")

if plantel == "":
  st.error("El plantel no puede estar vacio")
else:
  checksum += 1
#--------------------------------------------------
#Registro Carrera
carreras = [
    'Animación Digital',
    'Autotrónica',
    'Comercio Exterior',
    'Construcción',
    'Desarrollo Organizacional',
    'Diseño Gráfico Digital',
    'Electricidad',
    'Electrónica',
    'Enfermería General',
    'Estudios de Mercado y de Entornos Sociales',
    'Horticultura Sustentable',
    'Instrumentación Industrial',
    'Laboratorista Clínico',
    'Laboratorista Químico',
    'Logística',
    'Mantenimiento Automotriz',
    'Mantenimiento Industrial',
    'Máquinas-Herramienta',
    'Mecatrónica',
    'Preparación de Alimentos y Bebidas',
    'Procesos de Gestión Administrativa',
    'Producción Industrial',
    'Producción Industrial de Alimentos',
    'Programación',
    'Seguridad e Higiene y Protección Civil',
    'Servicios de Hotelería',
    'Soporte y Mantenimiento de Equipo de Cómputo',
    'Trabajo Social',
    'Ventas'
]

carreras = [carrera.upper() for carrera in carreras]

with cols2[1]:
  carrera = st.selectbox("Carrera*",carreras,help="Seleccione la carrera del alumno",index=0)
  checksum += 1






#--------------------------------------------------
#Boton de registro
#Diccionario de datos
reg_data = {"carreraAlumno": carrera.upper(),
            "plantelAlumno": plantel.upper(),
            "curp": curp.upper().strip(),
            "idcontrol": control_number}

check, mess = validar_datos(reg_data)

st.write(mess)
if check:
  flag = False
  indexreg = 1
  butt = sac.buttons([
      sac.ButtonsItem(label='REGISTRAR',icon='cloud-haze2'),
  ], position='right', format_func='upper', align='center', size='large',
  shape='round', return_index=True,index=indexreg)
else:
  butt = sac.buttons([
      sac.ButtonsItem(label='REGISTRAR',icon='cloud-haze2',disabled=True),
  ], position='right', format_func='upper', align='center', size='large',
  shape='round', return_index=True,index=1)
if butt == 0 and checksum == 4:

  #Registro del alumno
  with st.spinner("Registrando Alumno..."):
    data = register_Alumno(reg_data)

  if "message" not in data:
    #Registro exitoso
    st.session_state.last_registered = {"curp":curp.upper(),"id":data['id'],"idcontrol":control_number}
    st.success("Alumno registrado con éxito 😊")
    st.json(data)

    st.session_state.control_number = ""
    st.session_state.curp = ""
    st.session_state.plantel = ""
    st.session_state.carrera = ""
    with st.spinner("Redireccionando..."):
      time.sleep(2)
      switch_page("registroAlumno2")
  else:
    #Registro fallido
    st.error("Error al registrar al alumno 😥")
    st.error(data['message'])

elif butt == 0 and checksum != 4:
  #Campos vacios
  st.error("No se puede registrar al alumno, hay campos vacios 😲")



#--------------------------------------------------
#Steps de registro
if flag:
    stps = sac.steps(
    items=[
        sac.StepsItem(title='Paso 1',
        subtitle='Datos Básicos',
        description='Registra los datos básicos del alumno',
        disabled=True,icon='check2-square'),
        sac.StepsItem(title='Paso 2',icon='person-lines-fill'),
        sac.StepsItem(title='Paso 3',disabled=True,icon='pin-map'),
        sac.StepsItem(title='Paso4',disabled=True,icon='lungs'),
        sac.StepsItem(title='Paso5',disabled=True,icon='layer-backward'),
        sac.StepsItem(title='Paso6',disabled=True,icon='person-bounding-box'),
        sac.StepsItem(title='Paso7',disabled=True,icon='file-earmark-text'),],
        format_func='title',index=0,return_index=True)
else:
    sac.steps(
    items=[
        sac.StepsItem(title='Paso 1',
        subtitle='Datos Básicos',
        description='Registra los datos básicos del alumno',icon='fingerprint'),
        sac.StepsItem(title='Paso 2',disabled=True,icon='person-lines-fill'),
        sac.StepsItem(title='Paso 3',disabled=True,icon='pin-map'),
        sac.StepsItem(title='Paso4',disabled=True,icon='lungs'),
        sac.StepsItem(title='Paso5',disabled=True,icon='layer-backward'),
        sac.StepsItem(title='Paso6',disabled=True,icon='person-bounding-box'),
        sac.StepsItem(title='Paso7',disabled=True,icon='file-earmark-text'),],
        format_func='title',index=0)


st_lottie('https://lottie.host/a9d8ce55-0145-4cce-87ff-06c4cd00c3dc/Y9tHbq2E8F.json',key='footer',height=100)
