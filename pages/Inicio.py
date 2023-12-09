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
from streamlit_lottie import st_lottie
import datetime
from mitosheet.streamlit.v1 import spreadsheet
from streamlit_calendar import calendar
from streamlit_elements import elements, mui, html
from streamlit_elements import elements, sync, event
import json
import asyncio
import concurrent.futures


from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace


from modules import Dashboard,Editor, Card, DataGrid, Radar, Pie, Player


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
st.set_page_config(page_title="Inicio", page_icon="rsc/Logos/cecytem-logo.png", layout="wide", initial_sidebar_state="collapsed")


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


def get_current_user_info(id):
    """
    The function `get_current_user_info` retrieves the information of the current user based on their username from a
    database.

    :param usrname: The `usrname` parameter is the username of the user whose information you want to retrieve
    :return: The function `get_current_user_info` returns the information of the current user specified by the `usrname`
    parameter.
    """
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.records().get("Credentials", id)
    return data

def get_manager():
    """
    The function `get_manager` returns a `CookieManager` object with the key 'MyCookieManager'.
    :return: an instance of the `CookieManager` class with the key set to 'MyCookieManager'.
    """
    return stx.CookieManager(key='MyCookieManager')



#--------------------------------------------------
#credenciales de la base de datos
cookie_manager = get_manager()

#--------------------------------------------------
#variables de Session State






#--------------------------------------------------
#Authentication
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] == False:
    switch_page('Main')
