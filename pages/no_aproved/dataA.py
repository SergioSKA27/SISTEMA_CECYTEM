import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
from streamlit_elements import elements, mui, html
from streamlit_elements import elements, sync, event
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from mitosheet.streamlit.v1 import spreadsheet

#Student ID,student_name,gender,grade,school_name,reading_score,math_score
data = pd.read_csv('students_complete.csv')



# Display the dataframe in a Mito spreadsheet, no puede tener mas de 1500 filas
final_dfs, code = spreadsheet(data)

# Display the final dataframes created by editing the Mito component
# This is a dictionary from dataframe name -> dataframe
st.write(final_dfs)

# Display the code that corresponds to the script
st.code(code)
