import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from streamlit_elements import elements, mui, html
from streamlit_elements import elements, sync, event




import json


from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace

from modules import Dashboard,Editor, Card, DataGrid, Radar, Pie, Player
#from .modules.elements import Dashboard, Editor, Card, DataGrid, Radar, Pie, Player




#Pagina de inicio visible para todos los usuarios con anuncios y noticias
st.set_page_config(page_title="Inicio", page_icon=":house:", layout="wide", initial_sidebar_state="collapsed")


#st.markdown('<style>' + open('./rsc/css/sidebar/style.css').read() + '</style>', unsafe_allow_html=True)

if "authentication_status" not in st.session_state:
    switch_page('Main')
else:
# el usuario debe estar autenticado para acceder a esta página
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

            st.toast(f'Bienvenido {st.session_state["name"]}',icon='👋')
            st.title('Some content')

            if "w" not in state:
                board = Dashboard()
                w = SimpleNamespace(
                    dashboard=board,
                    editor=Editor(board, 0, 0, 6, 11,),
                    player=Player(board, 7, 0, 4, 10, minH=5),
                    pie=Pie(board, 6, 0, 6, 7, minW=3, minH=4),
                    radar=Radar(board, 12, 7, 3, 7, minW=2, minH=4),
                    card=Card(board, 6, 7, 3, 7, minW=2, minH=4),
                    data_grid=DataGrid(board, 6, 13, 6, 7, minH=4),
                )
                state.w = w

                w.editor.add_tab("Card content", Card.DEFAULT_CONTENT, "plaintext")
                w.editor.add_tab("Data grid", json.dumps(DataGrid.DEFAULT_ROWS, indent=2), "json")
                w.editor.add_tab("Radar chart", json.dumps(Radar.DEFAULT_DATA, indent=2), "json")
                w.editor.add_tab("Pie chart", json.dumps(Pie.DEFAULT_DATA, indent=2), "json")
            else:
                w = state.w

            with elements("demo"):
                event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

                with w.dashboard(rowHeight=57):
                    w.editor()
                    w.player()
                    w.pie(w.editor.get_content("Pie chart"))
                    w.radar(w.editor.get_content("Radar chart"))
                    w.card(w.editor.get_content("Card content"))
                    w.data_grid(w.editor.get_content("Data grid"))



