#Data_cleaning.py>
import streamlit as st 
from ast import literal_eval
import streamlit as st 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from ast import literal_eval
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
st.subheader("Data Cleaning,Transformation,Visualization")
st.text("""
        Data cleaning or cleansing is the process of detecting and correcting (or removing) 
        corrupt or inaccurate records from a record set, table, or database and refers to identifying 
        incomplete, incorrect, inaccurate or irrelevant parts of the data and then replacing, modifying, 
        or deleting the dirty or coarse data.
    
        Data transformation is a crucial step in the data analysis process, allowing us to convert raw 
        data into a more suitable format for analysis and visualization.
        
        Data visualization provides a good, organized pictorial representation of the data which makes 
        it easier to understand, observe, analyze.
        
        """)



movies=pd.read_csv(r"C:\Users\ritaj\OneDrive\Desktop\2nd semster\Netflix Movie\archive (5)\credits.csv")
credits=pd.read_csv(r"C:\Users\ritaj\OneDrive\Desktop\2nd semster\Netflix Movie\archive (5)\titles.csv")
data=movies.merge(credits,how='inner',on='id')
data=pd.DataFrame(data)
data['genres']=data['genres'].apply(literal_eval)
data=data.explode('genres',ignore_index=True)
st.subheader("what do you want to see?")
menu=['General Information of the data','Data_cleaning & Transformation','Data_Visualization']
choice=st.selectbox("menu",menu)



data['genres']=data['genres'].replace(" ","")
def information(data):
        st.write("1.Check the information of the data")
        st.dataframe(data.describe())
        st.write("2.Check the null values in the data")
        df=pd.DataFrame(data=data.isna().sum(),columns=['Total_number_Missing_Values'])
        st.table(df)
        st.write("3.Check How many columns we have?")
        df2=pd.DataFrame(data=data.columns,columns=['column_name'])
        st.write(df2)
        st.write("4.what kind of data type we have per each columns?")
        st.write(data.dtypes)
        st.write("5.general information about the data")
        st.write(df.describe())
def cleaning_transformation(data):
     st.subheader("This is stepwise explanation of Data Cleaning steps")
     st.write("1. Drop duplicate,saving the first one and drop unneccesary columns")
     data=data.drop_duplicates(keep='first')
     data.drop(['seasons','runtime','imdb_votes'],axis=1,inplace=True)
     st.write(data.head())
     st.write("2. convert data types to the nearest one")
     data=data.convert_dtypes(infer_objects=True, convert_string=True, convert_integer=True, convert_boolean=True, convert_floating=True)
     st.write(data.dtypes)
     data['release_year']=pd.to_datetime(data['release_year'])
     st.write("3. substitute missing values")
     data['imdb_score'].fillna(data['imdb_score'].mean(),inplace=True)
     data['tmdb_popularity'].fillna(data['tmdb_popularity'].mean(),inplace=True)
     data['tmdb_score'].fillna(data['tmdb_score'].mean(),inplace=True)
     st.write(data.isna().sum())
     st.write(data.head())
     data.dropna(inplace=True)
     st.write("4. Check the data type of the data")
     st.write(data.dtypes)
     st.write("5. Check the data for null values")
     st.write(data.isna().sum())
     st.write("6. check the overall data")
     df=pd.DataFrame(data)
     st.write(df.describe()) 
     return df
     
def cleaned(data):
    data=data.drop_duplicates(keep='first')
    data.drop(['seasons','runtime','imdb_votes'],axis=1,inplace=True)   
    data=data.convert_dtypes(infer_objects=True, convert_string=True, convert_integer=True, convert_boolean=True, convert_floating=True)
    data['release_year']=pd.to_datetime(data['release_year'])
    data['imdb_score'].fillna(data['imdb_score'].mean(),inplace=True)
    data['tmdb_popularity'].fillna(data['tmdb_popularity'].mean(),inplace=True)
    data['tmdb_score'].fillna(data['tmdb_score'].mean(),inplace=True)
    data.dropna(inplace=True)
    
    
def viz(data):
    ###########################################################################
    st.write("1.which type of broadcast video are popular??")
    
    fig1=plt.figure(figsize=(9,7))
    plt.pie(data.type.groupby(data.type).count(),labels=data.type.unique())
    plt.title("Movies Popularity per genres")
    st.pyplot(fig1)
    plt.gcf()
    ###########################################################################
    st.write("2.which type of movies genres are popular?")
    fig2=plt.figure(figsize=(9,7))
    index=data.genres.dropna().unique()
    sns.barplot(data,y=index,x=data.genres.groupby(data.genres).count().sort_values(ascending=False))
    plt.title("Movies popularity per genres")
    st.pyplot(fig2)
    plt.gcf()
    ###########################################################################
    st.write("3.The distribution of movies produced per age-certification as well as I should check this and correct it Note:-we want to see the distribution of key metrics per age_certification")
   ############################################################################
    fig3=plt.figure(figsize=(9,7))
    sns.barplot(data=data.dropna(inplace=True),x=data.age_certification.unique(),y=data['age_certification'].groupby(data.age_certification).count())
    plt.title('movie_distribution per age varaition')
    st.pyplot(fig3)
    plt.gcf()
    ###########################################################################
    st.subheader("Movies Genre and respective score")
    ###########################################################################
    st.write("4.which movies genres have high tmdb_popularity?")
    fig4=plt.figure(figsize=(9,7))
    sns.histplot(data=data,y=data.genres,x=data.tmdb_popularity.sort_values(ascending=False),hue=data.genres)
    plt.title('movies genres have high score of tmdb_popularity') 
    st.pyplot(fig4)
    plt.gcf()
    ###########################################################################
    st.write('5.which movies genres have high imdb_score?')
    ###########################################################################
    fig5=plt.figure(figsize=(9,7))
    sns.barplot(data=data,y=data.genres,x=data.imdb_score.sort_values(ascending=False))
    plt.title('movies genres have high score of imdb_score') 
    st.pyplot(fig5)
    plt.gcf()
    
    ###########################################################################
    st.write('6.which movies genres have high tmdb_score?')
    ###########################################################################
    fig6=plt.figure(figsize=(9,7))
    sns.violinplot(data=data,y=data.genres,x=data.tmdb_score.sort_values(ascending=False))
    plt.title('movies genres have high score of tmdb_score')
    st.pyplot(fig6)
    plt.gcf()
    
    
    
    

if choice=='General Information of the data':
    
    if st.button('yes'):
        st.write("Do you want to check the general information of the data?")
        information(data)
    
elif choice=='Data_cleaning & Transformation':
    
    if st.button('yes'):
        st.write("Do you want to check the stepwise process of cleaning and transforming data?")
        cleaning_transformation(data)
    
    
elif choice=='Data_Visualization':
    
    if st.button('yes'):
        st.write("Do you want the visualization of cleaned data?")
        cleaned(data)
        viz(data)
        
    
        


