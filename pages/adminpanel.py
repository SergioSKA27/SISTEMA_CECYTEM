import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
from streamlit.components.v1 import iframe
from streamlit_agraph import agraph, Node, Edge, Config
import random
import pandas as pd
import streamlit_analytics
from streamlit_option_menu import option_menu
import asyncio
import concurrent.futures
import requests

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
st.set_page_config(page_title="Admin", page_icon=":shield:", layout="wide", initial_sidebar_state="collapsed")



#--------------------------------------------------
#Funciones

def query_users()->dict:
    """
    The function `query_users` queries a database to retrieve user information and returns it as a dictionary.
    :return: The function `query_users` returns a dictionary containing the records of users queried from the "Credentials"
    table in the database. The dictionary contains the following columns for each user: "id", "username", "email",
    "password", "avatar.url", "name", and "role".
    """
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.data().query("Credentials", {
        "columns": [
            "id",
            "username",
            "email",
            "password",
            "avatar.url",
            "name",
            "role"
        ]
    })
    d = data['records']
    for record in d:
        record['avatar'] = record['avatar']['url']
    return d

def random_color()->str:
    """
    The function `random_color` generates a random hexadecimal color code.
    :return: The function `random_color()` returns a randomly generated color in the format of a hexadecimal string.
    """
    # trunk-ignore(bandit/B311)
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def graph_agr():
    """
    The function `graph_agr` generates a graph visualization of a data structure in Python using the `agraph` library.
    :return: The function `graph_agr()` returns a graph visualization of a data structure.
    """
    nodes = [
        Node(id="Alumno", label="Alumno\n(id_controlAlumno, carreraAlumno, plantelAlumno)", shape="box", color="#3498db", size=20),
        Node(id="DataAlumno", label="DataAlumno\n(curp, nombre, apellidoPaterno, ...)", shape="box", color="#e74c3c", size=20),
        Node(id="TutorAlumno", label="TutorAlumno\n(id_TutorAlumno, curp, nombre, ...)", shape="box", color="#2ecc71", size=20),
        Node(id="SaludAlumno", label="SaludAlumno\n(id_SaludAlumno, enfermedad_estatus, ...)", shape="box", color="#f39c12", size=20),
        Node(id="DomicilioAlumno", label="DomicilioAlumno\n(id_DomicilioAlumno, calle, num_exterior, ...)", shape="box", color="#9b59b6", size=20),
        Node(id="ProcedenciaAlumno", label="ProcedenciaAlumno\n(id_ProcedenciaAlumno, clave_ceneval, ...)", shape="box", color="#34495e", size=20),
        Node(id="DocumentacionAlumno", label="DocumentacionAlumno\n(id_DocumentacionAlumno, Acta_nacimiento, ...)", shape="box", color="#e67e22", size=20),
        Node(id="EstatusAlumno", label="EstatusAlumno\n(id_EstatusAlumno, actual_estatus, ...)", shape="box", color="#1abc9c", size=20),
        Node(id="PromedioAlumno", label="PromedioAlumno\n(id_PromedioAlumno, promedio_general, ...)", shape="box", color="#d35400", size=20),
        Node(id="SeguroAlumno", label="SeguroAlumno\n(id_SeguroAlumno, asegurado_por, tipo_seguro, ...)", shape="box", color="#27ae60", size=20),
        Node(id="BecaAlumno", label="BecaAlumno\n(id_BecaAlumno, id_controlAlumno)", shape="box", color="#95a5a6", size=20),
        Node(id="ArchivosAlumno", label="ArchivosAlumno\n(id_archivo, id_controlAlumno, archivo, ...)", shape="box", color="#ecf0f1", size=20),
    ]

    edges = [
        Edge(source="Alumno", target="DataAlumno", label="curpAlumno", color="#3498db"),
        Edge(source="Alumno", target="EstatusAlumno", label="id_EstatusAlumno", color="#3498db"),
        Edge(source="Alumno", target="PromedioAlumno", label="id_PromedioAlumno", color="#3498db"),
        Edge(source="Alumno", target="SeguroAlumno", label="id_SeguroAlumno", color="#3498db"),
        Edge(source="DataAlumno", target="TutorAlumno", label="id_TutorAlumno", color="#e74c3c"),
        Edge(source="DataAlumno", target="SaludAlumno", label="id_SaludAlumno", color="#e74c3c"),
        Edge(source="DataAlumno", target="DomicilioAlumno", label="id_DomicilioAlumno", color="#e74c3c"),
        Edge(source="DataAlumno", target="ProcedenciaAlumno", label="id_ProcedenciaAlumno", color="#e74c3c"),
        Edge(source="DataAlumno", target="DocumentacionAlumno", label="id_DocumentacionAlumno", color="#e74c3c"),
        Edge(source="BecaAlumno", target="Alumno", label="id_controlAlumno", color="#95a5a6"),
        Edge(source="ArchivosAlumno", target="Alumno", label="id_controlAlumno", color="#ecf0f1"),
    ]

    config = Config(width=1200, height=350,
    directed=True, physics=True, hierarchical=False,
    collapsible=True, nodeHighlightBehavior=True,
    highlightColor="#F7A7A6",
    node={'labelProperty': 'label'},link={'labelProperty': 'label'},
    fit=True,nodeSpacing=1000, maxVelocity=50,Solver='hierarchicalRepulsion')

    return_value = agraph(nodes=nodes, edges=edges, config=config)
    return return_value


