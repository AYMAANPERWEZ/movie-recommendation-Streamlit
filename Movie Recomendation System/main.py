import streamlit as st
import pickle
import pandas as pd
import requests
import os


def fetch_poster(movie_id):
    API_KEY = 'd0235aef1abf36790f502191179db04e'  
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('poster_path'):
                return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
    return None



def recommended(movie):
    movie_index = movies[movies['title'] == movie].index
    if len(movie_index) == 0:
        return []  
    movie_index = movie_index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movie_list:
        recommended_movies.append({
            'title': movies.iloc[i[0]]['title'],
            'poster': fetch_poster(movies.iloc[i[0]]['movie_id'])
        })
    return recommended_movies


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'movies_dict.pkl'), 'rb') as f:
    movies_dict = pickle.load(f)

with open(os.path.join(BASE_DIR, 'similarity.pkl'), 'rb') as f:
    similarity = pickle.load(f)

movies = pd.DataFrame(movies_dict)


st.set_page_config(layout='wide', page_title='Movie Recommendation System', page_icon='🎬', 
                   initial_sidebar_state='collapsed')

st.title('🎥 Movie Recommendation System')
selected_movie_name = st.selectbox('Select a movie:', movies['title'])
recommend_button = st.button('Recommend')


if recommend_button:
    recommendations = recommended(selected_movie_name)
    if recommendations:
        st.subheader("Recommended Movies")
        cols = st.columns(5)
        for i, movie in enumerate(recommendations):
            with cols[i % 5]:
                st.text(movie['title'])
                if movie['poster']:
                    st.image(movie['poster'], use_container_width=True)

                else:
                    st.write("No poster available")
    else:
        st.error("No recommendations found.")
