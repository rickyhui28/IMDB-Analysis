from flask import Flask, request, render_template
import requests
import pandas as pd
#from recommendation import recommend_similar_movies

app = Flask(__name__)

# TMDB API key (replace with your actual API key)
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYmNhNDI3Zjc1Y2NiZTVkZmYxYzc1ZjgzZDA4ZTc0OSIsIm5iZiI6MTcyNzc5NzIyMi42NDYxOTcsInN1YiI6IjY2ZmMxNWRiMDYxYWZlMTE0YmYxODdmYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.PgAc25GiB7LERYWWeSNxRSsiimNwKTYl4lgJ980dUAs"
TMDB_BASE_URL = "https://api.themoviedb.org/3"


def get_movie_data_from_tmdb(movie_name):
    """
    Fetch movie data from TMDB API using the movie name.
    """
    search_url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': movie_name
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]  # return the first result
    return None
@app.route("/", methods=["GET", "POST"])
def index():
    movie_data = None
    recommendations = None

    if request.method == "POST":
        movie_name = request.form.get("movie_name")
        
        # Step 1: Fetch movie information from TMDB
        movie_data = get_movie_data_from_tmdb(movie_name)
        
        # Step 2: Get similar movie recommendations from Kaggle dataset
        if movie_data:
            movie_title = movie_data.get("title", "")
            recommendations = recommend_similar_movies(movie_title)

    return render_template("index.html", movie_data=movie_data, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
    