import streamlit as st
import pandas as pd
from io import StringIO

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)


btn = st.download_button(
            label="Download image",
            data=file,
            file_name="https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fen%2Fthumb%2Fe%2Fe2%2FIMG_Academy_Logo.svg%2F640px-IMG_Academy_Logo.svg.png&tbnid=pdSATE7nqfTDiM&vet=12ahUKEwj-xJ-e_smCAxV1NN4AHes7BUgQMygBegQIARBs..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FIMG_Academy&docid=r6Vx2lLW0GRdzM&w=640&h=640&q=img&ved=2ahUKEwj-xJ-e_smCAxV1NN4AHes7BUgQMygBegQIARBs",
            mime="image/png"
          )
