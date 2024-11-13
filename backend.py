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
df['Decade'] = (df['Released_Year'] // 10) * 10

# Add a column for the runtime in blocks of 30 minutes
df['Runtime_Block'] = (df['tmdb_runtime'] // 30) * 30

# Add a column for the difference between tmdb_revenue and tmdb_budget
df['Revenue_Budget_Diff'] = df['tmdb_revenue'] - df['tmdb_budget']

# Combine relevant features into a single string for each movie
df['Features'] = (
    df['Genre'] + ' ' +
    df['Decade'].astype(str) + ' ' +
    df['Runtime_Block'].astype(str) + ' ' +
    df['Director'] + ' ' +
    df['Star1']
)

# Create a TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Fit and transform the Features column
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Features'])

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
    return df.iloc[top_indices]

# Return all genres
def get_genres():
    unique_genres = df_expanded['Genre'].unique().tolist()
    return unique_genres

# Return all decades
def get_decades():
    # Filter out non-numeric values and get unique decades
    unique_decades = df['Decade'].dropna().unique().tolist()
    # Convert decades to strings
    unique_decades = [str(int(decade)) for decade in unique_decades]
    return unique_decades

# Return top 10 directors
def get_top_directors():
    # Count the number of movies for each director
    director_counts = df['Director'].value_counts()
    # Get the top ten directors
    top_directors = director_counts.head(10).index.tolist()
    return top_directors

# Return top 10 stars in Star1
def get_top_star1():
    # Count the number of movies for each star in Star1
    star1_counts = df['Star1'].value_counts()
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
    #collab_recommendations = get_collab_recs('The Shawshank Redemption')
    #print(collab_recommendations[['Series_Title', 'Genre', 'Released_Year', 'IMDB_Rating', 'Director', 'Star1']])