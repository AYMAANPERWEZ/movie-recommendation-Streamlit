import streamlit as st
import pickle
import pandas as pd
import requests
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movies_path = os.path.join(BASE_DIR, 'movies_dict.pkl')
similarity_path = os.path.join(BASE_DIR, 'similarity.pkl')

with open(movies_path, 'rb') as f:
    movies = pickle.load(f)

with open(similarity_path, 'rb') as f:
    similarity = pickle.load(f)


# Function to fetch movie poster from TMDb API
def fetch_poster(movie_id):
    #Give your OpenAi key
    API_KEY = ' '
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('poster_path'):
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    return None

# Function to recommend movies
def recommended(movie):
    movie_index = movies[movies['title'] == movie].index
    if len(movie_index) == 0:
        return []  # Return empty list if movie not found
    movie_index = movie_index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    
    for i in movie_list:
        recommended_movies.append({
            'title': movies.iloc[i[0]]['title'],
            'poster': fetch_poster(movies.iloc[i[0]]['movie_id'])  # Fetch poster for each recommended movie
        })
    return recommended_movies

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set page width and background color
st.set_page_config(layout='wide', page_title='Movie Recommendation System', page_icon='🎬', 
                   initial_sidebar_state='collapsed')

# Title and sidebar
st.title('🎥 Movie Recommendation System')
selected_movie_name = st.selectbox('Select a movie:', movies['title'])
recommend_button = st.button('Recommend')

# Main content
if recommend_button:
    recommendations = recommended(selected_movie_name)
    if recommendations:
        st.subheader("Recommended Movies")
        # Display posters in a grid layout
        col1, col2, col3 = st.columns(3)
        for movie in recommendations:
            with col1, st.expander(movie['title']):
                if movie['poster']:
                    st.image(movie['poster'], caption='', use_column_width=True)
                else:
                    st.write("No poster available")
    else:
        st.error("No recommendations found.")
