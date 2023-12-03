import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import extra_streamlit_components as stx
import datetime
import streamlit_analytics
import uuid
import bcrypt
from streamlit_option_menu import option_menu


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
st.set_page_config(page_title="SISTEMA CECYTEM", page_icon="rsc/Logos/cecytem-logo.png", layout="wide", initial_sidebar_state="collapsed")



#--------------------------------------------------
#Funciones

def get_credentials():
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

def credentials_formating(credentials):
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


def get_manager():
    """
    The function `get_manager` returns a `CookieManager` object with the key 'MyCookieManager'.
    :return: an instance of the `CookieManager` class with the key set to 'MyCookieManager'.
    """
    return stx.CookieManager(key='MyCookieManager')



#--------------------------------------------------
#Estilos de la pagina
st.markdown('''
<style>
body {
background-color: #e5e5f7;

}

[data-testid="collapsedControl"] {
        display: none
    }

#MainMenu, header, footer {visibility: hidden;}

.reportview-container .main .block-container {{
                    1100px
                    padding-top: 1rem;
                    padding-right: 5rem;
                    padding-left: 5rem;
                    padding-bottom: 1rem;
                }}

.st-emotion-cache-1juwlj7 {
  border: 1px solid rgba(9, 59, 41, 0.2);
  border-radius: 0.5rem;
  padding: calc(1em - 1px);
  background-color: azure;
}

.bg {
  animation:slide 20s ease-in-out infinite alternate;
  background-image: url(https://images.unsplash.com/photo-1444927714506-8492d94b4e3d?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&s=067f0b097deff88a789e125210406ffe);
  bottom:0;
  left:-50%;
  opacity:.5;
  position:fixed;
  right:-50%;
  top:0;
  z-index:0;
  ackground-size: cover;
  background-position: center center;
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


<div class="bg"></div>
<div class="bg bg2"></div>
<div class="bg bg3"></div>
''',unsafe_allow_html=True)








#--------------------------------------------------
#credenciales de la base de datos
data = get_credentials()
credentials = credentials_formating(data['records'])
#credentials
#st.session_state

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

if 'name' not in st.session_state:
    st.session_state['name'] = None


#--------------------------------------------------
# Cookie manager

cookie_manager = get_manager()
#--------------------------------------------------
#Navbar
# CSS style definitions
selected3 = option_menu(None, ["Inicio", "Docs","Acerca de","Contacto","Login"],
    icons=['house-heart',  "filetype-doc", 'patch-question', 'person-lines-fill', 'key'],
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#99B1BF00", "border-radius": "10px"},
        "icon": {"color": "#011526", "font-size": "25px"},
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#4F758C"},
        "nav-link-selected": {"background-color": "#0F4C59"},
    },key='menu'
)


if selected3 == "Login":
    switch_page('Login')


st.markdown(
    """
<style>
/* Desktops and laptops ----------- */
@media only screen and (min-width: 1224px) {
h1 {
--s: 0.1em;   /* the thickness of the line */
--c: #2c4bff; /* the color */
color: #0000;
padding-bottom: var(--s);
background:
  linear-gradient(90deg,var(--c) 50%,#000 0) calc(100% - var(--_p,0%))/200% 100%,
  linear-gradient(var(--c) 0 0) 0% 100%/var(--_p,0%) var(--s) no-repeat;
-webkit-background-clip: text,padding-box;
        background-clip: text,padding-box;
transition: 0.5s;
text-align: left;
}

h1:hover {--_p: 100%}
h1 {
  font-family: 'Oswald', sans-serif;
  font-size: 3rem;
  cursor: pointer;
}
}

@media all and (min-width:960px) and (max-width: 1024px) {
h1 {
--s: 0.1em;   /* the thickness of the line */
--c: #2c4bff; /* the color */
color: #0000;
padding-bottom: var(--s);
background:
  linear-gradient(90deg,var(--c) 50%,#000 0) calc(100% - var(--_p,0%))/200% 100%,
  linear-gradient(var(--c) 0 0) 0% 100%/var(--_p,0%) var(--s) no-repeat;
-webkit-background-clip: text,padding-box;
        background-clip: text,padding-box;
transition: 0.5s;
text-align: left;
}

h1:hover {--_p: 100%}
h1 {
  font-family: 'Oswald', sans-serif;
  font-size: 3rem;
  cursor: pointer;
}
}

@media all and (min-width:801px) and (max-width: 959px) {
  h1 {
  font-family: 'Roboto', sans-serif;
  font-size: 3rem;
  cursor: pointer;
}
}

@media all and (min-width:769px) and (max-width: 800px) {
  h1 {
  font-family: 'Roboto', sans-serif;
  font-size: 3rem;
  cursor: pointer;
}
}

@media all and (min-width:569px) and (max-width: 768px) {
  h1 {
  font-family: 'Roboto', sans-serif;
  font-size: 3rem;
  cursor: pointer;
}
}

@media all and (min-width:481px) and (max-width: 568px) {
  h1 {
  font-family: 'Roboto', sans-serif;
  font-size: 3rem;
  cursor: pointer;
}
}

@media all and (min-width:321px) and (max-width: 480px) {
  h1 {
  font-family: 'Roboto', sans-serif;
  font-size: 3rem;
  cursor: pointer;
}
}

@media all and (min-width:0px) and (max-width: 320px) {
  h1 {
  font-family: 'Roboto', sans-serif;
  font-size: 3rem;
  cursor: pointer;
}
}










</style>""",unsafe_allow_html=True,
)

cols = st.columns([0.8, 0.2])

with cols[0]:
  "# COLEGIO DE ESTUDIOS CIENTIFICOS Y TECNOLOGICOS DEL ESTADO DE MEXICO"


with cols[1]:
  st.image("rsc/Logos/cecytem-logo.png", width=120)

sac.divider(label='', icon='house', align='center')






st.markdown('''
<style>
.gallery-wrap {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 70vh;
}

.item {
  flex: 1;
  height: 100%;
  background-position: center;
  background-size: cover;
  background-repeat: none;
  transition: flex 0.8s ease;
}
.item:hover {
  flex: 7;
}

.item-1 {
  background-image: url("https://images.unsplash.com/photo-1499198116522-4a6235013d63?auto=format&fit=crop&w=1233&q=80");
}

.item-2 {
  background-image: url("https://images.unsplash.com/photo-1492760864391-753aaae87234?auto=format&fit=crop&w=1336&q=80");
}

.item-3 {
  background-image: url("https://images.unsplash.com/photo-1503631285924-e1544dce8b28?auto=format&fit=crop&w=1234&q=80");
}

.item-4 {
  background-image: url("https://images.unsplash.com/photo-1510425463958-dcced28da480?auto=format&fit=crop&w=1352&q=80");
}

.item-5 {
  background-image: url("https://images.unsplash.com/photo-1503602642458-232111445657?auto=format&fit=crop&w=1234&q=80");
}

.social {
  position: absolute;
  right: 35px;
  bottom: 0;
}
.social img {
  display: block;
  width: 32px;
}
</style>


<div class="container">

  <div class="gallery-wrap">
    <div class="item item-1"></div>
    <div class="item item-2"></div>
    <div class="item item-3"></div>
    <div class="item item-4"></div>
    <div class="item item-5"></div>
  </div>
 </div>




''',unsafe_allow_html=True)
