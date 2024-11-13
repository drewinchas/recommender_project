import streamlit as st
import pandas as pd
from backend import get_content_recs, get_genres, get_decades, get_top_directors, get_top_star1
from collab import get_collab_recs

# Set the title of the app
st.title("Drew's Movie Recommender")

# Initialize session state
if 'screen' not in st.session_state:
    st.session_state.screen = 'query'

# Function to switch to recommendations screen
def show_recommendations():
    st.session_state.screen = 'recommendations'
    st.rerun()

# Function to switch to collaborative recommendations screen
def show_collab_recommendations(movie_title):
    st.session_state.screen = 'collab_recommendations'
    st.session_state.collab_recommendations = get_collab_recs(movie_title).copy()
    st.session_state.collab_recommendations.rename(columns={
            'Released_Year': 'Year',
            'Series_Title': 'Title',
            'IMDB_Rating': 'IMDB Rating',
        }, inplace=True)
    
    # Convert Year to string without decimal points or commas
    st.session_state.collab_recommendations['Year'] = st.session_state.collab_recommendations['Year'].astype(int).astype(str)

    st.rerun()

# Query screen
if st.session_state.screen == 'query':
    # Create a form for user input
    with st.form(key='recommender_form'):
        genre = st.selectbox('Select Genre', options=[''] + get_genres())
        decade = st.selectbox('Select Decade', options=[''] + get_decades())
        director = st.selectbox('Select Director', options=[''] + get_top_directors())
        star = st.selectbox('Select Star', options=[''] + get_top_star1())
        runtime = st.selectbox('Select Runtime Block', options=[''] + get_runtime_blocks())
        
        # Submit button
        submit_button = st.form_submit_button(label='Get Recommendations')

    # Handle form submission
    if submit_button:
        # Create a query string based on user input
        query = ' '.join(filter(None, [genre, decade, runtime, director, star]))
        
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

    with st.container(border=True):
        # Display column headers
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 1, 1, 2, 2])
        with col1:
            st.write("Title")
        with col2:
            st.write("Genre")
        with col3:
            st.write("Year")
        with col4:
            st.write("IMDB Rating")
        with col5:
            st.write("Director")
        with col6:
            st.write("Starring Actor")
    
        # Display recommendations with clickable buttons
        recommendations = st.session_state.recommendations
        if not recommendations.empty:
        
            for index, row in recommendations.iterrows():
                col1, col2, col3, col4, col5, col6 = st.columns([3,2,1,1,2,2])
                with col1:
                    #st.write(row['Title'])
                    if st.button(row['Title'], key=index):
                        show_collab_recommendations(row['Title'])
                with col2:
                    st.write(row['Genre'])
                with col3:
                    st.write(row['Year'])
                with col4:
                    st.write(row['IMDB Rating'])
                with col5:
                    st.write(row['Director'])
                with col6:
                    st.write(row['Star1'])
        else:
            st.write("No recommendations found for the given criteria.")
    
    # Button to go back to query screen
    if st.button('Back to Query'):
        st.session_state.screen = 'query'
    
    # Collaborative recommendations screen
if st.session_state.screen == 'collab_recommendations':
    st.write("Here are movies similar to your selected favorite:")
    
    with st.container(border=True):
        # Display column headers
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 1, 1, 2, 2])
        with col1:
            st.write("Title")
        with col2:
            st.write("Genre")
        with col3:
            st.write("Year")
        with col4:
            st.write("IMDB Rating")
        with col5:
            st.write("Director")
        with col6:
            st.write("Starring Actor")

        # Display collaborative recommendations
        collab_recommendations = st.session_state.collab_recommendations
        if not collab_recommendations.empty:
            for index, row in collab_recommendations.iterrows():
                col1, col2, col3, col4, col5, col6 = st.columns([3,2,1,1,2,2])
                with col1:
                    st.write(row['Title'])
                with col2:
                    st.write(row['Genre'])
                with col3:
                    st.write(row['Year'])
                with col4:
                    st.write(row['IMDB Rating'])
                with col5:
                    st.write(row['Director'])
                with col6:
                    st.write(row['Star1'])
        else:
            st.write("No similar movies found.")
    
    # Button to go back to query screen
    if st.button('Back to Query'):
        st.session_state.screen = 'query'
        st.rerun()