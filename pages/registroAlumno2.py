import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import uuid
import time



if "last_registered" not in st.session_state:
  st.session_state.last_registered = None
if "last_registered_data" not in st.session_state:
  st.session_state.last_registered_data = None

with st.form("Registro de Alumno",clear_on_submit=True):
  st.subheader("Datos Generales del Alumno")

  data = {}

  cols1 = st.columns([0.4,0.6])


  with cols1[0]:
    control_number = st.text_input("Numero de Control",placeholder=uuid.uuid4().hex[:8],max_chars=8,help="Ingrese el numero de control del alumno")

  with cols1[1]:
    curp = st.text_input("CURP*",placeholder="CURP",max_chars=18,help="Ingrese el CURP del alumno")

  periodo = st.selectbox("Periodo*",[i for i in range(2000,2030)],help="Seleccione el periodo del alumno")
  plantel = st.text_input("Plantel*",placeholder="Plantel",help="Ingrese el plantel del alumno")
  carrera = st.text_input("Carrera*",placeholder="Programación",help="Ingrese la carrera del alumno")
  tipoinscripcion = st.text_input("Tipo de Inscripción*",placeholder="Tipo de Inscripción",help="Ingrese el tipo de inscripción del alumno")

  nombre = st.text_input("Nombre(s)*",placeholder="Nombre(s)",help="Ingrese el nombre del alumno")
  cols2 = st.columns([0.5,0.5])

  with cols2[0]:
    apellidop = st.text_input("Apellido Paterno*",placeholder="Apellido Paterno",help="Ingrese el apellido paterno del alumno")
  with cols2[1]:
    apellidom = st.text_input("Apellido Materno*",placeholder="Apellido Materno",help="Ingrese el apellido materno del alumno")

  fecha_nacimiento = st.date_input("Fecha de Nacimiento*",help="Ingrese la fecha de nacimiento del alumno")
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
  enfermedads = st.empty()
  if enfermedad == "Si":
    enfermedad_desc = enfermedads.text_area("¿Cual?",help="Ingrese la enfermedad crónica del alumno",height=100)
  else:
    enfermedads.empty()
    enfermedad_desc = None

  nombre_tutor = st.text_input("Nombre del Tutor*",placeholder="Nombre del Tutor",help="Ingrese el nombre del tutor del alumno")
  telefono = st.text_input("Telefono*",placeholder="Telefono",help="Ingrese el telefono del tutor del alumno")
  celular = st.text_input("Celular",placeholder="Celular",help="Ingrese el celular del tutor del alumno")
  numero_seguro_social = st.text_input("Numero de Seguro Social*",placeholder="Numero de Seguro Social",help="Ingrese el numero de seguro social del tutor del alumno")
  tipo_servicio = st.selectbox("Tipo de Servicio*",["IMSS","ISSSTE","PEMEX","SEDENA","SEMAR","OTRO"],help="Seleccione el tipo de servicio del alumno")
  correo_personal = st.text_input("Correo Personal*",placeholder="Correo Personal",help="Ingrese el correo personal del alumno")
  correo_institucional = st.text_input("Correo Institucional*",placeholder="Correo Institucional",help="Ingrese el correo institucional del alumno")
  if st.form_submit_button("Registrar"):
    data["control_number"] = control_number
    data["curp"] = curp
    data["periodo"] = periodo
    data["plantel"] = plantel
    data["carrera"] = carrera
    data["tipoinscripcion"] = tipoinscripcion
    data["nombre"] = nombre
    data["apellidop"] = apellidop
    data["apellidom"] = apellidom
    data["fecha_nacimiento"] = fecha_nacimiento
    data["estado_nacimiento"] = estado_nacimiento
    data["nacionalidad"] = nacionalidad
    data["sexo"] = sexo
    data["estado_civil"] = estado_civil
    data["enfermedad"] = enfermedad
    data["enfermedad_desc"] = enfermedad_desc
    data["last_registered"] = st.session_state.last_registered
    data["type"] = "alumno"
    data["status"] = "Activo"
    data["id"] = uuid.uuid4().hex
    data["type"] = "alumno"
    data["status"] = "Activo"
    data["id"] = uuid.uuid4().hex
    data["nombre_tutor"] = nombre_tutor
    data["telefono"] = telefono
    if celular != "":
      data["celular"] = celular
    else:
      data["celular"] = None
    data["numero_seguro_social"] = numero_seguro_social
    data["tipo_servicio"] = tipo_servicio
    data["correo_personal"] = correo_personal
    data["correo_institucional"] = correo_institucional

    st.session_state.last_registered = data["curp"]

    st.success("Alumno registrado con exito")
    st.session_state.last_registered_data = data
    time.sleep(5)
    switch_page("registro_tutor")



st.write(st.session_state.last_registered_data)
