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

#Configuracion de la pagina
st.set_page_config(page_title="Admin", page_icon=":shield:", layout="wide", initial_sidebar_state="collapsed")



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

def get_current_user_info(usrname: str)->dict:
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
    return data['records']

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

# Add on_change callback
def on_change(key):
    selection = st.session_state[key]
    st.write(f"Selection changed to {selection}")


@st.cache_data
def credentials_formating(credentials: list)->dict:
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





#--------------------------------------------------
#Credenciales de la base de datos

data = get_credentials()
credentials = credentials_formating(data['records'])





#--------------------------------------------------
#Cuerpo de la pagina
#Authentication
if "authentication_status" not in st.session_state  :
    switch_page('Main')
else:
# el usuario debe estar autenticado para acceder a esta página
    if st.session_state["authentication_status"]:
        usrdata = get_current_user_info(st.session_state['username'])




            # Menu de navegacion
        selected3 = option_menu(None, ["Inicio", "Alumnos",  "Profesores", 'Perfil'],
            icons=['house', 'cloud-upload', "list-task", 'gear'],
                menu_icon="cast", default_index=0, orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "25px"},
                    "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "green"},
                },on_change=on_change,key='menu'
            )




            #usrdata
        #--------------------------------------------------
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        authenticator = stauth.Authenticate(
                {'usernames':credentials},
                config['cookie']['name'],
                config['cookie']['key'],
                config['cookie']['expiry_days'],
                config['preauthorized']
            )

        authenticator.logout('Cerrar Sesión', 'main', key='unique_key')

        if usrdata['role'] == 'admin':
            data = query_users()
            #data
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
            st.dataframe(pd.DataFrame(data))


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






