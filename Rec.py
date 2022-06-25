import streamlit as st
import pandas as pd
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

raww = pd.read_csv("anime.csv")
raw = pd.read_csv("anime_with_synopsis.csv")
raw = raw.rename(columns={"sypnopsis":"Synopsis"})
raw = raw[["MAL_ID","Synopsis"]]
raww = raww[["MAL_ID","Name","Score","Genres","English name","Type","Episodes","Premiered"]]
df = pd.merge(raw,raww, on="MAL_ID")
df = df[["MAL_ID","Name","Synopsis","Genres","Score","Type","Episodes","Premiered"]]

data = df[df["Type"].str.contains("TV")]

#df[df.isnull().any(axis=1)]
data = data.dropna()
data.isnull().sum()

data["Features"] = data["Synopsis"]+df["Genres"]

#FEauteres to matrix of token counts
cm =CountVectorizer().fit_transform(data["Features"])
cs = cosine_similarity(cm,cm)

indices = pd.Series(data.Name)

def rec(name,cs=cs):
    recnime =[]
    idx = indices[indices== name].index[0]
    
    score_series=pd.Series(cs[idx]).sort_values(ascending=False)

    top_10_indexes= list(score_series.iloc[1:4].index)

    for i in top_10_indexes:
        recnime.append(list(data.Name)[i])
    first = recnime[0]
    second = recnime[1]
    third = recnime[2]
    return (first,second,third)
    print(idx)
st.title("ANIREC")
col_one_list = data["Name"].tolist()
choice = st.selectbox("Pick", col_one_list)

st.write(rec(choice))



#UserI = st.text_input("Anime")
#rec(input)