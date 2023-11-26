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

    xata = XataClient()

    idtutor = uuid.uuid4().hex
    iddomicilio = uuid.uuid4().hex
    idsalud = uuid.uuid4().hex
    iddocumentos = uuid.uuid4().hex
    idprocedencia = uuid.uuid4().hex


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
        "id_saludAlumno": idsalud
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
        "id_domicilioAlumno": "---"
    })

    dataTutor = xata.records().insert("TutorAlumno", {
        "nombre": "---",
        "apellidoPaterno": "---",
        "apellidoMaterno": "---",
        "curp": "---",
        "id_tutorAlumno": idtutor
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
        "curp": dataAlumno['id']
	  })

    verf = xata.records().query("Alumno",{"filter": {"id": data['id']}})

    if verf['records'] == []:
        return False, {}
    else:
        return True, data




#--------------------------------------------------



st.title('Registro de Alumno')



st.divider()
st.subheader('Datos Básicos')

autog = st.checkbox("Generar numero de control automaticamente",help="Si se activa esta opción, el numero de control se generará aleatoriamente")

cols1 = st.columns([0.4,0.6])


with cols1[0]:
  if autog:
      st.write("Numero de control: ",uuid.uuid4().hex[:8])
  else:
    control_number = st.text_input("Numero de Control",placeholder=uuid.uuid4().hex[:8],max_chars=8,help="Ingrese el numero de control del alumno")

with cols1[1]:
  curp = st.text_input("CURP*",placeholder="CURP",max_chars=18,help="Ingrese el CURP del alumno")


cols2 = st.columns([0.4,0.6])

with cols2[0]:
  plantel = st.text_input("Plantel*",placeholder="Plantel",help="Ingrese el plantel del alumno")

with cols2[1]:
  carrera = st.text_input("Carrera*",placeholder="Programación",help="Ingrese la carrera del alumno")

flag = False

if st.button("Registrar"):
  reg_data = {"carreraAlumno": carrera,
              "plantelAlumno": plantel,
              "curp": curp.upper(),
              "idcontrol": control_number}

  flag, data = register_Alumno(reg_data)

  if flag:
    st.session_state.last_registered = {"curp":curp.upper(),"id":data['id'],"idcontrol":control_number}
    st.success("Alumno registrado con éxito")
    switch_page("registroAlumno2")
  else:
    st.error("Error al registrar al alumno")




if flag:

    stps = sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        subtitle='Registro Básico',
        description='Registra los datos básicos del alumno',
        disabled=True),

        sac.StepsItem(title='Paso 2'),

        sac.StepsItem(title='Paso 3'),

        sac.StepsItem(title='Paso4'),

        ], format_func='title',index=1,return_index=True)


    if stps == 1:
      switch_page("registroAlumno2")

    if st.button("Siguiente"):
      switch_page("registroAlumno2")



else:
    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        subtitle='Registro Básico',
        description='Registra los datos básicos del alumno',),

        sac.StepsItem(title='Paso 2',disabled=True),

        sac.StepsItem(title='Paso 3',disabled=True),

        sac.StepsItem(title='Paso4',disabled=True),

        ], format_func='title',index=0)


st_lottie('https://lottie.host/a9d8ce55-0145-4cce-87ff-06c4cd00c3dc/Y9tHbq2E8F.json',key='footer',height=100)
