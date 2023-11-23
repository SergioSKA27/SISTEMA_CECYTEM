import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import uuid
import time

flag = False

with st.form("Registro de Alumno",clear_on_submit=True):
  st.subheader("Datos Generales del Alumno")



  cols1 = st.columns([0.4,0.6])


  with cols1[0]:
    control_number = st.text_input("Numero de Control",placeholder=uuid.uuid4().hex[:8],max_chars=8,help="Ingrese el numero de control del alumno")

  with cols1[1]:
    curp = st.text_input("CURP*",placeholder="CURP",max_chars=18,help="Ingrese el CURP del alumno")

  plantel = st.text_input("Plantel*",placeholder="Plantel",help="Ingrese el plantel del alumno")
  carrera = st.text_input("Carrera*",placeholder="Programación",help="Ingrese la carrera del alumno")

  if st.form_submit_button("Registrar"):

    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])

    #Creamos todos los registros necesarios con campos por defecto
    datat = xata.records().insert("TutorAlumno", {
    "id_tutorAlumno": uuid.uuid4().hex[:8]
    })


    data1 = xata.records().insert("DataAlumno", {
    "nombre": "string",
    "apellidoPaterno": "string",
    "apellidoMaterno": "string",
    "fechaNacimiento": "2000-01-01T00:00:00Z",
    "estadoNacimiento": "string",
    "sexo": "string",
    "nacionalidad": "string",
    "estadoCivil": "string",
    "telefono": "string",
    "celular": "string",
    "correoe_p": "a@b.com",
    "correoe_i": "a@b.com",
    "curp": curp.upper(),
    "id_tutorAlumno": datat['id']
})
    data = xata.records().insert("Alumno", {
    "carreraAlumno": carrera,
    "plantelAlumno": plantel,
    "curp": data1['id'],
    "idcontrol": uuid.uuid4().hex[:8],
    })

    flag = True
    st.write(data1)
    st.write(datat)
    st.write(data)

    st.session_state.last_registered = {"curp":curp.upper(),"id":data1['id'], "id_tutorAlumno": datat['id'], "idcontrol": data}
    st.success("Alumno registrado con éxito")

if flag:

    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        subtitle='Registro Básico',
        description='Registra los datos básicos del alumno',
        disabled=True),

        sac.StepsItem(title='Paso 2'),

        sac.StepsItem(title='Paso 3'),

        sac.StepsItem(title='Paso4', disabled=True),

        ], format_func='title',index=1)

    time.sleep(5)
    switch_page("registroAlumno2")



else:
    sac.steps(

    items=[

        sac.StepsItem(title='Paso 1',
        subtitle='Registro Básico',
        description='Registra los datos básicos del alumno',),

        sac.StepsItem(title='Paso 2'),

        sac.StepsItem(title='Paso 3'),

        sac.StepsItem(title='Paso4',),

        ], format_func='title',index=0)


