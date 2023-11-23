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



if "last_registered" not in st.session_state:
  st.session_state.last_registered = None
if "last_registered_curp" not in st.session_state:
  st.session_state.last_registered_curp = None


if st.session_state.last_registered is None:
  switch_page("registroAlumno1")

flag = False

with st.form("Registro de Alumno",clear_on_submit=True):
  st.subheader("Datos Generales del Alumno")

  data = {}

  cols1 = st.columns([0.4,0.6])


  with cols1[0]:
    #control_number = st.text_input("Numero de Control",placeholder=uuid.uuid4().hex[:8],max_chars=8,help="Ingrese el numero de control del alumno")
    st.write("Número de Control :",st.session_state.last_registered["idcontrol"]['id'])
  with cols1[1]:
    #curp = st.text_input("CURP*",placeholder="CURP",max_chars=18,help="Ingrese el CURP del alumno")
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
  ,help="Seleccione el estado de nacimiento del alumno",placeholder="Estado de México")

  nacionalidad = st.selectbox("Nacionalidad*",["Mexicana","Extranjera"],help="Seleccione la nacionalidad del alumno",placeholder="Mexicana/Extranjera")

  sexo = st.selectbox("Sexo*",["Masculino","Femenino"],help="Seleccione el sexo del alumno")

  estado_civil = st.selectbox("Estado Civil*",["Soltero(a)","Casado(a)","Divorciado(a)","Viudo(a)","Unión Libre"],help="Seleccione el estado civil del alumno")


  enfermedad = st.selectbox("¿Padece alguna enfermedad crónica?",["Si","No"],help="Seleccione si el alumno padece alguna enfermedad crónica",placeholder="Si/No")

  telefono = st.text_input("Telefono*",placeholder="Telefono",help="Ingrese el telefono del tutor del alumno")

  celular = st.text_input("Celular",placeholder="Celular",help="Ingrese el celular del tutor del alumno")

  correo_personal = st.text_input("Correo Personal*",placeholder="Correo Personal",help="Ingrese el correo personal del alumno")

  correo_institucional = st.text_input("Correo Institucional*",placeholder="Correo Institucional",help="Ingrese el correo institucional del alumno")

  if st.form_submit_button("Registrar"):
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.records().update("DataAlumno", st.session_state.last_registered["id"], {
    "nombre": nombre,
    "apellidoPaterno": apellidop,
    "apellidoMaterno": apellidom,
    "fechaNacimiento": datetime.datetime(
    fecha_nacimiento.year,
    fecha_nacimiento.month,
    fecha_nacimiento.day,
    0,0,0,3).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "estadoNacimiento": estado_nacimiento,
    "sexo": sexo,
    "nacionalidad": nacionalidad,
    "estadoCivil": estado_civil,
    })
    st.write(data)

    st.success("Alumno registrado con exito")
    flag = True



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
    #switch_page("registroAlumno2")



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





