import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#write despliega texto,tablas y gráficas
st.write('Hello, :blue[world]! :sunglasses:')

df = pd.DataFrame(np.random.randn(10, 2), columns=('col1', 'col2'))


if 'nom' not in st.session_state:
    st.session_state['nom'] = 0
else:
    st.session_state['nom'] = st.session_state['nom'] +1

def cuadrado(x):
    return x**2

nom = st.number_input('Ingrese un número', value=st.session_state['nom'], max_value=10, min_value=0, step=1)
st.session_state['nom'] = nom
st.write(cuadrado(nom))
st.session_state
st.write(df)

'HOLA'

# Markdown despliega texto y html
st.markdown('**Hello, world!** :sunglasses:')


st.title('Titulo')
st.header('Header')
st.subheader('Subheader')
st.caption('Caption')
st.code('print("Hello, world!")')
st.write('Hola $f(x) = x^2$')
st.latex(r'''Hola e^{i\pi} + 1 = 0 ''')
st.divider()


st.dataframe(df)

st.data_editor(df)

st.table(df)

st.metric(label="Metric", value="Value", delta="Delta")


my_dic = {'one': [1, 2, 3], 'two': [4, 5, 6]}

st.json(my_dic)


st.area_chart(df)
st.bar_chart(df)
st.line_chart(df)
st.scatter_chart(df)

fig = go.Figure(data=go.Bar(y=[2, 3, 1]))

st.plotly_chart(fig)


if st.button('Say hello'):
    st.write('Why hello there')


b1 = st.button('Say hi')

if b1 == True:
    st.write('Why hello there')

st.download_button(label='Download data', data=df.to_csv(), file_name='data.csv', mime='text/csv')
st.link_button(label='Link to Streamlit', url='https://streamlit.io/')

check = st.checkbox('I am a checkbox')

if check == True:
    st.write('I am a checkbox')


tog = st.toggle('I am a toogle')

if tog == True:
    st.write('I am a toogle')



lista = st.radio('Pick one', ['one', 'two', 'three'])

st.write(lista)


selct = st.selectbox('Pick one', ['one', 'two', 'three'])
st.write(selct)

multisel = st.multiselect('Pick several', ['one', 'two', 'three'])

st.write(multisel)

sl = st.slider('Pick a number', min_value=0, max_value=10, value=5, step=1)
st.write(sl)

sll = st.slider('Pick a range of numbers', min_value=0.0, max_value=10.0, value=(2.0, 5.0), step=0.1)

st.write(sll)


name = st.text_input('Tell me your name', value='Name...')
st.write(name)


num = st.number_input('Tell me your number', value=1,max_value=10, min_value=0, step=1)
st.write(num)


ar =st.text_area('Text to analyze', height=200)
st.write(ar)


date = st.date_input('Date input',min_value=2000)
st.write(date)
