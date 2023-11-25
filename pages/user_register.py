import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import uuid
import base64
import re
from streamlit_option_menu import option_menu

#Configuracion de la pagina
st.set_page_config(page_title="Login", page_icon=":lock:", layout="wide", initial_sidebar_state="collapsed")

#--------------------------------------------------
#Funciones


@st.cache_data
def verificar_contrasena(contrasena: str)->(bool, int):
    """
    The function `verificar_contrasena` checks the security level of a password based on various criteria and returns a
    boolean indicating if the password is valid and an integer representing the security level.

    :param contrasena: The parameter `contrasena` is a string that represents the password that needs to be verified
    :type contrasena: str
    :return: The function `verificar_contrasena` returns a tuple containing two values: a boolean value indicating whether
    the password is valid or not, and an integer value representing the security score of the password.
    """
    seguridad = 0
    es_valida = True

    # Criterios para evaluar la seguridad de la contraseña
    longitud_minima = 8
    tiene_mayusculas = any(c.isupper() for c in contrasena)
    tiene_minusculas = any(c.islower() for c in contrasena)
    tiene_digitos = any(c.isdigit() for c in contrasena)
    tiene_caracter_especial = any(c in "!@#$%^&*()-_+=<>,.?/:;{}[]" for c in contrasena)

    # Evaluar la longitud de la contraseña
    if len(contrasena) < longitud_minima:
        es_valida = False

    # Evaluar otros criterios y asignar puntos
    seguridad += tiene_mayusculas
    seguridad += tiene_minusculas
    seguridad += tiene_digitos
    seguridad += tiene_caracter_especial

    return es_valida, seguridad

@st.cache_data
def validar_correo(correo: str)->bool:
    """
    The function `validar_correo` uses regular expressions to validate an email address.

    :param correo: The parameter "correo" is a string that represents an email address
    :type correo: str
    :return: a boolean value. It returns True if the given email address is valid according to the regular expression
    pattern, and False otherwise.
    """
    # Expresión regular para validar correos electrónicos
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Usar re.match() para validar el correo
    if re.match(patron, correo):
        return True
    else:
        return False

@st.cache_data
def validar_nombre_usuario(nombre_usuario: str)->bool:
    """
    The function `validar_nombre_usuario` uses regular expressions to validate a username, ensuring it contains only letters
    (uppercase or lowercase), numbers, underscores, or hyphens, and has a length between 3 and 20 characters.

    :param nombre_usuario: The parameter `nombre_usuario` is a string that represents the username that needs to be
    validated
    :type nombre_usuario: str
    :return: a boolean value. It returns True if the given username is valid according to the specified pattern, and False
    otherwise.
    """
    # Expresión regular para validar nombres de usuario
    # Debe contener solo letras (mayúsculas o minúsculas), números, guiones bajos (_) o guiones (-)
    # Debe tener al menos 3 caracteres y no más de 20 caracteres
    patron = r'^[a-zA-Z0-9_-]{3,20}$'

    # Usar re.match() para validar el nombre de usuario
    if re.match(patron, nombre_usuario):
        return True
    else:
        return False

@st.cache_data
def verify_contraseña(con1: str,repcon1: str)->bool:
    """
    The function `verify_contraseña` verifies that the password entered by the user is valid.

    :param con1: The `con1` parameter is the password entered by the user.
    :param repcon1: The `repcon1` parameter is the password entered by the user again to verify that it is correct.
    :return: The function `verify_contraseña` returns a boolean value. If the passwords match, it returns `True`,
    indicating that the password is valid. Otherwise, it returns `False`, indicating that the password is invalid.
    """

    if con1 == repcon1 and  con1 >= 8:
        return True
    else:
        return False

@st.cache_data
def verifydata(data: dict)->bool:
    flag = True
    if data['username'] == '' or data['password'] == '':
        flag = False
    if not validar_correo(data['email']):
        flag = False
    if not validar_nombre_usuario(data['username']):
        flag = False

    if check_availability(data['username']) == False:
        flag = False

    if verificar_contrasena(data['password'])[0] == False:
        flag = False


    return flag

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


def check_availability(usrname: str)->bool:
    """
    The function `check_availability` checks if the username entered by the user is available.
    :return: The function `check_availability` returns a boolean value indicating whether the username is available or not.
    """
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    ch = xata.data().query("Credentials",{"filter": {"username": usrname}})

    if ch['records'] != []:
        return False
    else:
        return True

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

def register_user(data: dict)->bool:
    """
    The `register_user` function registers a user by inserting their credentials into a database and returns `True` if the
    registration is successful, otherwise `False`.

    :param data: The `data` parameter is a dictionary that contains the user's registration information. It includes the
    following keys:
    :return: The function `register_user` returns a boolean value. If the verification query returns any records, it returns
    `True`, indicating that the user registration was successful. Otherwise, it returns `False`, indicating that the user
    registration failed.
    """

    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    data = xata.records().insert("Credentials", {
        "username": data['username'],
        "email": data['email'],
        "password": stauth.Hasher(data['password']).generate()[0],
        "avatar": {
                    "base64Content":data['avatar'],
                    "enablePublicUrl": True,
                    "mediaType": "application/octet-stream",
                    "name": f"{data['name']}_avatar.jpg",
                    "signedUrlTimeout": 300
                },
        "name": data['name'],
        "role": data['role']})

    #verf = xata.data().query("Credentials",{"filter": {"username": data['username']}})


    return True, data


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



