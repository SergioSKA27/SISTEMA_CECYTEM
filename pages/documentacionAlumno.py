import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import uuid
import time
import datetime
import base64
import asyncio


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


#--------------------------------------------------
#Configuracion de la pagina
#--------------------------------------------------
st.set_page_config(page_title="Registro de Alumno", page_icon="rsc/Logos/cecytem-logo.png", layout="wide", initial_sidebar_state="collapsed")

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
#--------------------------------------------------

async def reg_DOCSALUMNO(reg_data: dict,curpAlumno: str)-> dict:
    """
    The function `reg_DOCSALUMNO` updates the document information of a student in a database using their CURP (Unique
    Population Registry Code).

    :param reg_data: The `reg_data` parameter is a dictionary that contains the registration data for a student. It includes
    the following keys:
    :type reg_data: dict
    :param curpAlumno: The parameter `curpAlumno` is a string that represents the CURP (Clave Única de Registro de
    Población) of the student. It is used to identify the student in the database
    :type curpAlumno: str
    :return: a dictionary containing the updated data for the "DocumentacionAlumno" record.
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


async def reg_docs(reg_data: dict,curpAlumno: str)-> dict:
    """
    The function `reg_docs` is an asynchronous function that takes in a dictionary `reg_data` and a string `curpAlumno` as
    parameters, and returns a dictionary.

    :param reg_data: The `reg_data` parameter is a dictionary that contains the registration data for a student. It likely
    includes information such as the student's name, address, contact details, and any other relevant information for
    registration
    :type reg_data: dict
    :param curpAlumno: The parameter `curpAlumno` is a string that represents the CURP (Clave Única de Registro de
    Población) of a student
    :type curpAlumno: str
    :return: a dictionary.
    """

    task =  asyncio.create_task(reg_DOCSALUMNO(reg_data,curpAlumno))
    data = await task
    return data
#--------------------------------------------------
#Verificación de ultimo registro
if "last_registered" not in st.session_state or "idcontrol" not in st.session_state.last_registered:
  switch_page("registroAlumno1")


#--------------------------------------------------
#Autenticación
#--------------------------------------------------
if "authentication_status" not in st.session_state  :
    switch_page('Main')
else:
    #--------------------------------------------------
    # el usuario debe estar autenticado para acceder a esta página
    #--------------------------------------------------
    if st.session_state["authentication_status"]:
        #--------------------------------------------------
        #Contenido de la página
        #--------------------------------------------------

        st.title('Registro de Alumno')
        st.divider()
        st.subheader('Registro Documentación del Alumno')
        cols = st.columns([0.4,0.6])

        with cols[0]:
          st.write("**Número de Control** :",st.session_state.last_registered['idcontrol'])
        with cols[1]:
          st.write("**CURP** :",st.session_state.last_registered["curp"])


        st.divider()
        #--------------------------------------------------
        #Acta de nacimiento
        #--------------------------------------------------
        datareg =  {}
        st.write("#### Ingresa el acta de nacimiento del alumno")

        formatacta = st.selectbox("Formato de acta de nacimiento",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")

        acta_nacimiento = st.file_uploader("Acta de Nacimiento",type=['pdf','png','jpg','jpeg'])



        if formatacta == 'pdf' and acta_nacimiento is not None:
            try:
                acta_nacimientoa = acta_nacimiento.read()
                _acta_nacimiento = base64.b64encode(acta_nacimientoa).decode('utf-8')
                acta_nacimientoAlumno = f"data:application/pdf;base64,{_acta_nacimiento}"
                pdf_display = f'<iframe  src="{acta_nacimientoAlumno}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['acta_nacimientoAlumno'] = {
                "base64Content": _acta_nacimiento,
                "enablePublicUrl": False,
                "mediaType": "application/octet-stream",
                "name": '-'.join(["acta_nacimientoAlumno",uuid.uuid4().hex])+".pdf",
                "signedUrlTimeout": 300
            }
            except Exception as e:
                st.error("El archivo no es un pdf o está dañado")
                st.error(e)
        elif acta_nacimiento is not None:
            try:
                acta_nacimientoa = acta_nacimiento.read()
                acta_nacimientoAlumno = base64.b64encode(acta_nacimientoa).decode('utf-8')
                st.image(acta_nacimientoAlumno)
                datareg['acta_nacimientoAlumno'] = {
                "base64Content": acta_nacimientoAlumno,
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
        #Certificado de secundaria
        #--------------------------------------------------
        st.write("#### Ingresa el certificado de secundaria del alumno")

        formatacertificadoSec = st.selectbox("Formato de certificado de secundaria",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")

        filecertificado_secundariaAlumno = st.file_uploader("Certificado de Secundaria",type=['pdf','png','jpg','jpeg'])

        if formatacertificadoSec == 'pdf' and filecertificado_secundariaAlumno is not None:
            try:
                certificado_secundariaAlumno = filecertificado_secundariaAlumno.read()
                _certificado_secundariaAlumno = base64.b64encode(certificado_secundariaAlumno).decode('utf-8')
                certificado_secundariaAlumno_ = f"data:application/pdf;base64,{_certificado_secundariaAlumno}"
                pdf_display = f'<iframe  src="{certificado_secundariaAlumno_}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['certificado_secundariaAlumno'] = {
                "base64Content": _certificado_secundariaAlumno,
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
                _certificado_secundariaAlumno = base64.b64encode(certificado_secundariaAlumno).decode('utf-8')
                st.image(_certificado_secundariaAlumno)
                datareg['certificado_secundariaAlumno'] = {
                "base64Content": _certificado_secundariaAlumno,
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
        #Comprobante de domicilio
        #--------------------------------------------------
        st.write("#### Ingresa el comprobante de domicilio del alumno")

        formatacomprobanteDom = st.selectbox("Formato de comprobante de domicilio",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")

        filecomprobante_domAlumno = st.file_uploader("Comprobante de Domicilio",type=['pdf','png','jpg','jpeg'])

        if formatacomprobanteDom == 'pdf' and filecomprobante_domAlumno is not None:
            try:
                comprobante_domAlumno = filecomprobante_domAlumno.read()
                _comprobante_domAlumno = base64.b64encode(comprobante_domAlumno).decode('utf-8')
                comprobante_domAlumno_ = f"data:application/pdf;base64,{_comprobante_domAlumno}"
                pdf_display = f'<iframe  src="{comprobante_domAlumno_}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['comprobante_domAlumno'] = {
                "base64Content": _comprobante_domAlumno,
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
                _comprobante_domAlumno = base64.b64encode(comprobante_domAlumno).decode('utf-8')
                st.image(_comprobante_domAlumno)
                datareg['comprobante_domAlumno'] = {
                "base64Content": _comprobante_domAlumno,
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
        #Certificado de salud
        #--------------------------------------------------
        st.write("#### Ingresa el certificado de salud del alumno")

        formatacertificadoSalud = st.selectbox("Formato de certificado de salud",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")

        filecertificado_saludAlumno = st.file_uploader("Certificado de Salud",type=['pdf','png','jpg','jpeg'])

        if formatacertificadoSalud == 'pdf' and filecertificado_saludAlumno is not None:
            try:
                certificado_saludAlumno = filecertificado_saludAlumno.read()
                _certificado_saludAlumno = base64.b64encode(certificado_saludAlumno).decode('utf-8')
                certificado_saludAlumno_ = f"data:application/pdf;base64,{_certificado_saludAlumno}"
                pdf_display = f'<iframe  src="{certificado_saludAlumno_}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['certificado_saludAlumno'] = {
                "base64Content": _certificado_saludAlumno,
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
                _certificado_saludAlumno = base64.b64encode(certificado_saludAlumno).decode('utf-8')
                st.image(_certificado_saludAlumno)
                datareg['certificado_saludAlumno'] = {
                "base64Content": _certificado_saludAlumno,
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
        #Fotos del alumno
        #--------------------------------------------------
        st.write("#### Ingresa las fotos del alumno")

        filesfotos_Alumno = st.file_uploader("Fotos del Alumno",type=['png','jpg','jpeg'],accept_multiple_files=True)

        fotos_Alumno = []

        for file in range(len(filesfotos_Alumno)):
            if filesfotos_Alumno[file] is not None:
                try:
                    fotos = filesfotos_Alumno[file].read()
                    _fotos = base64.b64encode(fotos).decode('utf-8')
                    st.image(_fotos)
                    fotos_Alumno.append({
                        "base64Content": _fotos,
                        "enablePublicUrl": False,
                        "mediaType": "application/octet-stream",
                        "name": "-".join([st.session_state.last_registered['curp'],'fotos_Alumno'])+".jpg",
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
        #Solicitud de inscripción
        #--------------------------------------------------
        st.write("#### Ingresa la solicitud de inscripción del alumno")

        formataSolicitudInsc = st.selectbox("Formato de solicitud de inscripción",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")

        filesolicitud_inscAlumno = st.file_uploader("Solicitud de Inscripción",type=['pdf','png','jpg','jpeg'])

        if formataSolicitudInsc == 'pdf' and filesolicitud_inscAlumno is not None:
            try:
                solicitud_inscAlumno = filesolicitud_inscAlumno.read()
                _solicitud_inscAlumno = base64.b64encode(solicitud_inscAlumno).decode('utf-8')
                solicitud_inscAlumno_ = f"data:application/pdf;base64,{_solicitud_inscAlumno}"
                pdf_display = f'<iframe  src="{solicitud_inscAlumno_}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['solicitud_inscAlumno'] = {
                "base64Content": _solicitud_inscAlumno,
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
                _solicitud_inscAlumno = base64.b64encode(solicitud_inscAlumno).decode('utf-8')
                st.image(_solicitud_inscAlumno)
                datareg['solicitud_inscAlumno'] = {
                "base64Content": _solicitud_inscAlumno,
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
        #Recibo de preinscripción
        #--------------------------------------------------
        st.write("#### Ingresa el recibo de preinscripción del alumno")

        formataReciboPreinsc = st.selectbox("Formato de recibo de preinscripción",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")

        filerecibo_preinscAlumno = st.file_uploader("Recibo de Preinscripción",type=['pdf','png','jpg','jpeg'])

        if formataReciboPreinsc == 'pdf' and filerecibo_preinscAlumno is not None:
            try:
                recibo_preinscAlumno = filerecibo_preinscAlumno.read()
                _recibo_preinscAlumno = base64.b64encode(recibo_preinscAlumno).decode('utf-8')
                recibo_preinscAlumno_ = f"data:application/pdf;base64,{_recibo_preinscAlumno}"
                pdf_display = f'<iframe  src="{recibo_preinscAlumno_}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['recibo_preinscAlumno'] = {
                "base64Content": _recibo_preinscAlumno,
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
                _recibo_preinscAlumno = base64.b64encode(recibo_preinscAlumno).decode('utf-8')
                st.image(_recibo_preinscAlumno)
                datareg['recibo_preinscAlumno'] = {
                "base64Content": _recibo_preinscAlumno,
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
        #Recibo de inscripción
        #--------------------------------------------------
        st.write("#### Ingresa el recibo de inscripción del alumno")

        formataReciboInsc = st.selectbox("Formato de recibo de inscripción",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")

        filerecibo_inscAlumno = st.file_uploader("Recibo de Inscripción",type=['pdf','png','jpg','jpeg'])

        if formataReciboInsc == 'pdf' and filerecibo_inscAlumno is not None:
            try:
                recibo_inscAlumno = filerecibo_inscAlumno.read()
                _recibo_inscAlumno = base64.b64encode(recibo_inscAlumno).decode('utf-8')
                recibo_inscAlumno_ = f"data:application/pdf;base64,{_recibo_inscAlumno}"
                pdf_display = f'<iframe  src="{recibo_inscAlumno_}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['recibo_inscAlumno'] = {
                "base64Content": _recibo_inscAlumno,
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
                _recibo_inscAlumno = base64.b64encode(recibo_inscAlumno).decode('utf-8')
                st.image(_recibo_inscAlumno)
                datareg['recibo_inscAlumno'] =  {
                "base64Content": _recibo_inscAlumno,
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
        #INE del tutor
        #--------------------------------------------------
        st.write("#### Ingresa la credencial de elector del tutor del alumno")

        formataIneTutor = st.selectbox("Formato de credencial de elector",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")

        fileine_tutorAlumno = st.file_uploader("Credencial de Elector del Tutor",type=['pdf','png','jpg','jpeg'])


        if formataIneTutor == 'pdf' and fileine_tutorAlumno is not None:
            try:
                ine_tutorAlumno = fileine_tutorAlumno.read()
                _ine_tutorAlumno = base64.b64encode(ine_tutorAlumno).decode('utf-8')
                ine_tutorAlumno_ = f"data:application/pdf;base64,{_ine_tutorAlumno}"
                pdf_display = f'<iframe  src="{ine_tutorAlumno_}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['ine_tutorAlumno'] = {
                "base64Content": _ine_tutorAlumno,
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
                _ine_tutorAlumno = base64.b64encode(ine_tutorAlumno).decode('utf-8')
                st.image(_ine_tutorAlumno)
                datareg['ine_tutorAlumno'] = {
                "base64Content": _ine_tutorAlumno,
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

        #--------------------------------------------------
        #Carta de constancia
        #--------------------------------------------------
        st.write("#### Ingresa la carta de constancia del alumno")

        formataCartaConst = st.selectbox("Formato de carta de constancia",['pdf','png','jpg','jpeg'],help="Selecciona el formato del archivo")

        filecarta_constAlumno = st.file_uploader("Carta de Constancia",type=['pdf','png','jpg','jpeg'])

        if formataCartaConst == 'pdf' and filecarta_constAlumno is not None:
            try:
                carta_constAlumno = filecarta_constAlumno.read()
                _carta_constAlumno = base64.b64encode(carta_constAlumno).decode('utf-8')
                carta_constAlumno_ = f"data:application/pdf;base64,{_carta_constAlumno}"
                pdf_display = f'<iframe  src="{carta_constAlumno_}" width="700" height="600" type="application/pdf"></iframe>'
                st.write('Preview del archivo pdf:')
                st.markdown(pdf_display, unsafe_allow_html=True)
                datareg['carta_constAlumno'] = {
                "base64Content": _carta_constAlumno,
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
                _carta_constAlumno = base64.b64encode(carta_constAlumno).decode('utf-8')
                st.image(_carta_constAlumno)
                datareg['carta_constAlumno'] = {
                "base64Content": _carta_constAlumno,
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

        #--------------------------------------------------
        #Registro
        #--------------------------------------------------
        inx = 1
        butt = sac.buttons([
            sac.ButtonsItem(label='REGISTRAR',icon='cloud-haze2'),
        ], position='right', format_func='upper', align='center', size='large',
        shape='round', return_index=True,index=inx)


        flag = False

        if butt == 0:
            with st.spinner("Registrando Documentación del Alumno"):
                data = reg_DOCSALUMNO(datareg,st.session_state.last_registered['curp'])

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
