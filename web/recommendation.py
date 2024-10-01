import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load Kaggle dataset
df = pd.read_csv('../data/combined_df.csv')

# Preprocessing: Combine important features into a single string
df['combined_features'] = df['genres'] + df["title"]
# " " + df['keywords'] + " " + df['overview']

# TF-IDF Vectorizer to convert text into vectors
tfidf = TfidfVectorizer(stop_words='english')

# Fit the vectorizer to the combined features
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# Calculate cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Helper function to get index of a movie title
def get_index_from_title(title):
    try:
        return df[df.title == title].index[0]
    except:
        return None

def recommend_similar_movies(movie_title, num_recommendations=10):
    """
    Recommend top 'n' similar movies using cosine similarity based on movie title.
    """
    idx = get_index_from_title(movie_title)
    if idx is None:
        return []

    # Get similarity scores for the movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort movies based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top similar movies
    sim_indices = [i[0] for i in sim_scores[1:num_recommendations+1]]
    
    # Return the movie titles for the top similar movies
    return df.iloc[sim_indices][['title', 'genres']].to_dict(orient='records')
