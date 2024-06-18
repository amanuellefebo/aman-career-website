import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
st.title("Movie Recommender Based on Content Filtering")
st.subheader("what is content based filtering?")
st.text("""
        Content-based recommenders: suggest similar items based on a particular item.This
        system uses item metadata, such as genre, director, description, actors, etc. for
        movies, to make these recommendations. The general idea behind these recommender
        systems is that if a person likes a particular item, he or she will also like an 
        item that is similar to it. And to recommend that, it will make use of the user's 
        past item metadata. A good example could be YouTube, where based on your history,
        it suggests you new videos that you could potentially watch.
        """)

movies=pd.read_csv(r"C:\Users\ritaj\OneDrive\Desktop\2nd semster\Netflix Movie\archive (5)\credits.csv")
credits=pd.read_csv(r"C:\Users\ritaj\OneDrive\Desktop\2nd semster\Netflix Movie\archive (5)\titles.csv")

movies_df=movies.merge(credits,how='inner',on='id')
index1=movies_df[movies_df.imdb_id.isna()==True].index
movies_df.drop(index1,inplace=True)
index2=movies_df[movies_df.description.isna()==True].index
movies_df.drop(index2,inplace=True)
index3=movies_df[movies_df.character.isna()==True].index
movies_df.drop(index3,inplace=True)
movies_df=movies_df.convert_dtypes(infer_objects=True, convert_string=True, convert_integer=True, convert_boolean=True, convert_floating=True)
print(movies_df.dtypes)
movies_db=movies_df[['description','title','genres','type']]
movies_db['text']=movies_db['genres']+" "+movies_db['description']
movies_db['description']=movies_db['description'].drop_duplicates(keep='first')
movies_db.dropna(inplace=True)
print(len(movies_db))
##############################################################################
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
################################################################################

def stem(txt):
    L=''
    ps=PorterStemmer()
    sw=stopwords.words('english')
    words=word_tokenize(txt)
    for w in words:
        if w not in sw:
            L=L+" "+(ps.stem(w))
    return L

###############################################################################
movies_db['stem_text'] = movies_db['text'].apply(stem)
###############################################################################
movies_db=movies_db.convert_dtypes(infer_objects=True, convert_string=True, convert_integer=True, convert_boolean=True, convert_floating=True)
##############################################################################
movies_db.reset_index(inplace=True)
print(movies_db.dtypes)
##############################################################################
cv=CountVectorizer()
vector=cv.fit(movies_db['stem_text'])
vector=vector.transform(movies_db['stem_text']).toarray()
dist_out= 1- pairwise_distances(vector,metric="cosine")
indices = pd.Series(movies_db.index, index= movies_db['title']).drop_duplicates()


###############################################################################
def recommender(title,cosine_value=dist_out):
    try:
        # get the index of the movies that match the title
        index= indices[title]
        #get pairwise similarity scores of all movies with the selected movies
        score= list(enumerate(dist_out[index]))
        # sort the movies based on the score
        sim_score=sorted(score,key= lambda x:x[1],reverse=True)

        # get the scores of the 10 most similar movies
        sim_score=sim_score[1:11]
        
        # get the movie indices
        movie_indices = [i[0] for i in sim_score]
        # return the top 10 most similar movies
        return movies_db['title'].iloc[movie_indices]
    except:
        
         st.write("The movie is not in our database or incorrect title used")
    
###############################################################################
with st.form("Search the movie"):
    title=st.text_input("Enter movie title")
     #Every form must have a submit button.
    submitted = st.form_submit_button(label="recommend") 
    if submitted:
         data=recommender(str(title).capitalize())
         data=pd.DataFrame(data=data)
         #data=data.convert_dtypes(infer_objects=True)
         df=pd.DataFrame(data=data)
         st.write(df)
    
    
