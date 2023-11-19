import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from xata.client import XataClient
import uuid
import base64

#Configuracion de la pagina
st.set_page_config(page_title="Login", page_icon=":lock:", layout="wide", initial_sidebar_state="collapsed")
if 'datareg' not in st.session_state:
    st.session_state.datareg = None
st.title('Registro de usuario')

with st.form(key='Registro de usuario',clear_on_submit=False):
    xata = XataClient(api_key=st.secrets['db']['apikey'],db_url=st.secrets['db']['dburl'])
    flag = True
    usern = st.text_input('Nombre de usuario',
    help='Este nombre de usuario sera el que se utilizara para iniciar sesion',
    placeholder='Ejemplo: usuario123')

    ch = xata.data().query("Credentials",{"filter": {"username": usern}})

    if ch['records'] != []:
        flag = False
        st.error('El usuario ya existe')

    email = st.text_input('Correo electronico',placeholder="alguien@example.com")
    name = st.text_input('Nombre completo')
    password = st.text_input('Contraseña',type='password',help='La contraseña debe tener al menos 8 caracteres y no debe contener espacios')
    if len(password) < 8 and password != '':
        flag = False
        st.error('La contraseña debe tener al menos 8 caracteres')

    reppas = st.text_input('Repite tu contraseña',type='password')

    if password != reppas and password != '' and reppas != '':
        flag = False
        st.error('Las contraseñas no coinciden')

    avatar = st.file_uploader('Imagen de perfil',type=['png','jpg','jpeg'])
    if avatar is not None:
        st.image(avatar,width=200)
        avatar = base64.b64encode(avatar.read()).decode()
    else:
        avatar = base64.b64encode(open('rsc/avatars/PG.png','rb').read()).decode()
        st.image(open('rsc/avatars/PG.png','rb').read(),width=200)

    rol = st.selectbox('Rol',['basic_user','teacher','sub_admin'], placeholder='Rol del usuario',index=0)
    sub =  st.form_submit_button('Registrar',disabled=False)

    if sub:
        if flag and usern != '' and email != '' and name != '' and password != '':
            data = xata.records().insert("Credentials", {
                "username": usern.strip(),
                "email": email.strip(),
                "password": stauth.Hasher([password.strip()]).generate()[0],
                "avatar": {
                    "base64Content":avatar,
                    "enablePublicUrl": False,
                    "mediaType": "application/octet-stream",
                    "name": f"{usern.strip()}_avatar.jpg",
                    "signedUrlTimeout": 300
                },
                "name": name,
                "role": 'basic_user'


            })
            st.session_state.datareg = data

if st.session_state.datareg is not None:
    st.success('Usuario registrado')
    st.write(st.session_state.datareg)
