import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import uuid



with st.form("Registro de Tutor",clear_on_submit=True):
    nombre_completo = st.text_input("Nombre Completo*",placeholder="Nombre Completo",help="Ingrese el nombre completo del tutor")
    telefono = st.text_input("Telefono*",placeholder="Telefono",help="Ingrese el telefono del tutor")
    celular = st.text_input("Celular*",placeholder="Celular",help="Ingrese el celular del tutor")
    num_seguro_social = st.text_input("Numero de Seguro Social*",placeholder="Numero de Seguro Social",help="Ingrese el numero de seguro social del tutor")
