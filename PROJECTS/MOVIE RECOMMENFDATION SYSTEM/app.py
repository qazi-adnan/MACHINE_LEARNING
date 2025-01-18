import streamlit as st
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page Configuration
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎥",
    layout="centered"
)

# Load the dataset from your computer
@st.cache_data
def load_data():
    # Update the path to where your `movies.csv` file is stored
    return pd.read_csv(r"D:\STUDY\MACHINE_LEARNING\PROJECTS\MOVIE RECOMMENFDATION SYSTEM\movies.csv")

# Title of the app
st.title("🎬 Movie Recommendation System")
st.markdown("Discover movies similar to your favorites! Just enter a movie name and get personalized recommendations.")

# Load dataset
movies_data = load_data()



# Selecting the relevant features for recommendation
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']

# Replace null values with empty strings
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

# Combine all selected features into a single string
combined_features = (
    movies_data['genres']
    + ' ' + movies_data['keywords']
    + ' ' + movies_data['tagline']
    + ' ' + movies_data['cast']
    + ' ' + movies_data['director']
)

# Convert the text data to feature vectors
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

# Calculate the similarity scores
similarity = cosine_similarity(feature_vectors)

# Input movie name
st.subheader("Enter Your Favorite Movie 🎞️")
movie_name = st.text_input("Type a movie name:", placeholder="E.g., Avatar")

if st.button("Get Recommendations"):
    if movie_name.strip():
        # Get a list of all movie titles
        list_of_all_titles = movies_data['title'].tolist()

        # Find the closest match to the user's input
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles, n=1)

        if find_close_match:
            close_match = find_close_match[0]

            # Get the index of the matched movie
            index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]

            # Get similarity scores for all movies
            similarity_score = list(enumerate(similarity[index_of_the_movie]))

            # Sort movies based on similarity scores
            sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

            # Display the top 10 recommended movies
            st.subheader(f"Movies similar to '{close_match}':")
            recommendations = []
            for movie in sorted_similar_movies[1:11]:
                index = movie[0]
                title_from_index = movies_data[movies_data.index == index]['title'].values[0]
                recommendations.append(title_from_index)

            # Show recommendations
            for i, recommendation in enumerate(recommendations, 1):
                st.write(f"{i}. {recommendation}")
        else:
            st.error("No similar movies found. Please try a different movie name.")
    else:
        st.error("Please enter a movie name.")
