import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
#Configuracion de la pagina
st.set_page_config(page_title="Admin", page_icon=":shield:", layout="wide", initial_sidebar_state="collapsed")

xata = XataClient(api_key='xau_FT9FcVgwPqMemnUzaDaXKvgXSiPgkWgu3',db_url='https://Sergio-Lopez-Martinez-s-workspace-l2j1g2.us-east-1.xata.sh/db/sistema-cecytem')

data = xata.data().query("Credentials", {
    "columns": [
        "id",
        "username",
        "email",
        "password",
        "avatar",
        "name",
        "role"
    ]
})
data
if st.button('Registra un usuario'):
    switch_page('user_register')
