import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import yaml
from yaml.loader import SafeLoader
#Esta es la pagina de inicio, donde se muestra el contenido de la pagina visible para todos los usuarios

st.set_page_config(page_title="Inicio", page_icon=":house:", layout="wide", initial_sidebar_state="collapsed")



st.title('Bienvenido a la pagina de inicio')

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    st.json(config)

xata = XataClient(api_key='xau_FT9FcVgwPqMemnUzaDaXKvgXSiPgkWgu3',db_url='https://Sergio-Lopez-Martinez-s-workspace-l2j1g2.us-east-1.xata.sh/db/sistema-cecytem')

data = xata.data().query("Credentials", {
    "columns": [
        "id",
        "username",
        "email",
        "password"
    ],
    "page": {
        "size": 15
    }
})

st.write(data)
# Baner de la pagina
