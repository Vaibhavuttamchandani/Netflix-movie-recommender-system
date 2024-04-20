import streamlit as st 
import pickle
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

st.header("Movie Recommender System")

import streamlit.components.v1 as components

# Corrected the path with a raw string
imageCarouselComponent = components.declare_component("image-carousel-component", path=r"C:\Users\VAIBHAV\Desktop\netflix\frontend\frontend\public")

imageUrls = [
    fetch_poster(movie_id) for movie_id in [
        1632, 299536, 17455, 2830, 429422, 9722, 13972, 240, 155, 598, 914, 255709, 572154
    ]
]

imageCarouselComponent(imageUrls=imageUrls, height=200)
selectvalue = st.selectbox("Select movie from dropdown", movies['title'].values)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)
    recommend_movie, recommend_poster = [], []
    for i in distance[1:6]:  # Top 5 movies
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster

if st.button("Show Recommend"):
    movie_names, movie_posters = recommend(selectvalue)
    cols = st.columns(5)
    for col, name, poster in zip(cols, movie_names, movie_posters):
        with col:
            st.text(name)
            st.image(poster)