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
import bcrypt
import asyncio
import concurrent.futures
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
st.set_page_config(page_title="Login", page_icon=":lock:", layout="wide", initial_sidebar_state="collapsed")

#--------------------------------------------------
#Funciones



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

def verifydata(data: dict)->bool:
    """
    The function `verifydata` checks if the given data dictionary contains valid values for username, password, email, and
    if the username is available.

    :param data: The `data` parameter is a dictionary that contains the following keys:
    :type data: dict
    :return: a boolean value.
    """
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




async def check_availability(usrname: str)->bool:
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

async def register_user(data: dict)->bool:
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
        "password": bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode(),
        "avatar": {
                    "base64Content":data['avatar'],
                    "enablePublicUrl": True,
                    "mediaType": "application/octet-stream",
                    "name": f"{data['name']}_avatar.jpg",
                    "signedUrlTimeout": 300
                },
        "name": data['name'],
        "role": data['role']})




    return data


async def verify_user(username: str):
    task = asyncio.create_task(check_availability(username))

    data = await task

    return data

async def reg_user_async(data: dict):
    task = asyncio.create_task(register_user(data))
    data = await task
    return data

#--------------------------------------------------
#Authentication

if "authentication_status" not in st.session_state:
    switch_page('Main')
else:
# el usuario debe estar autenticado para acceder a esta página
    if st.session_state["authentication_status"]:



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
        elif selected3 == 'Cerrar Sesión':
            st.session_state["authentication_status"] = False
            st.session_state["username"] = None
            st.session_state["name"] = None
            st.session_state["role"] = None
            st.session_state["record_id"] = None
            switch_page('Login')
        elif selected3 == 'Alumnos':
            switch_page('AlumnosHome')


        logcols = st.columns([0.2,0.6,0.2])
        with logcols[0]:
            backpp = sac.buttons([sac.ButtonsItem(label='REGRESAR',icon='skip-backward-btn')],
            position='left', format_func='upper', align='center', size='large',shape='round', return_index=True,index=1)

            if backpp == 0:
                switch_page('adminpanel')

        if st.session_state['role'] == 'admin':

            st.title('Registro de usuario')
            sac.divider(label='',icon='person-plus',align='center')
            flag_Reg = True


            #--------------------------------------------------
            #Nombre de usuario
            usern = st.text_input('Nombre de usuario*',placeholder='Ejemplo: usuario123',value='',
            help='Este nombre de usuario sera el que se utilizara para iniciar sesion, usa minuculas y no uses espacios ni caracteres especiales')


            #Verificar disponibilidad del nombre de usuario
            if asyncio.run(verify_user(usern.strip())) == False and usern != '':
                st.error('Este nombre de usuario ya esta en uso')
                flag_Reg = False

            #Verificar que el nombre de usuario sea valido
            if not validar_nombre_usuario(usern.strip().lower()) and usern != '':
                st.error('El nombre de usuario no es valido')
                flag_Reg = False

            #--------------------------------------------------
            #Correo electronico
            email = st.text_input('Correo electronico*',placeholder='Ejemplo: alguien@example.com',value='',
            help='Ingresa un correo electronico valido')


            #Verificar que el correo electronico sea valido
            if not validar_correo(email.strip()) and email != '':
                st.error('El correo electronico no es valido')
                flag_Reg = False

            #--------------------------------------------------
            #Nombre completo
            nombre = st.text_input('Nombre completo*',help='Escribe tu nombre completo',value='',placeholder='Ejemplo: Juan Perez')

            #--------------------------------------------------
            #Contraseña
            password = st.text_input('Contraseña*',type='password',value='',
            help='La contraseña debe tener al menos 8 caracteres y no debe contener espacios')


            #Verificar que la contraseña sea valida
            reppas = st.text_input('Repite tu contraseña*',type='password',value='',
            help='Repite la contraseña para verificar que sea correcta')



            if (password.strip() != '' and reppas.strip() != '') and password.strip() == reppas.strip():
                val, score = verificar_contrasena(password.strip())
                if val == False:
                    st.error('La contraseña no es valida')
                    flag_Reg = False
                else:
                    st.success('La contraseña es valida')
                    if score <= 2:
                        st.warning('La contraseña es debil')
                    elif score == 3:
                        st.info('La contraseña es regular')
                    else:
                        st.success('La contraseña es fuerte')
            elif password.strip() != reppas.strip() and password.strip() != '' and reppas.strip() != '':
                st.error('Las contraseñas no coinciden')
                flag_Reg = False


            #--------------------------------------------------
            #Imagen de perfil

            avatar = st.file_uploader('Imagen de perfil',type=['png','jpg','jpeg'])
            #Verificar que la imagen de perfil sea valida
            if avatar is not None:
                try:
                    st.image(avatar,width=200)
                    _avatar = base64.b64encode(avatar.read()).decode()
                except:
                    st.error('No se pudo cargar la imagen o el formato no es valido')
                    flag_Reg = False
            else:
                _avatar = base64.b64encode(open('rsc/avatars/PG.png','rb').read()).decode()
                st.image(open('rsc/avatars/PG.png','rb').read(),width=200)




            #Rol
            rol = st.selectbox('Rol',['basic_user','vinculacion','maestro','orientacion','admin'], placeholder='Rol del usuario',index=0)



            d = {'username': usern.strip().lower(),
                'email': email.strip(),
                'password': password.strip(),
                'avatar': _avatar,
                'name': nombre,
                'role': rol}




            if st.button('Registrar'):

                if flag_Reg == False:
                    st.error('Verifica que los datos sean correctos')
                else:
                    if verifydata(d):
                        with st.spinner('Registrando usuario...'):
                            reg = asyncio.run(reg_user_async(d))
                        st.json(reg)
                        if 'message' in reg:
                            st.error('Ocurrio un error al registrar el usuario')
                        else:
                            st.success('Usuario registrado correctamente')
                            st.balloons()

        else:
            st.error('No tienes permisos para acceder a esta pagina')
            switch_page('Inicio')

    else:
        switch_page('Login')



