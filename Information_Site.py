from json import JSONDecodeError
import json
import streamlit as st
import requests
import pandas as pd
from PIL import Image
st.title("Movie Information Checker")
st.write("which movie do you want to check?")

def get_data():
    
    with st.form("Search the movie"):
         title=st.text_input("search title")
         submitted = st.form_submit_button(label="search")
         
         
         if submitted:
             #url=f'http://www.omdbapi.com/?i=tt3896198&apikey=64b5194b'
             url=f'http://www.omdbapi.com/?t={title}&apikey=64b5194b'
             resp=requests.get(url)
             resp.raise_for_status()
             data=resp.text
             #st.write(data)
             data1=json.loads(data)
             
             ###poster_url
             poster_url=data1["Poster"]
             st.subheader("Year of production")
             year=data1['Year']
             Genres=data1['Genre']
             Award=data1['Awards']
             Actors=data1['Actors']
             Rating=data1['imdbRating']
             Description=data1['Plot']
             index=['year','Genres','Award','rating','Description']
             df=pd.DataFrame(data=[year,Genres,Award,Rating,Description],index=index)
             #st.write(poster_url)
             st.table(df)
             poster_content=requests.get(poster_url).content
             
             
             with open(f'(title)_poster.jpg',mode='wb') as file:
                 file.write(poster_content)
                 st.image(Image.open('(title)_poster.jpg'))
        
data=get_data()

