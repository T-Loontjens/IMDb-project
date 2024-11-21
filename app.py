import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import gdown
import random

# Set the page layout to wide
st.set_page_config(layout="wide")

# Sidebar navigation with headers
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Homepage", "Movie recommendations", "Movie rating prediction", "Other projects"])

# Cache the CSV download and loading process so it only loads once and not every time a single filter is changed
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?export=download&id=107JsqPNA8Brr2vYrcQZyXQZwv25FFDNM"
    output = "movie_data.csv"
    gdown.download(url, output, quiet=False)

    # Load the data into a Pandas DataFrame
    df = pd.read_csv(
        output,
        quotechar='"',       # Use double quotes for quoted fields
        escapechar='\\',     # Escape special characters
        delimiter=",",       # Delimiter for columns
        lineterminator="\n", # Line terminator
        on_bad_lines="skip"  # Skip problematic lines
    )
    return df

# Initialize session state for filtered data
if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = pd.DataFrame()

# Homepage
if page == "Homepage":
    st.title("Welcome to the IMDb Project")
    st.write("Navigate to the different pages using the sidebar.\n")
    st.write("We are Kiki, Anouck, Menno, Michiel and Tom of Case 10 Group 1.\n")
    st.write("Hier moeten nog top 10 meest recente releases of top 10 best beoordeelde films ooit/deze maand/dit jaar")

# Movie recommendations
elif page == "Movie recommendations":
    st.title("Top 100 Movie recommendations based on your preferences")

    # Load the dataset
    df = load_data()

    # Sidebar filters
    st.sidebar.write("")
    rating = st.sidebar.slider("Select minimum average rating:", min_value=0.0, max_value=10.0, step=0.1, value=7.5)
    votes = st.sidebar.slider("Select minimum number of votes:", min_value=0, max_value=int(df['votes'].max()), step=1000, value=1000)

    # Unique genres and languages
    genres = df['genre'].dropna().str.split(',').explode().unique()
    languages_split = df['language'].dropna().str.split(',').explode().str.strip().unique()

    genre = st.sidebar.selectbox("Select genre (optional):", options=['Any'] + sorted(genres))
    min_year = st.sidebar.number_input("Select minimum year of publication:", min_value=1800, max_value=2024, step=1, value=1995)
    language = st.sidebar.selectbox("Select language (optional):", options=['Any'] + sorted(languages_split))
    actor_search = st.sidebar.text_input("Search for actor(s):", value="", help="Enter a name to search for actors.")

    # Add a search button
    if st.sidebar.button("Search"):
        # Filter data when "Search" is clicked
        filtered_df = df[df['avg_vote'] >= rating]
        filtered_df = filtered_df[filtered_df['votes'] >= votes]

        if genre != 'Any':
            filtered_df = filtered_df[filtered_df['genre'].str.contains(genre, na=False)]

        filtered_df = filtered_df[filtered_df['year'].astype(int) >= min_year]

        if language != 'Any':
            filtered_df = filtered_df[filtered_df['language'].str.contains(language, na=False, case=False)]

        if actor_search:
            filtered_df = filtered_df[filtered_df['actors'].str.contains(actor_search, case=False, na=False)]

        # Select 100 random rows from the filtered DataFrame
        if len(filtered_df) > 100:
            sampled_df = filtered_df.sample(n=100, random_state=random.randint(1, 1000))
        else:
            sampled_df = filtered_df

        # Save the filtered data to session state
        st.session_state.filtered_df = sampled_df

    # Display filtered data only if it's available
    if not st.session_state.filtered_df.empty:
        # Sort the sampled DataFrame by 'title' in ascending order
        sampled_df = st.session_state.filtered_df.sort_values(by='title')

        # Prioritize the first four columns and keep the rest as they are
        important_columns = ['title', 'year', 'genre', 'avg_vote', 'votes', 'language', 'duration', 'actors']
        other_columns = [col for col in sampled_df.columns if col not in important_columns]
        sampled_df = sampled_df[important_columns + other_columns]

        # Configure AgGrid for interactive table
        grid_options = GridOptionsBuilder.from_dataframe(sampled_df)
        grid_options.configure_pagination(enabled=True, paginationAutoPageSize=100)  # Enable pagination
        grid_options.configure_default_column(editable=True, sortable=True, filterable=True)  # Enable sorting and filtering

        # Display the interactive table
        st.write(f"Showing {len(sampled_df)} movies with the selected filters:")
        AgGrid(sampled_df, gridOptions=grid_options.build())

# Movie rating prediction
elif page == "Movie rating prediction":
    st.title("Movie rating prediction")
    # Add predictive analysis code here

# Other projects
elif page == "Other projects":
    st.title("Other projects")
    # Add Predictive analysis code here

# To run the script, put this in the terminal -> python -m streamlit run app.py

'''
Future objectives:
- "Insights" tab
'''
