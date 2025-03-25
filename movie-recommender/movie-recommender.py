import streamlit as st
import pandas as pd
import logging
import os

from pandas.io.formats.format import return_docstring
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(level=logging.INFO)

# Apply custom CSS to change the font
st.markdown("""
<style>
    body {
        font-family: Arial, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        # Try loading the data
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'movies.csv')
        movies = pd.read_csv(file_path)

        file_path_ratings = os.path.join(os.path.dirname(__file__), 'data', 'ratings.csv')
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
def recommend_movies(movie_title, similarity_df, movies_df, top_n=5):
    try:
        st.write(f"Finding recommendations for: {movie_title}")

        # Ensure that the movie exists in the dataset
        if movie_title not in movies_df['title'].values:
            st.error(f"Movie '{movie_title}' not found in the dataset.")
            return []

        # Get the index of the movie in the similarity matrix
        movie_index = similarity_df.columns.get_loc(movie_title)
        st.write(f"Movie found at index: {movie_index}")

        # Get the similarity scores for the selected movie
        similarity_scores = similarity_df.iloc[movie_index]

        # Sort the movies based on similarity scores
        similar_movies = similarity_scores.sort_values(ascending=False)

        st.write(f"Found {len(similar_movies)} similar movies.")

        # Return top N recommendations
        top_similar_movies = similar_movies.index[1:top_n + 1]  # Exclude the movie itself (first entry)
        return top_similar_movies

    except Exception as e:
        st.error(f"Error during movie recommendation: {e}")
        return []

# Streamlit App
st.title("🎥 Personalized Movie Recommendation System")
st.write("Enter a movie title, and we'll recommend similar movies!")

# Input for movie title
movie_title = st.selectbox("Choose a movie:", options=list(movies['title']))

if st.button("Recommend"):
    try:
        recommendations = recommend_movies(movie_title, similarity_df, movies)
        st.write(f"Movies similar to **{movie_title}**:")
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
    except KeyError:
        st.error("Movie not found in the dataset.")
