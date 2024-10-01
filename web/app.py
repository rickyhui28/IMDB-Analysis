from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Replace with your actual TMDB API Bearer token
TMDB_API_KEY = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYmNhNDI3Zjc1Y2NiZTVkZmYxYzc1ZjgzZDA4ZTc0OSIsIm5iZiI6MTcyNzc5NzM0Ny42NDc5LCJzdWIiOiI2NmZjMTVkYjA2MWFmZTExNGJmMTg3ZmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.0EtuhkjIK9bLV4dpX_8bxyM19jTqR1sCqNi18XLwrmE"

# Predefined genre mapping
GENRE_MAPPING = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

def search_movie_on_tmdb(movie_name):
    """
    Query the TMDB API for a movie by its name and get detailed information.
    """
    url = f"https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1&query={movie_name}"
    headers = {
        "accept": "application/json",
        "Authorization": TMDB_API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_movie_details(movie_id):
    """
    Fetch additional details for a specific movie, such as runtime, production countries, and genres.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": TMDB_API_KEY
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        movie_name = request.form.get("movie_name")
        
        # Search for the movie using the TMDB API
        tmdb_response = search_movie_on_tmdb(movie_name)
        
        # Check if the TMDB API returned any results
        if tmdb_response and "results" in tmdb_response:
            movie_info_list = []
            for movie in tmdb_response["results"]:
                # Get more details for each movie
                movie_details = get_movie_details(movie["id"])
                
                if movie_details:
                    movie_info_list.append({
                        "title": movie["title"],  # Movie title
                        "description": movie["overview"],
                        "release_year": movie["release_date"].split("-")[0],  # Extract year
                        "runtime": movie_details.get("runtime", "N/A"),  # Runtime from detailed call
                        "genres": [GENRE_MAPPING.get(genre_id, "Unknown") for genre_id in movie["genre_ids"]],
                        "production_countries": [country['name'] for country in movie_details.get("production_countries", [])],
                        "seasons": movie_details.get("seasons", "N/A"),  # Relevant for TV Shows, ignore for movies
                        "tmdb_popularity": movie["popularity"],
                        "tmdb_score": movie["vote_average"],
                        "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie["poster_path"] else None,  # Movie thumbnail
                        "platform": "N/A"  # Assuming 'platform' is inferred or provided from another service
                    })

            return render_template("index.html", movie_name=movie_name, movie_info=movie_info_list)
        else:
            return f"No results found for '{movie_name}'"
    
    return render_template("index.html", movie_name=None, movie_info=None)

if __name__ == "__main__":
    app.run(debug=True)