async def query_users_async():
    """
    The function `query_users_async` uses asyncio to run the `query_users` function in a separate thread and returns the
    result.
    :return: The function `query_users_async` is returning the data returned by the `query_users` function.
    """
    loop = asyncio.get_event_loop()

    with concurrent.futures.ThreadPoolExecutor() as pool:
        data = await loop.run_in_executor(pool, query_users)
        return data




#--------------------------------------------------
#Cuerpo de la pagina
#Authentication
if "authentication_status" not in st.session_state  :
    switch_page('Main')
else:
# el usuario debe estar autenticado para acceder a esta página
    if st.session_state["authentication_status"]:
        #st.session_state = get_current_user_info(st.session_state['username'])



        #--------------------------------------------------
        #Navbar
         # CSS style definitions
        selected3 = option_menu(None, ["Inicio", "Alumnos",  "Profesores","Vinculación", "Orientación",st.session_state.username,"Cerrar Sesión"],
               icons=['house', 'mortarboard', "easel2", 'link', 'compass', 'person-heart','door-open'],
               menu_icon="cast", default_index=1, orientation="horizontal",
               styles={
                   "container": {"padding": "0!important", "background-color": "#e6f2f0"},
                   "icon": {"color": "#1B7821", "font-size": "20px"},
                   "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#4F758C"},
                   "nav-link-selected": {"background-color": "#0F4C59"},
               },key='menu'
           )
        if selected3 == 'Inicio':
            switch_page('Inicio')
        elif selected3 == st.session_state.username:
            switch_page('Perfil')
        elif selected3 == 'Cerrar Sesión':
            st.session_state["authentication_status"] = False
            st.session_state["username"] = None
            st.session_state["name"] = None
            st.session_state["role"] = None
            st.session_state["record_id"] = None
            switch_page('Login')

        #-------------------------------------------------

        if st.session_state['role'] == 'admin':
            data = asyncio.run(query_users_async())
            #--------------------------------------------------
            #Opciones de Administrador
            st.divider()
            st.subheader('Opciones de Administrador')
            colsop = st.columns(5)
            with colsop[0]:
                if st.button('Registra un usuario'):
                    switch_page('user_register')

            with colsop[1]:
                if st.button('Elimina un usuario'):
                    pass

            with colsop[2]:
                if st.button('Edita un usuario'):
                    pass

            with colsop[3]:
                if st.button('Genera reporte'):
                    pass
            with colsop[4]:
                if st.button('Opciones de la pagina'):
                    pass
            st.divider()
        #Cuerpo de la pagina
            st.title('Panel de Administrador')
            st.divider()
            #--------------------------------------------------
            #Administrar Usuarios
            st.header('Administrar Usuarios')
            st.dataframe(pd.DataFrame(data),use_container_width=True,
            column_config={'avatar': st.column_config.ImageColumn( "Preview Image",
            help="Streamlit app preview screenshots") },hide_index=True)



            #--------------------------------------------------
            #Diagrama de la base de datos
            st.header('Diagrama de la base de datos')
            #Para Los desarrolladores y administradores en
            st.markdown(r"""<iframe width="1000" height="315" src='https://dbdiagram.io/e/65597c3c3be149578745fdcf/6559b1063be1495787470237'> </iframe>""",unsafe_allow_html=True)
            if not st.checkbox('Grafo Interactivo'):
                st.graphviz_chart('''
                digraph G {
                  // Definición de las tablas
                  Alumno [label="Alumno\n(id_controlAlumno, carreraAlumno, plantelAlumno)", shape=box];
                  DataAlumno [label="DataAlumno\n(curp, nombre, apellidoPaterno, ...)", shape=box];
                  TutorAlumno [label="TutorAlumno\n(id_TutorAlumno, curp, nombre, ...)", shape=box];
                  SaludAlumno [label="SaludAlumno\n(id_SaludAlumno, enfermedad_estatus, ...)", shape=box];
                  DomicilioAlumno [label="DomicilioAlumno\n(id_DomicilioAlumno, calle, num_exterior, ...)", shape=box];
                  ProcedenciaAlumno [label="ProcedenciaAlumno\n(id_ProcedenciaAlumno, clave_ceneval, ...)", shape=box];
                  DocumentacionAlumno [label="DocumentacionAlumno\n(id_DocumentacionAlumno, Acta_nacimiento, ...)", shape=box];
                  EstatusAlumno [label="EstatusAlumno\n(id_EstatusAlumno, actual_estatus, ...)", shape=box];
                  PromedioAlumno [label="PromedioAlumno\n(id_PromedioAlumno, promedio_general, ...)", shape=box];
                  SeguroAlumno [label="SeguroAlumno\n(id_SeguroAlumno, asegurado_por, tipo_seguro, ...)", shape=box];
                  BecaAlumno [label="BecaAlumno\n(id_BecaAlumno, id_controlAlumno)", shape=box];
                  ArchivosAlumno [label="ArchivosAlumno\n(id_archivo, id_controlAlumno, archivo, ...)", shape=box];

                  // Definición de las relaciones
                  Alumno -> DataAlumno [label="curpAlumno"];
                  Alumno -> EstatusAlumno [label="id_EstatusAlumno"];
                  Alumno -> PromedioAlumno [label="id_PromedioAlumno"];
                  Alumno -> SeguroAlumno [label="id_SeguroAlumno"];

                  DataAlumno -> TutorAlumno [label="id_TutorAlumno"];
                  DataAlumno -> SaludAlumno [label="id_SaludAlumno"];
                  DataAlumno -> DomicilioAlumno [label="id_DomicilioAlumno"];
                  DataAlumno -> ProcedenciaAlumno [label="id_ProcedenciaAlumno"];
                  DataAlumno -> DocumentacionAlumno [label="id_DocumentacionAlumno"];

                  BecaAlumno -> Alumno [label="id_controlAlumno"];
                  ArchivosAlumno -> Alumno [label="id_controlAlumno"];
                }

            ''',use_container_width=True)
            else:
                graph_agr()

        else:
            st.title('Panel de Administrador')
            st.divider()
            st.header('No tienes permisos para ver esta pagina')
            st.subheader('Contacta al administrador para obtener permisos')
            st.image('https://media.giphy.com/media/3o7aDczQq9MJ0R2MlO/giphy.gif',use_column_width=True)
            st.balloons()

#Para ver estadisticas de la pagin usa '?analytics=on' en la url






