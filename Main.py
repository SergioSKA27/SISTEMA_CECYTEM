import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac


st.set_page_config(page_title="Login", page_icon=":unlock:", layout="wide", initial_sidebar_state="collapsed")



st.markdown('''
<style>
body {
background-color: #e5e5f7;

}

[data-testid="collapsedControl"] {
        display: none
    }

#MainMenu, header, footer {visibility: hidden;}

.bg {
  animation:slide 20s ease-in-out infinite alternate;
  background-image: linear-gradient(315deg, #aee1f9 0%, #f6ebe6 74%);
  bottom:0;
  left:-50%;
  opacity:.5;
  position:fixed;
  right:-50%;
  top:0;
  z-index:0;
}

.bg2 {
  animation-direction:alternate-reverse;
  animation-duration:15s;
}

.bg3 {
  animation-duration:17s;
}

@keyframes slide {
  0% {
    transform:translateX(-25%);
  }
  100% {
    transform:translateX(25%);
  }
}
</style>


<div class="bg"></div>
<div class="bg bg2"></div>
<div class="bg bg3"></div>
''',unsafe_allow_html=True)





sac.alert(message='Bienvenido al Sistema de Gestion y Analisis CECYTEM',
description='Si no tienes usuario y contraseña, contacta con el administrador.', banner=True, icon=True, closable=True, height=100)

cols1 = st.columns([.5,.5])

with cols1[0]:
    st.image("rsc/back1.jpg",use_column_width=True)


with cols1[1]:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    authenticator.login('Login', 'main')
    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'main', key='unique_key')
        st.toast(f'Bienvenido {st.session_state["name"]}',icon='🔓')
        switch_page('Home')
        st.title('Some content')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Por favor, introduce tu usuario y contraseña')



i = sac.tags([
    sac.Tag(label='Contacto', icon='person-lines-fill', color='cyan', link='https://ant.design/components/tag'),

], format_func='title', align='center',)
