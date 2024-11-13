import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read the CSV file into a DataFrame
df = pd.read_csv('data/updated_imdb_top_1000.csv')

# Function to train a collaborative filtering model and return similar movies
def get_collab_recs(series_title):
    # Combine relevant features into a single string for each movie
    df['Features'] = (
        df['Series_Title'].fillna('') + ' ' +
        df['Released_Year'].fillna('').astype(str) + ' ' +
        df['Certificate'].fillna('') + ' ' +
        df['Runtime'].fillna('').astype(str) + ' ' +
        df['Genre'].fillna('') + ' ' +
        df['IMDB_Rating'].fillna('').astype(str) + ' ' +
        df['Overview'].fillna('') + ' ' +
        df['Meta_score'].fillna('').astype(str) + ' ' +
        df['Director'].fillna('') + ' ' +
        df['Star1'].fillna('') + ' ' +
        df['tmdb_original_language'].fillna('') + ' ' +
        df['tmdb_popularity'].fillna('').astype(str) + ' ' +
        df['tmdb_genres'].fillna('')
    )

    # Create a TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform the Features column
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['Features'])

    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Find the index of the movie that matches the series_title
    idx = df[df['Series_Title'] == series_title].index[0]

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]  # Exclude the movie itself

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df.iloc[movie_indices]

# Example usage
if __name__ == "__main__":
    movie_title = 'Cast Away'
    recommendations = get_collab_recs(movie_title)
    print(recommendations[['Series_Title', 'Genre', 'Released_Year', 'IMDB_Rating', 'Director', 'Star1']])