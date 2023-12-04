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


# License: BSD 3-Clause

#Sistema de Gestión y Análisis CECYTEM

#Copyright (c) 2023 Sergio Demis Lopez Martinez

#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:

#1. Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.

#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

#3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



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
            "id_procedenciaAlumno",
        ],
        "filter": {
            "curp": curpAlumno
        }
    })

    data = xata.records().update("DocumentacionAlumno", iid['records'][0]['id_documentosAlumno']['id'],{
    "acta_nacimientoAlumno": reg_data['acta_nacimientoAlumno'],
    "certificado_secundariaAlumno": reg_data['certificado_secundariaAlumno'],
    "comprobante_domAlumno": reg_data['comprobante_domAlumno'],
    "certificado_saludAlumno": reg_data['certificado_saludAlumno'],
    "fotos_Alumno": reg_data['fotos_Alumno'],
    "solicitud_inscAlumno": reg_data['solicitud_inscAlumno'],
    "recibo_preinscAlumno": reg_data['recibo_preinscAlumno'],
    "recibo_inscAlumno": reg_data['recibo_inscAlumno'],
    "ine_tutorAlumno": reg_data['ine_tutorAlumno'],
    "carta_constAlumno": reg_data['carta_constAlumno'],
    "id_documentosAlumno": iid['records'][0]['id_documentosAlumno']['id']
})

    return data

#--------------------------------------------------
#Verificación de ultimo registro
if "last_registered" not in st.session_state or "idcontrol" not in st.session_state.last_registered:
  switch_page("registroAlumno1")


#--------------------------------------------------
#Authentication
if "authentication_status" not in st.session_state  :
    switch_page('Main')
