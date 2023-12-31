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
import base64
from streamlit_option_menu import option_menu

from streamlit_lottie import st_lottie

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
#Navbar
# CSS style definitions
selected3 = option_menu(None, ["Inicio", "Docs","Acerca de","Contacto","Login"],
    icons=['house-heart',  "filetype-doc", 'patch-question', 'person-lines-fill', 'key'],
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#99B1BF00",},
        "icon": {"color": "#011526", "font-size": "25px"},
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#4F758C"},
        "nav-link-selected": {"background-color": "#0F4C59"},
    },key='menu'
)


if selected3 == "Login":
    switch_page('Login')


cols = st.columns([0.8, 0.2])

with cols[0]:
  "# COLEGIO DE ESTUDIOS CIENTIFICOS Y TECNOLOGICOS DEL ESTADO DE MEXICO"


with cols[1]:
  st.image("rsc/Logos/cecytem-logo.png", width=120)

sac.divider(label='', icon='house', align='center')

st.markdown("## Sistema de Gestión Escolar y Análisis de Datos CECYTEM")


st.markdown("<div style='text-align: center;font-family: futura;font-size: 30px;'>Bienvenido al Sistema de Gestión Escolar y Análisis CECYTEM</div>", unsafe_allow_html=True)

st.markdown("<div style='text-align: center;font-family: futura;font-size: 20px;'>Nuestra plataforma integral está diseñada para ofrecer una experiencia educativa sin complicaciones y eficiente. Descubre cómo nuestro sistema puede potenciar la gestión escolar y optimizar el análisis de datos para estudiantes, maestros y administradores.</div>", unsafe_allow_html=True)


sac.divider(label='', icon='mortarboard', align='center')
cols2 = st.columns([0.6, 0.4])


with cols2[0]:
  st.markdown('''
  ### Gestión de Alumnos:

  - Registra fácilmente nuevos alumnos, capturando información esencial en un proceso fluido y estructurado.


  - Explora herramientas avanzadas de búsqueda y gestión de perfiles para un acceso rápido y eficiente a la información del alumno.


  - Control total sobre la información académica, de salud, procedencia y documentación de cada estudiante.

  ''',unsafe_allow_html=True)

with cols2[1]:
  st_lottie("https://lottie.host/b7ef026c-555f-42ba-8c63-d34ab2c09d34/ZozkKz25so.json", height=300)

st.divider()


st.markdown('''
<div style="text-align: center;font-family: 'Osaka';font-size: 30px;">
Conectando estudiantes, maestros y administradores de manera eficiente.
</div>
<div style="text-align: center;font-family: 'futura';font-size: 20px;">
Datos potenciados, educación mejorada.
</div>
''',unsafe_allow_html=True)

sac.divider(label='', icon='graph-up', align='center')

cols3 = st.columns([0.6, 0.4])

with cols3[0]:
  '''
  ### Estadísticas y Análisis:

    - Sumérgete en estadísticas detalladas y métricas generales para evaluar el rendimiento académico y la eficiencia operativa.

    - Utiliza herramientas de hoja de cálculo y SQL para un análisis personalizado y profundo de los datos.

  '''

with cols3[1]:
  st.image("https://miro.medium.com/v2/resize:fit:1400/1*cXdJh394X6YIzRCvXsaJzg.gif", width=300)



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
''',unsafe_allow_html=True)

#Defaul images
URL1 = "https://pbs.twimg.com/media/CLGIjQQUwAEoXvH.jpg"

URL2 = "https://www.cecytemchimalhuacan.com/wp-content/uploads/2019/11/Banner-1024x363.png"

URL3 = "https://cecytem.edomex.gob.mx/sites/cecytem.edomex.gob.mx/files/images/TEQUIXQUIAC.jpg"

URL4 = "https://asisucede.com.mx/wp-content/uploads/2022/01/educacion.jpeg"

URL5 = "https://s3.amazonaws.com/rytvmx/wpmedia/2022/01/04202709/WhatsApp-Image-2022-01-04-at-1.53.09-PM-2.jpeg"


urlpreba3 = "https://images.unsplash.com/photo-1503631285924-e1544dce8b28?auto=format&fit=crop&w=1234&q=80"
urlpreba1 = 'https://images.unsplash.com/photo-1499198116522-4a6235013d63?auto=format&fit=crop&w=1233&q=80'
urlpreba2 = 'https://images.unsplash.com/photo-1492760864391-753aaae87234?auto=format&fit=crop&w=1336&q=80'
urlpreba4 = 'https://images.unsplash.com/photo-1510425463958-dcced28da480?auto=format&fit=crop&w=1352&q=80'
urlpreba5 = 'https://images.unsplash.com/photo-1503602642458-232111445657?auto=format&fit=crop&w=1234&q=80'

if st.checkbox("Cambiar Imagenes") :
  st.markdown('<style>.item-1 {'+f'background-image: url({urlpreba1});'+'}</style>',unsafe_allow_html=True )
  st.markdown('<style>.item-2 {'+f'background-image: url({urlpreba2});'+'}</style>',unsafe_allow_html=True )
  st.markdown('<style>.item-3 {'+f'background-image: url({urlpreba3});'+'}</style>',unsafe_allow_html=True)
  st.markdown('<style>.item-4 {'+f'background-image: url({urlpreba4});'+'}</style>',unsafe_allow_html=True)
  st.markdown('<style>.item-5 {'+f'background-image: url({urlpreba5});'+'}</style>',unsafe_allow_html=True )
else:
  st.markdown('<style>.item-1 {'+f'background-image: url({URL1});'+'}</style>',unsafe_allow_html=True )
  st.markdown('<style>.item-2 {'+f'background-image: url({URL2});'+'}</style>',unsafe_allow_html=True )
  st.markdown('<style>.item-3 {'+f'background-image: url({URL3});'+'}</style>',unsafe_allow_html=True)
  st.markdown('<style>.item-4 {'+f'background-image: url({URL4});'+'}</style>',unsafe_allow_html=True)
  st.markdown('<style>.item-5 {'+f'background-image: url({URL5});'+'}</style>',unsafe_allow_html=True )



st.markdown('''

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
