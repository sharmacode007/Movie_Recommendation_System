import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    api_key = "ba4af4ba"  # Replace with your OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_id}&apikey={api_key}"
    #st.write(f"Fetching poster for: {movie_id}")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        st.write(f"Poster found for {movie_id}: {data.get('Poster', 'No Image')}")
        return data.get('Poster', "https://via.placeholder.com/500x750?text=No+Image")
    else:
        st.write(f"Failed to fetch poster for {movie_id}. HTTP Status: {response.status_code}")
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters


movies_dict = pickle.load(open('movies_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox('Punch Your Favourite Movie',
                                   movies['title'].values)
if st.button('Recommended'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])