with elements("dashboard"):

    # You can create a draggable and resizable dashboard using
    # any element available in Streamlit Elements.

    from streamlit_elements import dashboard

    # First, build a default layout for every element you want to include in your dashboard

    layout = [
        # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
        dashboard.Item("first_item", 0, 0, 4, 3, isDraggable=True,isResizable=True),
        dashboard.Item("second_item", 0, 4, 6, 3, isDraggable=True, moved=False),
        dashboard.Item("third_item", 6, 0, 6, 3, isResizable=True,isDraggable=True),
        dashboard.Item("fourth_item", 6, 4, 4, 3, isResizable=True, isDraggable=True),
    ]

    # Next, create a dashboard layout using the 'with' syntax. It takes the layout
    # as first parameter, plus additional properties you can find in the GitHub links below.

    with dashboard.Grid(layout):
        from streamlit_elements import media

        with mui.Card(key="first_item", sx={"display": "flex", "flexDirection": "column", "borderRadius": 2, "overflow": "hidden"}, elevation=1):
            mui.CardHeader(
                title="Lorem ipsum dolor sit amet",
                subheader="date",
                avatar=mui.Avatar("U", sx={"bgcolor": "blue"}),
                action=mui.IconButton(mui.icon.MoreVert),

            )
            mui.CardMedia(
                component="img",
                height=194,
                image="https://cdn.analyticsvidhya.com/wp-content/uploads/2021/10/64750featred.jpg",
                alt="streamlit logo",
            )

            with mui.CardContent(sx={"flex": 1}):
                mui.Typography('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')

            with mui.CardActions(disableSpacing=True):
                mui.IconButton(mui.icon.Favorite)
                mui.IconButton(mui.icon.Share)


        with mui.Card(key="second_item", sx={"display": "flex", "flexDirection": "column", "borderRadius": 2, "overflow": "hidden"}, elevation=1):
            mui.CardHeader(
                title="Lorem ipsum dolor sit amet",
                subheader="date",
                avatar=mui.Avatar("U", sx={"bgcolor": "blue"}),
                action=mui.IconButton(mui.icon.MoreVert),

            )
            mui.CardMedia(
                component="img",
                height=194,
                image="https://cdn.analyticsvidhya.com/wp-content/uploads/2021/10/64750featred.jpg",
                alt="streamlit logo",
            )

            with mui.CardContent(sx={"flex": 1}):
                mui.Typography('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')

            with mui.CardActions(disableSpacing=True):
                mui.IconButton(mui.icon.Favorite)
                mui.IconButton(mui.icon.Share)
        #dashboard.card("Second item (cannot drag)",key="second_item")
        #mui.Paper("Third item (cannot resize)", key="third_item")

        with mui.Card(key="third_item", sx={"display": "flex", "flexDirection": "column", "borderRadius": 2, "overflow": "hidden"}, elevation=1):
            mui.CardHeader(
                title="Lorem ipsum dolor sit amet",
                subheader="Septiembre 22, 2023",
                avatar=mui.Avatar("S", sx={"bgcolor": "green"}),
                action=mui.IconButton(mui.icon.MoreVert),

            )
            mui.CardMedia(
                component="img",
                height=194,
                image="https://cdn.analyticsvidhya.com/wp-content/uploads/2021/10/64750featred.jp",
                alt="python logo",
            )

            with mui.CardContent(sx={"flex": 1}):
                mui.Typography('lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')

            with mui.CardActions(disableSpacing=True):
                mui.IconButton(mui.icon.Favorite)
                mui.IconButton(mui.icon.Share)

        with elements("nivo_charts"):
            # Streamlit Elements includes 45 dataviz components powered by Nivo.

            from streamlit_elements import nivo

            DATA = [
                { "taste": "fruity", "chardonay": 93, "carmenere": 61, "syrah": 114 },
                { "taste": "bitter", "chardonay": 91, "carmenere": 37, "syrah": 72 },
                { "taste": "heavy", "chardonay": 56, "carmenere": 95, "syrah": 99 },
                { "taste": "strong", "chardonay": 64, "carmenere": 90, "syrah": 30 },
                { "taste": "sunny", "chardonay": 119, "carmenere": 94, "syrah": 103 },
            ]

            with mui.Box(sx={"height": 500},key='fourth_item'):
                nivo.Radar(
                    data=DATA,
                    keys=[ "chardonay", "carmenere", "syrah" ],
                    indexBy="taste",
                    valueFormat=">-.2f",
                    margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
                    borderColor={ "from": "color" },
                    gridLabelOffset=36,
                    dotSize=10,
                    dotColor={ "theme": "background" },
                    dotBorderWidth=2,
                    motionConfig="wobbly",
                    legends=[
                        {
                            "anchor": "top-left",
                            "direction": "column",
                            "translateX": -50,
                            "translateY": -40,
                            "itemWidth": 80,
                            "itemHeight": 20,
                            "itemTextColor": "#999",
                            "symbolSize": 12,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ]
                        }
                    ],
                    theme={
                        "background": "#FFFFFF",
                        "textColor": "#31333F",
                        "tooltip": {
                            "container": {
                                "background": "#FFFFFF",
                                "color": "#31333F",
                            }
                        }
                    }
                )


with elements("media_player"):
    # Play video from many third-party sources: YouTube, Facebook, Twitch,
    # SoundCloud, Streamable, Vimeo, Wistia, Mixcloud, DailyMotion and Kaltura.
    #
    # This element is powered by ReactPlayer (GitHub link below).
    from streamlit_elements import media
    media.Player(url="https://www.youtube.com/watch?v=iik25wqIuFo", controls=True,key="fitfh_item")