else:
# el usuario debe estar autenticado para acceder a esta página
    if st.session_state["authentication_status"]:
            #--------------------------------------------------
            #Ballons
            if 'ballons' not in st.session_state:
                st.session_state['ballons'] = False
                if datetime.datetime.now().year < 2025 or (datetime.datetime.now().month == 12 or datetime.datetime.now().month == 11):
                    if datetime.datetime.now().month == 12:
                        st.snow()
                    else:
                        st.balloons()
                else:
                    st.session_state.ballons = False


            #--------------------------------------------------
            #Notificaciones
            if 'notificationwelcome' not in st.session_state:
                st.session_state['notificationwelcome'] = False
                st.toast(f'Bienvenido {st.session_state["name"]}',icon='👋')
            #--------------------------------------------------
            #usrdata
            #usrdata = get_current_user_info(st.session_state['record_id'])
            #usrdata
            #--------------------------------------------------
            #Navbar
            # CSS style definitions
            selected3 = option_menu(None, ["Inicio", "Alumnos",  "Profesores","Vinculación", "Orientación",st.session_state.username,"Cerrar Sesión"],
                icons=['house', 'mortarboard', "easel2", 'link', 'compass', 'person-heart','door-open'],
                menu_icon="cast", default_index=0, orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#e6f2f0"},
                    "icon": {"color": "#FFFFFF", "font-size": "20px"},
                    "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#4F758C"},
                    "nav-link-selected": {"background-color": "#0F4C59"},
                },key='menu'
            )
            if selected3 == 'Alumnos':
                switch_page('AlumnosHome')
            elif selected3 == st.session_state.username:
                switch_page('Perfil')

            elif selected3 == 'Cerrar Sesión':
                st.session_state["authentication_status"] = False
                st.session_state["username"] = None
                st.session_state["name"] = None
                st.session_state["role"] = None
                st.session_state["record_id"] = None
                switch_page('Login')
            #--------------------------------------------------
            #Contenido de la pagina
            st.title('Sistema de Administración Escolar CECYTEM')
            sac.divider(label='',icon='house',align='center')
            if 'welcome' not in st.session_state:
                sac.alert(message=f'Bienvenido {st.session_state.name} al Sistema de Gestion y Analisis CECYTEM',
                description=f'Tu rol actual es {st.session_state["role"]} ', banner=True, icon=True, closable=True, height=100,type='success')

            #--------------------------------------------------
            #Dashboard de Inicio
            st.header('Noticias')
            if "w" not in state:
                board = Dashboard()
                args = {}
                args["board"] = board
                w = SimpleNamespace(
                    dashboard=board,
                    player=Player(board, 0, 0, 8, 12, minH=6),
                    card=Card(board, 8, 0, 4, 6, minW=4, minH=6),
                    card2=Card(board, 4, 12, 4, 6, minW=4, minH=6),
                    card3=Card(board, 0,12, 4, 6, minW=4, minH=6),
                    card4=Card(board, 8, 6, 4, 6, minW=4, minH=6),
                    card5=Card(board, 8, 12, 4, 6, minW=4, minH=6),

                )
                state.w = w


            else:
                w = state.w

            with elements("demo"):
                event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
                def handle_layout_change(updated_layout):
                    # You can save the layout in a file, or do anything you want with it.
                    # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
                    st.write(updated_layout)

                with w.dashboard(rowHeight=57, ):
                    w.player()
                    w.card("Este es un Anuncio",'data:image/png;base64,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')
                    w.card2('Anuncio 2','https://www.certus.edu.pe/blog/wp-content/uploads/2020/09/que-es-data-analytics-importancia-1-1200x720.jpg')
                    w.card3('Anuncio 3','https://www.certus.edu.pe/blog/wp-content/uploads/2020/09/que-es-data-analytics-importancia-1-1200x720.jpg')
                    w.card4('Anuncio 4','https://www.certus.edu.pe/blog/wp-content/uploads/2020/09/que-es-data-analytics-importancia-1-1200x720.jpg')
                    w.card5('Anuncio 5','https://www.certus.edu.pe/blog/wp-content/uploads/2020/09/que-es-data-analytics-importancia-1-1200x720.jpg')

                    x = w.dashboard.layout()
                    x
            #--------------------------------------------------
            #Calendario
            st.subheader('Calendario')
            mode = st.selectbox(
                "Tipo de Calendario:",
                (
                    "daygrid",
                    "timegrid",
                    "timeline",
                    "resource-daygrid",
                    "resource-timegrid",
                    "resource-timeline",
                    "list",
                    "multimonth",
                ),
            )

            events = [
                {
                    "title": "Event 1",
                    "color": "#FF6C6C",
                    "start": "2023-07-03",
                    "end": "2023-07-05",
                    "resourceId": "a",
                },
                {
                    "title": "Event 2",
                    "color": "#FFBD45",
                    "start": "2023-07-01",
                    "end": "2023-07-10",
                    "resourceId": "b",
                },
                {
                    "title": "Event 3",
                    "color": "#FF4B4B",
                    "start": "2023-07-20",
                    "end": "2023-07-20",
                    "resourceId": "c",
                },
                {
                    "title": "Event 4",
                    "color": "#FF6C6C",
                    "start": "2023-07-23",
                    "end": "2023-07-25",
                    "resourceId": "d",
                },
                {
                    "title": "Event 5",
                    "color": "#FFBD45",
                    "start": "2023-07-29",
                    "end": "2023-07-30",
                    "resourceId": "e",
                },
                {
                    "title": "Event 6",
                    "color": "#FF4B4B",
                    "start": "2023-07-28",
                    "end": "2023-07-20",
                    "resourceId": "f",
                },
                {
                    "title": "Event 7",
                    "color": "#FF4B4B",
                    "start": "2023-07-01T08:30:00",
                    "end": "2023-07-01T10:30:00",
                    "resourceId": "a",
                },
                {
                    "title": "Event 8",
                    "color": "#3D9DF3",
                    "start": "2023-07-01T07:30:00",
                    "end": "2023-07-01T10:30:00",
                    "resourceId": "b",
                },
                {
                    "title": "Event 9",
                    "color": "#3DD56D",
                    "start": "2023-07-02T10:40:00",
                    "end": "2023-07-02T12:30:00",
                    "resourceId": "c",
                },
                {
                    "title": "Event 10",
                    "color": "#FF4B4B",
                    "start": "2023-07-15T08:30:00",
                    "end": "2023-07-15T10:30:00",
                    "resourceId": "d",
                },
                {
                    "title": "Event 11",
                    "color": "#3DD56D",
                    "start": "2023-07-15T07:30:00",
                    "end": "2023-07-15T10:30:00",
                    "resourceId": "e",
                },
                {
                    "title": "Event 12",
                    "color": "#3D9DF3",
                    "start": "2023-07-21T10:40:00",
                    "end": "2023-07-21T12:30:00",
                    "resourceId": "f",
                },
                {
                    "title": "Event 13",
                    "color": "#FF4B4B",
                    "start": "2023-07-17T08:30:00",
                    "end": "2023-07-17T10:30:00",
                    "resourceId": "a",
                },
                {
                    "title": "Event 14",
                    "color": "#3D9DF3",
                    "start": "2023-07-17T09:30:00",
                    "end": "2023-07-17T11:30:00",
                    "resourceId": "b",
                },
                {
                    "title": "Event 15",
                    "color": "#3DD56D",
                    "start": "2023-07-17T10:30:00",
                    "end": "2023-07-17T12:30:00",
                    "resourceId": "c",
                },
                {
                    "title": "Event 16",
                    "color": "#FF6C6C",
                    "start": "2023-07-17T13:30:00",
                    "end": "2023-07-17T14:30:00",
                    "resourceId": "d",
                },
                {
                    "title": "Event 17",
                    "color": "#FFBD45",
                    "start": "2023-07-17T15:30:00",
                    "end": "2023-07-17T16:30:00",
                    "resourceId": "e",
                },
            ]
            calendar_resources = [
                {"id": "a", "building": "Edificio A", "title": "Salon 201"},
                {"id": "b", "building": "Edificio A", "title": "Salon 202"},
                {"id": "c", "building": "Edificio B", "title": "Salon 203"},
                {"id": "d", "building": "Edificio B", "title": "Salon 204"},
                {"id": "e", "building": "Edificio C", "title": "Salon 205"},
                {"id": "f", "building": "Edificio C", "title": "Salon 206"},
            ]

            calendar_options = {
                "editable": "true",
                "navLinks": "true",
                "resources": calendar_resources,
                'close': 'fa-times',
                 'prev': 'fa-chevron-left',
                  'ext': 'fa-chevron-right',
                  'revYear': 'fa-angle-double-left',
                  'extYear': 'fa-angle-double-right'
            }

            if "resource" in mode:
                if mode == "resource-daygrid":
                    calendar_options = {
                        **calendar_options,
                        "initialDate": datetime.datetime.now().strftime("%Y-%m-%d"),
                        "initialView": "resourceDayGridDay",
                        "resourceGroupField": "building",
                    }
                elif mode == "resource-timeline":
                    calendar_options = {
                        **calendar_options,
                        "headerToolbar": {
                            "left": "today prev,next",
                            "center": "title",
                            "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
                        },
                        "initialDate": "2023-07-01",
                        "initialView": "resourceTimelineDay",
                        "resourceGroupField": "building",
                    }
                elif mode == "resource-timegrid":
                    calendar_options = {
                        **calendar_options,
                        "initialDate": "2023-07-01",
                        "initialView": "resourceTimeGridDay",
                        "resourceGroupField": "building",
                    }
            else:
                if mode == "daygrid":
                    calendar_options = {
                        **calendar_options,
                        "headerToolbar": {
                            "left": "today prev,next",
                            "center": "title",
                            "right": "dayGridDay,dayGridWeek,dayGridMonth",
                        },
                        "initialDate": "2023-07-01",
                        "initialView": "dayGridMonth",
                    }
                elif mode == "timegrid":
                    calendar_options = {
                        **calendar_options,
                        "initialView": "timeGridWeek",
                    }
                elif mode == "timeline":
                    calendar_options = {
                        **calendar_options,
                        "headerToolbar": {
                            "left": "today prev,next",
                            "center": "title",
                            "right": "timelineDay,timelineWeek,timelineMonth",
                        },
                        "initialDate": "2023-07-01",
                        "initialView": "timelineMonth",
                    }
                elif mode == "list":
                    calendar_options = {
                        **calendar_options,
                        "initialDate": "2023-07-01",
                        "initialView": "listMonth",
                    }
                elif mode == "multimonth":
                    calendar_options = {
                        **calendar_options,
                        "initialView": "multiMonthYear",
                    }

            state = calendar(
                events=st.session_state.get("events", events),
                options=calendar_options,
                custom_css="""
                .fc-event-past {
                    opacity: 0.8;
                }
                .fc-event-time {
                    font-style: italic;
                }
                .fc-event-title {
                    font-weight: 700;
                }
                .fc-toolbar-title {
                    font-size: 2rem;
                }
                """,
                key=mode,
            )

            if state.get("eventsSet") is not None:
                st.session_state["events"] = state["eventsSet"]

            #st.write(state)

            st_lottie('https://lottie.host/204fe26b-ee80-4dfe-b95c-e1bcabbcf8ef/11JlAAyTKa.json',key='mainbanner')
    else:
        switch_page('Main')