# Add on_change callback
def on_change(key):
    selection = st.session_state[key]
    st.write(f"Selection changed to {selection}")

#--------------------------------------------------
#Variables de Session

if 'usrname' not in st.session_state:
    st.session_state.usrname = ''

if 'correo' not in st.session_state:
    st.session_state.correo = ''

if 'name' not in st.session_state:
    st.session_state.name = ''

if 'password' not in st.session_state:
    st.session_state.password = ''

if 'reppas' not in st.session_state:
    st.session_state.reppas = ''

if 'avatar' not in st.session_state:
    st.session_state.avatar = ''

if 'datareg' not in st.session_state:
    st.session_state.datareg = None

if 'rol' not in st.session_state:
    st.session_state.rol = 'basic_user'

#--------------------------------------------------
#Credenciales de la base de datos

data = get_credentials()
credentials = credentials_formating(data['records'])


#--------------------------------------------------
#Pagina



#--------------------------------------------------
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

            st.title('Registro de usuario')
            st.divider()



            #Nombre de usuario
            usern = st.text_input('Nombre de usuario*',
help='Este nombre de usuario sera el que se utilizara para iniciar sesion, usa minuculas y no uses espacios ni caracteres especiales',
placeholder='Ejemplo: usuario123',value=st.session_state.usrname)

            if usern != '':
                st.session_state.usrname = usern.strip().lower()

            #Verificar disponibilidad del nombre de usuario
            if check_availability(usern.strip().lower()) == False and usern != '':
                st.error('Este nombre de usuario ya esta en uso')

            #Verificar que el nombre de usuario sea valido
            if not validar_nombre_usuario(usern.strip().lower()) and usern != '':
                st.error('El nombre de usuario no es valido')

            #Correo electronico
            email = st.text_input('Correo electronico*',placeholder="",value=st.session_state.correo)

            if email != '':
                st.session_state.correo = email.strip()

            #Verificar que el correo electronico sea valido
            if not validar_correo(email) and email != '':
                st.error('El correo electronico no es valido')

            #Nombre completo
            nombre = st.text_input('Nombre completo*',help='Escribe tu nombre completo',value=st.session_state.name)

            #Contraseña
            password = st.text_input('Contraseña*',type='password',help='La contraseña debe tener al menos 8 caracteres y no debe contener espacios',value=st.session_state.password)

            if password != '':
                st.session_state.password = password.strip()

            reppas = st.text_input('Repite tu contraseña*',type='password',value=st.session_state.reppas)

            if reppas != '':
                st.session_state.reppas = reppas.strip()

            if (password != '' and reppas != '') and password == reppas:
                val, score = verificar_contrasena(password)
                if val == False:
                    st.error('La contraseña no es valida')
                else:
                    st.success('La contraseña es valida')
                    if score <= 2:
                        st.warning('La contraseña es debil')
                    elif score == 3:
                        st.info('La contraseña es regular')
                    else:
                        st.success('La contraseña es fuerte')



            #Imagen de perfil

            avatar = st.file_uploader('Imagen de perfil',type=['png','jpg','jpeg'])
            #Verificar que la imagen de perfil sea valida
            if avatar is not None:
                st.image(avatar,width=200)
                avatar = base64.b64encode(avatar.read()).decode()
                st.session_state.avatar = avatar
            else:
                avatar = base64.b64encode(open('rsc/avatars/PG.png','rb').read()).decode()
                st.image(open('rsc/avatars/PG.png','rb').read(),width=200)
                st.session_state.avatar = avatar



            #Rol
            rol = st.selectbox('Rol',['basic_user','teacher','sub_admin','admin'], placeholder='Rol del usuario',index=0)

            st.session_state.rol = rol


            d = {'username': usern.strip().lower(),
                'email': email.strip(),
                'password': password.strip(),
                'avatar': avatar,
                'name': nombre,
                'role': rol}




            if st.button('Registrar'):

                if usern == '' or email == '' or nombre == '' or password == '' or reppas == '':
                    st.error('Por favor, llena todos los campos')
                else:
                    if verifydata(d):
                        reg = register_user(d)
                        st.subheader('Informacion del registro')
                        st.json(reg)
                        if reg[0]:
                            st.success('Usuario registrado correctamente')
                            st.session_state.datareg = d
                            st.session_state.usrname = ''
                            st.session_state.correo = ''
                            st.session_state.name = ''
                            st.session_state.password = ''
                            st.session_state.reppas = ''
                            st.session_state.avatar = ''
                            st.session_state.rol = 'basic_user'
                        else:
                            st.error('No se pudo registrar el usuario intentelo de nuevo')

        else:
            st.error('No tienes permisos para acceder a esta pagina')
            switch_page('Inicio')