else:
# el usuario debe estar autenticado para acceder a esta página
    if st.session_state["authentication_status"]:

        usrdata = get_current_user_info(st.session_state['username'])


        #--------------------------------------------------
        #Contenido de la página
        st.title('Registro de Alumno')
        st.divider()
        st.subheader('Registro Documentación del Alumno')
        cols = st.columns([0.4,0.6])

        with cols[0]:
          st.write("**Número de Control** :",st.session_state.last_registered['idcontrol'])
        with cols[1]:
          st.write("**CURP** :",st.session_state.last_registered["curp"])


        st.divider()

        datareg =  {}
        st.write("#### Ingresa el acta de nacimiento del alumno")
        formatacta = st.selectbox("Formato de acta de nacimiento",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")
        acta_nacimiento = st.file_uploader("Acta de Nacimiento",type=['pdf','png','jpg','jpeg'])



        if formatacta == 'pdf' and acta_nacimiento is not None:
            try:
                acta_nacimientoa = acta_nacimiento.read()
                acta_nacimientoAlumno = base64.b64encode(acta_nacimientoa.decode('utf-8'))
                acta_nacimientoAlumno = f"data:application/pdf;base64,{acta_nacimientoAlumno}"
                pdf_display = f'<iframe  src="{acta_nacimientoAlumno}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['acta_nacimientoAlumno'] = {
                "base64Content": acta_nacimientoa,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": '-'.join(["acta_nacimientoAlumno",uuid.uuid4().hex])+".pdf",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es un pdf o está dañado")
        elif acta_nacimiento is not None:
            try:
                acta_nacimientoa = acta_nacimiento.read()
                acta_nacimientoAlumno = base64.b64encode(acta_nacimientoa).decode('utf-8')
                acta_nacimientoAlumno = f"data:image/{formatacta};base64,{acta_nacimientoAlumno}"
                st.image(acta_nacimientoAlumno)
                datareg['acta_nacimientoAlumno'] = {
                "base64Content": acta_nacimientoa,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": '-'.join([st.session_state.last_registered['curp'],"acta_nacimientoAlumno"])+f".{formatacta}",
                "signedUrlTimeout": 300
            }
            except Exception as e:
                st.error(e)
                st.error("El archivo no es una imagen o está dañado")
        else:
            datareg['acta_nacimientoAlumno'] = {
                "base64Content": "SGVsbG8gV29ybGQ=",
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "upload.txt",
                "signedUrlTimeout": 300
            }

        #--------------------------------------------------
        st.write("#### Ingresa el certificado de secundaria del alumno")
        formatacertificadoSec = st.selectbox("Formato de certificado de secundaria",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")
        filecertificado_secundariaAlumno = st.file_uploader("Certificado de Secundaria",type=['pdf','png','jpg','jpeg'])

        if formatacertificadoSec == 'pdf' and filecertificado_secundariaAlumno is not None:
            try:
                certificado_secundariaAlumno = filecertificado_secundariaAlumno.read()
                certificado_secundariaAlumno = base64.b64encode(certificado_secundariaAlumno).decode('utf-8')
                certificado_secundariaAlumno = f"data:application/pdf;base64,{certificado_secundariaAlumno}"
                pdf_display = f'<iframe  src="{certificado_secundariaAlumno}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['certificado_secundariaAlumno'] = {
                "base64Content": certificado_secundariaAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'certificado_secundariaAlumno'])+".pdf",
                "signedUrlTimeout": 300
                }
            except:
                st.error("El archivo no es un pdf o está dañado")
        elif filecertificado_secundariaAlumno is not None:
            try:
                certificado_secundariaAlumno = filecertificado_secundariaAlumno.read()
                certificado_secundariaAlumno = base64.b64encode(certificado_secundariaAlumno).decode('utf-8')
                certificado_secundariaAlumno = f"data:image/{formatacertificadoSec};base64,{certificado_secundariaAlumno}"
                st.image(certificado_secundariaAlumno)
                datareg['certificado_secundariaAlumno'] = {
                "base64Content": certificado_secundariaAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'certificado_secundariaAlumno'])+f".{formatacertificadoSec}",
                "signedUrlTimeout": 300
                }
            except:
                st.error("El archivo no es una imagen o está dañado")
        else:
            datareg['certificado_secundariaAlumno'] = {
                "base64Content": "SGVsbG8gV29ybGQ=",
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "upload.txt",
                "signedUrlTimeout": 300
            }

        #--------------------------------------------------
        st.write("#### Ingresa el comprobante de domicilio del alumno")
        formatacomprobanteDom = st.selectbox("Formato de comprobante de domicilio",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")
        filecomprobante_domAlumno = st.file_uploader("Comprobante de Domicilio",type=['pdf','png','jpg','jpeg'])

        if formatacomprobanteDom == 'pdf' and filecomprobante_domAlumno is not None:
            try:
                comprobante_domAlumno = filecomprobante_domAlumno.read()
                comprobante_domAlumno = base64.b64encode(comprobante_domAlumno).decode('utf-8')
                comprobante_domAlumno = f"data:application/pdf;base64,{comprobante_domAlumno}"
                pdf_display = f'<iframe  src="{comprobante_domAlumno}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['comprobante_domAlumno'] = {
                "base64Content": comprobante_domAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'comprobante_domAlumno'])+".pdf",
                "signedUrlTimeout": 300
                }
            except:
                st.error("El archivo no es un pdf o está dañado")

        elif filecomprobante_domAlumno is not None:
            try:
                comprobante_domAlumno = filecomprobante_domAlumno.read()
                comprobante_domAlumno = base64.b64encode(comprobante_domAlumno).decode('utf-8')
                comprobante_domAlumno = f"data:image/{formatacomprobanteDom};base64,{comprobante_domAlumno}"
                st.image(comprobante_domAlumno)
                datareg['comprobante_domAlumno'] = {
                "base64Content": comprobante_domAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'comprobante_domAlumno'])+f".{formatacomprobanteDom}",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es una imagen o está dañado")
        else:
            datareg['comprobante_domAlumno'] = {
                "base64Content": "SGVsbG8gV29ybGQ=",
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "upload.txt",
                "signedUrlTimeout": 300
            }

        #--------------------------------------------------
        st.write("#### Ingresa el certificado de salud del alumno")
        formatacertificadoSalud = st.selectbox("Formato de certificado de salud",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")
        filecertificado_saludAlumno = st.file_uploader("Certificado de Salud",type=['pdf','png','jpg','jpeg'])

        if formatacertificadoSalud == 'pdf' and filecertificado_saludAlumno is not None:
            try:
                certificado_saludAlumno = filecertificado_saludAlumno.read()
                certificado_saludAlumno = base64.b64encode(certificado_saludAlumno).decode('utf-8')
                certificado_saludAlumno = f"data:application/pdf;base64,{certificado_saludAlumno}"
                pdf_display = f'<iframe  src="{certificado_saludAlumno}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['certificado_saludAlumno'] = {
                "base64Content": certificado_saludAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'certificado_saludAlumno'])+".pdf",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es un pdf o está dañado")
        elif filecertificado_saludAlumno is not None:
            try:
                certificado_saludAlumno = filecertificado_saludAlumno.read()
                certificado_saludAlumno = base64.b64encode(certificado_saludAlumno).decode('utf-8')
                certificado_saludAlumno = f"data:image/{formatacertificadoSalud};base64,{certificado_saludAlumno}"
                st.image(certificado_saludAlumno)
                datareg['certificado_saludAlumno'] = {
                "base64Content": certificado_saludAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'certificado_saludAlumno'])+f".{formatacertificadoSalud}",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es una imagen o está dañado")
        else:
            datareg['certificado_saludAlumno'] = {
                "base64Content": "SGVsbG8gV29ybGQ=",
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "upload.txt",
                "signedUrlTimeout": 300
            }

        #--------------------------------------------------
        st.write("#### Ingresa las fotos del alumno")
        filesfotos_Alumno = st.file_uploader("Fotos del Alumno",type=['png','jpg','jpeg'],accept_multiple_files=True)

        fotos_Alumno = []

        for file in range(len(filesfotos_Alumno)):
            if filesfotos_Alumno[file] is not None:
                try:
                    fotos = filesfotos_Alumno[file].read()
                    fotos = base64.b64encode(fotos).decode('utf-8')
                    fotos = f"data:image/{formatacertificadoSalud};base64,{fotos}"
                    st.image(fotos)
                    fotos_Alumno.append({
                "base64Content": fotos,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'fotos_Alumno'])+f".{filesfotos_Alumno[file].type}",
                "signedUrlTimeout": 300
            })
                except Exception as e:
                    st.error(e)
                    st.error("El archivo no es una imagen o está dañado")


        if len(fotos_Alumno) == 0:
            fotos_Alumno = [
                {
                    "base64Content": "SGVsbG8gV29ybGQ=",
                    "enablePublicUrl": False,
                    "mediaType": "application/octet-stream",
                    "name": "upload.txt",
                    "signedUrlTimeout": 300
                }
            ]


        datareg['fotos_Alumno'] = fotos_Alumno
        #--------------------------------------------------
        st.write("#### Ingresa la solicitud de inscripción del alumno")
        formataSolicitudInsc = st.selectbox("Formato de solicitud de inscripción",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")
        filesolicitud_inscAlumno = st.file_uploader("Solicitud de Inscripción",type=['pdf','png','jpg','jpeg'])

        if formataSolicitudInsc == 'pdf' and filesolicitud_inscAlumno is not None:
            try:
                solicitud_inscAlumno = filesolicitud_inscAlumno.read()
                solicitud_inscAlumno = base64.b64encode(solicitud_inscAlumno).decode('utf-8')
                solicitud_inscAlumno = f"data:application/pdf;base64,{solicitud_inscAlumno}"
                pdf_display = f'<iframe  src="{solicitud_inscAlumno}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['solicitud_inscAlumno'] = {
                "base64Content": solicitud_inscAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'solicitud_inscAlumno'])+".pdf",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es un pdf o está dañado")
        elif filesolicitud_inscAlumno is not None:
            try:
                solicitud_inscAlumno = filesolicitud_inscAlumno.read()
                solicitud_inscAlumno = base64.b64encode(solicitud_inscAlumno).decode('utf-8')
                solicitud_inscAlumno = f"data:image/{formataSolicitudInsc};base64,{solicitud_inscAlumno}"
                st.image(solicitud_inscAlumno)
                datareg['solicitud_inscAlumno'] = {
                "base64Content": solicitud_inscAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'solicitud_inscAlumno'])+f".{formataSolicitudInsc}",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es una imagen o está dañado")
        else:
            datareg['solicitud_inscAlumno'] = {
                "base64Content": "SGVsbG8gV29ybGQ=",
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "upload.txt",
                "signedUrlTimeout": 300
            }

        #--------------------------------------------------
        st.write("#### Ingresa el recibo de preinscripción del alumno")
        formataReciboPreinsc = st.selectbox("Formato de recibo de preinscripción",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")
        filerecibo_preinscAlumno = st.file_uploader("Recibo de Preinscripción",type=['pdf','png','jpg','jpeg'])

        if formataReciboPreinsc == 'pdf' and filerecibo_preinscAlumno is not None:
            try:
                recibo_preinscAlumno = filerecibo_preinscAlumno.read()
                recibo_preinscAlumno = base64.b64encode(recibo_preinscAlumno).decode('utf-8')
                recibo_preinscAlumno = f"data:application/pdf;base64,{recibo_preinscAlumno}"
                pdf_display = f'<iframe  src="{recibo_preinscAlumno}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['recibo_preinscAlumno'] = {
                "base64Content": recibo_preinscAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'recibo_preinscAlumno'])+".pdf",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es un pdf o está dañado")
        elif filerecibo_preinscAlumno is not None:
            try:
                recibo_preinscAlumno = filerecibo_preinscAlumno.read()
                recibo_preinscAlumno = base64.b64encode(recibo_preinscAlumno).decode('utf-8')
                recibo_preinscAlumno = f"data:image/{formataReciboPreinsc};base64,{recibo_preinscAlumno}"
                st.image(recibo_preinscAlumno)
                datareg['recibo_preinscAlumno'] = {
                "base64Content": recibo_preinscAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": '-'.join([st.session_state.last_registered['curp'],'recibo_preinscAlumno'])+f".{formataReciboPreinsc}",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es una imagen o está dañado")
        else:
            datareg['recibo_preinscAlumno'] = {
                "base64Content": "SGVsbG8gV29ybGQ=",
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "upload.txt",
                "signedUrlTimeout": 300
            }

        #--------------------------------------------------
        st.write("#### Ingresa el recibo de inscripción del alumno")
        formataReciboInsc = st.selectbox("Formato de recibo de inscripción",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")
        filerecibo_inscAlumno = st.file_uploader("Recibo de Inscripción",type=['pdf','png','jpg','jpeg'])

        if formataReciboInsc == 'pdf' and filerecibo_inscAlumno is not None:
            try:
                recibo_inscAlumno = filerecibo_inscAlumno.read()
                recibo_inscAlumno = base64.b64encode(recibo_inscAlumno).decode('utf-8')
                recibo_inscAlumno = f"data:application/pdf;base64,{recibo_inscAlumno}"
                pdf_display = f'<iframe  src="{recibo_inscAlumno}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['recibo_inscAlumno'] = {
                "base64Content": recibo_inscAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'recibo_inscAlumno'])+".pdf",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es un pdf o está dañado")
        elif filerecibo_inscAlumno is not None:
            try:
                recibo_inscAlumno = filerecibo_inscAlumno.read()
                recibo_inscAlumno = base64.b64encode(recibo_inscAlumno).decode('utf-8')
                recibo_inscAlumno = f"data:image/{formataReciboInsc};base64,{recibo_inscAlumno}"
                st.image(recibo_inscAlumno)
                datareg['recibo_inscAlumno'] =  {
                "base64Content": recibo_inscAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": '-'.join([st.session_state.last_registered['curp'],'recibo_inscAlumno'])+f".{formataReciboInsc}",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es una imagen o está dañado")
        else:
            datareg['recibo_inscAlumno'] =  {
                "base64Content": "SGVsbG8gV29ybGQ=",
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "upload.txt",
                "signedUrlTimeout": 300
            }
        #--------------------------------------------------
        st.write("#### Ingresa la credencial de elector del tutor del alumno")
        formataIneTutor = st.selectbox("Formato de credencial de elector",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")
        fileine_tutorAlumno = st.file_uploader("Credencial de Elector del Tutor",type=['pdf','png','jpg','jpeg'])


        if formataIneTutor == 'pdf' and fileine_tutorAlumno is not None:
            try:
                ine_tutorAlumno = fileine_tutorAlumno.read()
                ine_tutorAlumno = base64.b64encode(ine_tutorAlumno).decode('utf-8')
                ine_tutorAlumno = f"data:application/pdf;base64,{ine_tutorAlumno}"
                pdf_display = f'<iframe  src="{ine_tutorAlumno}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['ine_tutorAlumno'] = {
                "base64Content": ine_tutorAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'ine_tutorAlumno'])+".pdf",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es un pdf o está dañado")
        elif fileine_tutorAlumno is not None:
            try:
                ine_tutorAlumno = fileine_tutorAlumno.read()
                ine_tutorAlumno = base64.b64encode(ine_tutorAlumno).decode('utf-8')
                ine_tutorAlumno = f"data:image/{formataIneTutor};base64,{ine_tutorAlumno}"
                st.image(ine_tutorAlumno)
                datareg['ine_tutorAlumno'] = {
                "base64Content": ine_tutorAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": '-'.join([st.session_state.last_registered['curp'],'ine_tutorAlumno'])+f".{formataIneTutor}",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es una imagen o está dañado")
        else:
            datareg['ine_tutorAlumno'] = {
                "base64Content": "SGVsbG8gV29ybGQ=",
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "upload.txt",
                "signedUrlTimeout": 300
            }


        st.write("#### Ingresa la carta de constancia del alumno")
        formataCartaConst = st.selectbox("Formato de carta de constancia",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")
        filecarta_constAlumno = st.file_uploader("Carta de Constancia",type=['pdf','png','jpg','jpeg'])

        if formataCartaConst == 'pdf' and filecarta_constAlumno is not None:
            try:
                carta_constAlumno = filecarta_constAlumno.read()
                carta_constAlumno = base64.b64encode(carta_constAlumno).decode('utf-8')
                carta_constAlumno = f"data:application/pdf;base64,{carta_constAlumno}"
                pdf_display = f'<iframe  src="{carta_constAlumno}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['carta_constAlumno'] = {
                "base64Content": carta_constAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "-".join([st.session_state.last_registered['curp'],'carta_constAlumno'])+".pdf",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es un pdf o está dañado")
        elif filecarta_constAlumno is not None:
            try:
                carta_constAlumno = filecarta_constAlumno.read()
                carta_constAlumno = base64.b64encode(carta_constAlumno).decode('utf-8')
                carta_constAlumno = f"data:image/{formataCartaConst};base64,{carta_constAlumno}"
                st.image(carta_constAlumno)
                datareg['carta_constAlumno'] = {
                "base64Content": carta_constAlumno,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": '-'.join([st.session_state.last_registered['curp'],'carta_constAlumno'])+f".{formataCartaConst}",
                "signedUrlTimeout": 300
            }
            except:
                st.error("El archivo no es una imagen o está dañado")
        else:
            datareg['carta_constAlumno'] = {
                "base64Content": "SGVsbG8gV29ybGQ=",
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": "upload.txt",
                "signedUrlTimeout": 300
            }


        butt = sac.buttons([
            sac.ButtonsItem(label='REGISTRAR',icon='cloud-haze2'),
        ], position='right', format_func='upper', align='center', size='large',
        shape='round', return_index=True,index=1)


        flag = False

        if butt == 0:
            with st.spinner("Registrando Documentación del Alumno"):
                data = reg_procedenciaAlumno(datareg,st.session_state.last_registered['curp'])

            if "message"  in data:
                st.error('Error al registrar la documentación del alumno')
                st.error(data['message'])
            else:
                st.success("Se ha registrado toda la documentación del alumno con éxito 🎉")
                st.balloons()
                flag = True
                with st.spinner("Redireccionando a la página de inicio"):
                    time.sleep(5)
                    switch_page("AlumnosHome")



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

                sac.StepsItem(title='Paso5',disabled=True,icon='check2-square'),

                sac.StepsItem(title='Paso6',disabled=True,icon='check2-square'),

                sac.StepsItem(title='Paso7',disabled=True,icon='file-earmark-text'),

                ], format_func='title',index=6)



        else:
            sac.steps(items=[

                sac.StepsItem(title='Paso 1',
                description='Registro Básico',disabled=True,icon='check2-square'),
                sac.StepsItem(title='Paso 2',description='Datos Personales',disabled=True,icon='check2-square'),
               sac.StepsItem(title='Paso 3',disabled=True,icon='check2-square',
               description='Domicilio'),
                sac.StepsItem(title='Paso4',disabled=True,icon='check2-square',description='Salud'),
                sac.StepsItem(title='Paso5',disabled=True,icon='check2-square',description='Procedencia'),
                sac.StepsItem(title='Paso6',disabled=True,icon='check2-square',
                description='Tutor'),
                sac.StepsItem(title='Paso7',disabled=False,icon='file-earmark-text',subtitle='Documentación',
                description='Registra la documentación del alumno')], format_func='title',index=5)
    else:
        switch_page('Main')
