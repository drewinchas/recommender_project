import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read the CSV file into a DataFrame
df = pd.read_csv('data/updated_imdb_top_1000.csv')

# Split the Genre column by comma and create new rows for each genre
df_expanded = df.assign(Genre=df['Genre'].str.split(',')).explode('Genre')

# Strip leading and trailing white space from each genre value
df_expanded['Genre'] = df_expanded['Genre'].str.strip()

# Add a column for the decade of the year the movie was released
df_expanded['Decade'] = (df_expanded['Released_Year'] // 10) * 10

# Add a column for the runtime in blocks of 30 minutes
df_expanded['Runtime_Block'] = (df_expanded['tmdb_runtime'] // 30) * 30

# Add a column for the difference between tmdb_revenue and tmdb_budget
df_expanded['Revenue_Budget_Diff'] = df_expanded['tmdb_revenue'] - df_expanded['tmdb_budget']

# Combine relevant features into a single string for each movie
df_expanded['Features'] = (
    df_expanded['Genre'] + ' ' +
    df_expanded['Decade'].astype(str) + ' ' +
    df_expanded['Runtime_Block'].astype(str) + ' ' +
    df_expanded['Director'] + ' ' +
    df_expanded['Star1']
)

# Create a TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Fit and transform the Features column
tfidf_matrix = tfidf_vectorizer.fit_transform(df_expanded['Features'])

# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Create another TF-IDF Vectorizer
tfidf_vectorizer2 = TfidfVectorizer(stop_words='english')

# Fit and transform the Features column
tfidf_matrix2 = tfidf_vectorizer2.fit_transform(df)

# Compute the cosine similarity matrix
cosine_sim2 = cosine_similarity(tfidf_matrix2, tfidf_matrix2)

# Function to get movie recommendations based on user query
def get_content_recs(query, cosine_sim=cosine_sim):
    # Transform the query using the TF-IDF Vectorizer
    query_vec = tfidf_vectorizer.transform([query])
    
    # Compute the cosine similarity between the query and all movies
    sim_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    # Get the indices of the top 10 most similar movies
    top_indices = sim_scores.argsort()[-10:][::-1]
    
    # Return the top 10 most similar movies
    return df_expanded.iloc[top_indices]

# Function to get collaborative recommendations based on a single Series_Title
def get_collab_recs(series_title, cosine_sim=cosine_sim2):
    # Find the index of the movie that matches the series_title
    idx = df[df['Series_Title'] == series_title].index[0]
    
    # Get the pairwise similarity scores of all movies with that movie
    similarities = list(enumerate(cosine_sim[idx]))
    print(similarities)
    
    # Sort the movies based on the similarity scores
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    
    # Get the scores of the 10 most similar movies
    similarities = similarities[1:11]
    
    # Get the movie indices
    movie_indices = [i[0] for i in similarities]
    
    # Return the top 10 most similar movies
    return df.iloc[movie_indices]

# Return all genres
def get_genres():
    unique_genres = df_expanded['Genre'].unique().tolist()
    return unique_genres

# Return all decades
def get_decades():
    # Filter out non-numeric values and get unique decades
    unique_decades = df_expanded['Decade'].dropna().unique().tolist()
    # Convert decades to strings
    unique_decades = [str(int(decade)) for decade in unique_decades]
    return unique_decades

# Return top 10 directors
def get_top_directors():
    # Count the number of movies for each director
    director_counts = df_expanded['Director'].value_counts()
    # Get the top ten directors
    top_directors = director_counts.head(10).index.tolist()
    return top_directors

# Return top 10 stars in Star1
def get_top_star1():
    # Count the number of movies for each star in Star1
    star1_counts = df_expanded['Star1'].value_counts()
    # Get the top ten stars
    top_star1 = star1_counts.head(10).index.tolist()
    return top_star1

if __name__ == "__main__":
    # Example usage
    query = 'Action 1980 Steven Spielberg Tom Hanks'
    recommendations = get_content_recs(query)
    print(recommendations[['Series_Title', 'Genre', 'Released_Year', 'IMDB_Rating', 'Director', 'Star1']])
    print(get_genres())
    print(get_decades())   
    print(get_top_directors())
    print(get_top_star1())

    # Example usage of collaborative recommendations
    collab_recommendations = get_collab_recs('The Shawshank Redemption')
    print(collab_recommendations[['Series_Title', 'Genre', 'Released_Year', 'IMDB_Rating', 'Director', 'Star1']])