import streamlit as st
import pandas as pd
import logging
import os

from pandas.io.formats.format import return_docstring
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(level=logging.INFO)

import os
st.write("Current working directory:", os.getcwd())

# Load data
@st.cache_data
def load_data():
    try:
        # Try loading the data
        file_path = os.path.join(os.path.dirname(__file__),'data', 'movies.csv')
        st.write(f"Resolved file path: {file_path}")
        movies = pd.read_csv(file_path)

        file_path_ratings = os.path.join(os.path.dirname(__file__),'data', 'ratings.csv')
        st.write(f"Resolved file path: {file_path_ratings}")
        ratings = pd.read_csv(file_path_ratings)

        data = pd.merge(ratings, movies, on="movieId")
    except FileNotFoundError:
        st.error("File not found. Please make sure 'movies.csv' is in the 'data' folder.")
        data = None
        movies = None
        ratings = None
    return movies, data

movies, data = load_data()

if data is not None:
    st.write("Movies data loaded successfully!")
    st.write(data.head())
else:
    exit(-1)

# Create a user-item matrix and similarity dataframe
user_item_matrix = data.pivot_table(index='userId', columns='title', values='rating').fillna(0)
movie_similarity = cosine_similarity(user_item_matrix.T)
similarity_df = pd.DataFrame(movie_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)

# Recommendation function
def recommend_movies(movie_title, similarity_df, top_n=5):
    similar_movies = similarity_df[movie_title].sort_values(ascending=False)[1:top_n+1]
    return similar_movies.index.tolist()

# Streamlit App
st.title("🎥 Personalized Movie Recommendation System")
st.write("Enter a movie title, and we'll recommend similar movies!")

# Input for movie title
movie_title = st.selectbox("Choose a movie:", options=list(movies['title']))

if st.button("Recommend"):
    try:
        recommendations = recommend_movies(movie_title, similarity_df)
        st.write("Movies similar to **{}**:".format(movie_title))
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
    except KeyError:
        st.error("Movie not found in the dataset.")
