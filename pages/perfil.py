import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import yaml
from yaml.loader import SafeLoader
from streamlit_option_menu import option_menu
import extra_streamlit_components as stx
import datetime


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




#Esta es la pagina de inicio, donde se muestra el contenido de la pagina visible para todos los usuarios


#Configuracion de la pagina
st.set_page_config(page_title="Perfil", page_icon=":person-heart:", layout="wide", initial_sidebar_state="collapsed")

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


#--------------------------------------------------
#Funciones


def get_current_user_info(usrname):
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


def get_manager():
    """
    The function `get_manager` returns a `CookieManager` object with the key 'MyCookieManager'.
    :return: an instance of the `CookieManager` class with the key set to 'MyCookieManager'.
    """
    return stx.CookieManager(key='MyCookieManager')




def query_user(usrname):
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
        "filter": {
            "username": usrname
        }
    })
    return data,xata

#--------------------------------------------------

cookie_manager = get_manager()

#--------------------------------------------------
#Authentication
if "authentication_status" not in st.session_state:
    switch_page('Main')
else:
# el usuario debe estar autenticado para acceder a esta página
    if st.session_state["authentication_status"]:
            #--------------------------------------------------
            #credenciales de la base de datos
            with st.spinner('Cargando datos...'):
                usrdata = get_current_user_info(st.session_state["username"])


           #--------------------------------------------------
            #Navbar
            # CSS style definitions
            selected3 = option_menu(None, ["Inicio", "Alumnos",  "Profesores","Vinculación", "Orientación",st.session_state.username,"Cerrar Sesión"],
                icons=['house', 'mortarboard', "easel2", 'link', 'compass', 'person-heart','door-open'],
                menu_icon="cast", default_index=5, orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#e6f2f0"},
                    "icon": {"color": "#1B7821", "font-size": "20px"},
                    "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#4F758C"},
                    "nav-link-selected": {"background-color": "#0F4C59"},
                },key='menu'
            )
            if selected3 == 'Inicio':
                switch_page('Inicio')
            elif selected3 == 'Alumnos':
                switch_page('AlumnosHome')
            elif selected3 == 'Alumnos':
                switch_page('AlumnosHome')

            elif selected3 == 'Cerrar Sesión':
                st.session_state["authentication_status"] = False
                st.session_state["username"] = None
                st.session_state["name"] = None
                st.session_state["role"] = None
                st.session_state["record_id"] = None
                switch_page('Login')
            #usrdata
            cols = st.columns([.4,.6])

            with cols[0]:
                try:
                    st.image(usrdata['avatar']['url'],width=200)
                except:
                    st.image('https://us-east-1.xata.sh/file/01m34qhhcspcvkhlrcpn6ho9k5rllmsr4684epaf4qhu0isltg9eqlvs20ojac1n6csjicpk68sj0dhk60spm7l0pcq32gb3nuv5jk7rsinfhtal4982p9ss6cou06hb45qmnrcvm6aninblpkdqv2rja9g01tah')

            with cols[1]:
                st.title(f'¡Bienvenido {usrdata["username"]}!')
                st.write(f'**Nombre:** {usrdata["name"]}')
                st.write(f'**Correo:** {usrdata["email"]}')
                st.write(f'**Rol:** {usrdata["role"]}')
            st.divider()


            if usrdata['role'] == 'admin':
                if st.button('Panel de Administración'):
                    switch_page('adminpanel')
                st.write('**Administrador**')
                st.write('Como administrador puedes crear, modificar y eliminar usuarios.')
                st.write('**Alumnos**')
                st.write('Como administrador puedes crear, modificar y eliminar alumnos.')
                st.write('**Profesores**')
                st.write('Como administrador puedes crear, modificar y eliminar profesores.')
                st.write('**Vinculación**')
                st.write('Como administrador puedes crear, modificar y eliminar vinculaciones.')
                st.write('**Orientación**')
                st.write('Como administrador puedes crear, modificar y eliminar orientaciones.')
