import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import uuid



with st.form("Registro de Tutor",clear_on_submit=True):
    nombre_completo = st.text_input("Nombre(s)*",placeholder="Nombre(s)",help="Ingrese el nombre(s) del tutor")
    cols2 = st.columns([0.5,0.5])

    with cols2[0]:
        apellidop = st.text_input("Apellido Paterno*",placeholder="Apellido Paterno",help="Ingrese el apellido paterno del tutor")
    with cols2[1]:
        apellidom = st.text_input("Apellido Materno*",placeholder="Apellido Materno",help="Ingrese el apellido materno del tutor")


    telefono = st.text_input("Telefono*",placeholder="Telefono",help="Ingrese el telefono del tutor")
    celular = st.text_input("Celular",placeholder="Celular",help="Ingrese el celular del tutor")
    #num_seguro_social = st.text_input("Numero de Seguro Social*",placeholder="Numero de Seguro Social",help="Ingrese el numero de seguro social del tutor")

    st.form_submit_button("Registrar")
