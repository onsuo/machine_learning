import pickle

import key
import streamlit as st
from tmdbv3api import (
    Movie,
    TMDb,
)


# This code defines a function called "get_recommendations" which takes a movie title as an input.
# The function then finds the index of the corresponding movie in a pandas dataframe called "movies".
# It then calculates the cosine similarity scores between the selected movie and all other movies in the dataframe using a pre-calculated cosine similarity matrix called "cosine_sim".
# The function then sorts the similarity scores in descending order and selects the top 10 movies with the highest similarity scores (excluding the selected movie itself).
# For each of these top 10 movies, the function retrieves details (including the movie title and poster image URL) using the "movie.details" function from a Python package called "tmdbsimple".
# Finally, the function returns a tuple containing lists of movie poster image URLs and titles for the top 10 recommended movies.
def get_recommendations(_title):
    _idx = movies[movies["title"] == _title].index[0]
    _sim_scores = list(enumerate(cosine_sim[_idx]))
    _sim_scores = sorted(_sim_scores, key=lambda x: x[1], reverse=True)
    _sim_scores = _sim_scores[1:11]
    _movie_indices = [i[0] for i in _sim_scores]

    _images = []
    _titles = []
    for i in _movie_indices:
        _movie_id = movies["id"].iloc[i]
        _details = movie.details(_movie_id)

        _image_path = _details["poster_path"]
        if _image_path:
            _image_path = "https://image.tmdb.org/t/p/w500" + _image_path
        else:
            _image_path = "project/no_image.jpg"

        _images.append(_image_path)
        _titles.append(_details["title"])

    return _images, _titles


movie = Movie()
tmdb = TMDb()
tmdb.api_key = key.API_KEY
tmdb.language = "ko-KR"

movies = pickle.load(open("project/movies.pickle", "rb"))
cosine_sim = pickle.load(open("project/cosine_sim.pickle", "rb"))

st.set_page_config(layout="wide")
st.header("OUUNFLIX")

movie_list = movies["title"].values
title = st.selectbox("Choose a movie you like", movie_list)
if st.button("Recommend"):
    with st.spinner("Please wait..."):
        images, titles = get_recommendations(title)

        idx = 0
        for i in range(0, 2):
            cols = st.columns(5)
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1
