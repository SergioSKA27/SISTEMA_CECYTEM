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


def modify_seguro(curp,datareg):

    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.data().query("Alumno", {
            "columns": [
                "id",
                "carreraAlumno",
                "plantelAlumno",
                "idcontrol",
                "curp.*",
                "estatus.id",
                "seguro.id",
            ],
            "filter": {
                "curp.curp": curp
            }
    })
    datar = xata.records().update("SeguroAlumno",data['records'][0]['seguro']['id'], {
    "tipo_seguro": datareg['tipo_seguro'],
    "no_seguro": datareg['no_seguro'],
    "provedor": datareg['provedor'],
    })
    return datar

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
        if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
          backpp = sac.buttons([
                            sac.ButtonsItem(label='REGRESAR',icon='skip-backward-btn'),
                        ], position='left', format_func='upper', align='center', size='large',
                        shape='round', return_index=True,index=1)

          if backpp == 0:
            st.session_state.last_registered['update'] = False
            st.session_state.dataupdate = {}
            switch_page('perfilAlumno')



        st.markdown("<h1>REGISTRO SEGURO ALUMNO</h1>", unsafe_allow_html=True)
        st.divider()

        if "update" in st.session_state.last_registered and st.session_state.last_registered['update'] and st.session_state.dataupdate ['tipo_seguro'] in ["SEGURO FACULTATIVO","SEGURO POPULAR","SEGURO IMSS","SEGURO ISSSTE","SEGURO PRIVADO"]:
            tipo_seguro =  st.selectbox("Tipo de seguro",["SEGURO FACULTATIVO","SEGURO POPULAR","SEGURO IMSS","SEGURO ISSSTE","SEGURO PRIVADO"],
            index=["SEGURO FACULTATIVO","SEGURO POPULAR","SEGURO IMSS","SEGURO ISSSTE","SEGURO PRIVADO"].index(st.session_state.dataupdate['tipo_seguro']),
            help="Selecciona el tipo de seguro del alumno")
        else:
            tipo_seguro =  st.selectbox("Tipo de seguro",["SEGURO FACULTATIVO","SEGURO POPULAR","SEGURO IMSS","SEGURO ISSSTE","SEGURO PRIVADO"],help="Selecciona el tipo de seguro del alumno")


        if "update" in st.session_state.last_registered and st.session_state.last_registered['update'] and st.session_state.dataupdate ['provedor'] in ["ESCUELA","PADRES","OTRO"]:
            provedor = st.selectbox("Provedor",["ESCUELA","PADRES","OTRO"],index=["ESCUELA","PADRES","OTRO"].index(st.session_state.dataupdate['provedor']),
            help="Selecciona el provedor del seguro del alumno")
        else:
            provedor = st.selectbox("Provedor",["ESCUELA","PADRES","OTRO"],help="Selecciona el provedor del seguro del alumno")

        if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
            no_seguro = st.text_input("Numero de seguro",value=st.session_state.dataupdate['no_seguro'],help="Ingresa el numero de seguro del alumno")
        else:
            no_seguro = st.text_input("Numero de seguro",help="Ingresa el numero de seguro del alumno")


        if st.button("REGISTRAR"):
            if "update" in st.session_state.last_registered and st.session_state.last_registered['update']:
                d = modify_seguro(st.session_state.last_registered['curp'],{
                    "tipo_seguro": tipo_seguro,
                    "no_seguro": no_seguro,
                    "provedor": provedor,
                })

                if "message" in d:
                    st.error('Error al registrar el seguro del alumno')
                    st.error(d['message'])
                else:
                    st.session_state.last_registered['update'] = False
                    st.session_state.dataupdate = {}
                    st.success('Seguro del alumno registrado con éxito')
                    time.sleep(2)
                    switch_page('perfilAlumno')
            else:
                modify_seguro(st.session_state.last_registered['curp'],{
                    "tipo_seguro": tipo_seguro,
                    "no_seguro": no_seguro,
                    "provedor": provedor,
                })
                switch_page('registroAlumno1')
    else:
        switch_page('Main')
