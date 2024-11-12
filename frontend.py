import streamlit as st
import pandas as pd
from backend import get_content_recs, get_genres, get_decades, get_top_directors, get_top_star1

# Set the title of the app
st.title("Drew's Movie Recommender")

# Initialize session state
if 'screen' not in st.session_state:
    st.session_state.screen = 'query'

# Function to switch to recommendations screen
def show_recommendations():
    st.session_state.screen = 'recommendations'
    st.rerun()

# Query screen
if st.session_state.screen == 'query':
    # Create a form for user input
    with st.form(key='recommender_form'):
        genre = st.selectbox('Select Genre', options=[''] + get_genres())
        decade = st.selectbox('Select Decade', options=[''] + get_decades())
        director = st.selectbox('Select Director', options=[''] + get_top_directors())
        star = st.selectbox('Select Star', options=[''] + get_top_star1())
        
        # Submit button
        submit_button = st.form_submit_button(label='Get Recommendations')

    # Handle form submission
    if submit_button:
        # Create a query string based on user input
        query = ' '.join(filter(None, [genre, decade, director, star]))
        
        # Get recommendations
        recommendations = get_content_recs(query)
        
        # Sort recommendations by IMDB rating
        recommendations = recommendations.sort_values(by='IMDB_Rating', ascending=False)
        
        # Rename columns
        recommendations = recommendations.rename(columns={
            'Released_Year': 'Year',
            'Series_Title': 'Title',
            'IMDB_Rating': 'IMDB Rating',
        })

       # Convert Year to string without decimal points or commas
        recommendations['Year'] = recommendations['Year'].astype(int).astype(str)
        
        # Store recommendations in session state
        st.session_state.recommendations = recommendations
        
        # Switch to recommendations screen
        show_recommendations()

# Recommendations screen
if st.session_state.screen == 'recommendations':
    st.write("Pick your favorite movie from this list, for a more personalized recommendation.")
    
    # Display recommendations
    recommendations = st.session_state.recommendations
    if not recommendations.empty:
        st.dataframe(recommendations[['Title', 'Genre', 'Year', 'IMDB Rating', 'Director', 'Star1']])
    else:
        st.write("No recommendations found for the given criteria.")
    
    # Button to go back to query screen
    if st.button('Back to Query'):
        st.session_state.screen = 'query'