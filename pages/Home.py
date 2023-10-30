import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac




if st.session_state["authentication_status"]:
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )
        authenticator.logout('Logout', 'main', key='unique_key')
        if not  st.session_state["authentication_status"]:
            switch_page('Main')

        st.toast(f'Bienvenido {st.session_state["name"]}',icon='🔓')
        st.title('Some content')

        with st.sidebar.empty():
            sac.menu([

                sac.MenuItem('home', icon='house-fill'),

                sac.MenuItem('products', icon='box-fill', children=[

                sac.MenuItem('apple', icon='apple', tag=sac.Tag('USA', color='green', bordered=False)),

                    sac.MenuItem('other', icon='git', children=[

                        sac.MenuItem('google', icon='google'),

                        sac.MenuItem('gitlab', icon='gitlab'),

                        sac.MenuItem('wechat' * 5, icon='wechat'),

                    ]),

                ]),

                sac.MenuItem('disabled', icon='send', disabled=True),

                sac.MenuItem(type='divider'),

                sac.MenuItem('reference', type='group', children=[

                    sac.MenuItem('antd-menu', icon='heart-fill', href='https://ant.design/components/menu#menu'),

                    sac.MenuItem('bootstrap-icon', icon='bootstrap', href='https://icons.getbootstrap.com/'),

                ]),

            ], format_func='title', open_all=True, return_index=True)
