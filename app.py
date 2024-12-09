import streamlit as st
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt

# python -m streamlit run app.py

# Set the page layout to wide
st.set_page_config(layout="wide")

# url leading to google colab backend server
global ngrok_url 
ngrok_url = "https://8cb5-34-125-16-213.ngrok-free.app"

# Sidebar navigation with headers
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Homepage", "Movie database", "Insights", "Movie rating prediction"])

# Caching the API call to avoid redundant requests
@st.cache_data
def fetching_movies(payload):
    """Fetches data from the API and caches it."""
    api_url = f"{ngrok_url}/analyze"
    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        filtered_data = response.json()
        df = pd.DataFrame(filtered_data)
        
        # Ensure avg_vote has 1 decimal place
        if 'avg_vote' in df.columns:
            df['avg_vote'] = df['avg_vote'].round(1)  # Rounds to 1 decimal place
        
        return df
    else:
        st.error("Failed to fetch data. Please try again.")
        return pd.DataFrame()  # Return an empty DataFrame in case of failure

def fetching_columns(payload):
    """Fetches data from the API and caches it."""
    api_url = f"{ngrok_url}/columns"
    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        filtered_data = response.json()
        df = pd.DataFrame(filtered_data)

        # Ensure avg_vote has 1 decimal place
        if 'avg_vote' in df.columns:
            df['avg_vote'] = df['avg_vote'].round(1)  # Rounds to 1 decimal place
        
        return df
    else:
        st.error("Failed to fetch data. Please try again.")
        return pd.DataFrame()  # Return an empty DataFrame in case of failure

def dynamic_plot(x_col, y_col=None, plot_type="scatter"):
    """
    Generates plots dynamically based on user inputs.
    Args:
    - x_col (Series): Column for x-axis.
    - y_col (Series, optional): Column for y-axis.
    - plot_type (str): Type of plot ('scatter', 'hist', 'bar', 'box', etc.).
    """
    plt.figure(figsize=(10, 6))
    if plot_type == "scatter" and y_col is not None and not y_col.empty:
        sns.scatterplot(x=x_col, y=y_col)
        plt.title(f"Scatter Plot: {x_col.name} vs {y_col.name}")
    elif plot_type == "hist":
        sns.histplot(x=x_col, kde=True, bins=20)
        plt.title(f"Histogram of {x_col.name}")
    elif plot_type == "bar" and y_col is None:
        sns.countplot(x=x_col)
        plt.title(f"Bar Plot of {x_col.name}")
    elif plot_type == "box" and y_col is not None and not y_col.empty:
        sns.boxplot(x=x_col, y=y_col)
        plt.title(f"Box Plot: {x_col.name} by {y_col.name}")
    else:
        plt.text(0.5, 0.5, "Invalid input for plot type or columns", ha='center', va='center')
        plt.title("Error")

    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)


# Homepage
if page == "Homepage":
    st.title("Welcome to the IMDb Project")
    st.write("Navigate to the different pages using the sidebar.\n")
    st.write("We are Kiki, Anouck, Menno, Michiel and Tom of Case 10 Group 1.\n")
    st.write("Hier moeten nog top 10 meest recente releases of top 10 best beoordeelde films ooit/deze maand/dit jaar")

# Movie recommendations
elif page == "Movie database":
    st.title("Movie list based on your preferences")

    # Initialize session state for filters and data
    if "filters" not in st.session_state:
        st.session_state.filters = {
            "avg_vote": 6.0,
            "votes": 0,
            "genre": "Any",
            "min_year": 1990,
            "language": "English",
            "actors": ""
        }

    if "table_data" not in st.session_state:
        st.session_state.table_data = pd.DataFrame()

    # Sidebar filters - updated dynamically
    st.session_state.filters["avg_vote"] = st.sidebar.slider(
        "Select minimum average rating:",
        min_value=0.0,
        max_value=10.0,
        step=0.1,
        value=st.session_state.filters.get("avg_vote", 6.0)
    )
    st.session_state.filters["votes"] = st.sidebar.slider(
        "Select minimum number of votes:",
        min_value=0,
        max_value=1000000,
        step=1000,
        value=st.session_state.filters.get("votes", 0)
    )
    st.session_state.filters["genre"] = st.sidebar.selectbox(
        "Select genre (optional):",
        options=['Any'] + ['Action', 'Drama', 'Comedy'],
        index=['Any', 'Action', 'Drama', 'Comedy'].index(st.session_state.filters.get("genre", "Any"))
    )
    st.session_state.filters["year"] = st.sidebar.number_input(
        "Select minimum year of publication:",
        min_value=1800,
        max_value=2024,
        step=1,
        value=st.session_state.filters.get("year", 1990)
    )
    st.session_state.filters["language"] = st.sidebar.selectbox(
        "Select language (optional):",
        options=['Any', 'English', 'French'],
        index=['Any', 'English', 'French'].index(st.session_state.filters.get("language", "English"))
    )
    st.session_state.filters["actors"] = st.sidebar.text_input(
        "Search for actor(s):",
        value=st.session_state.filters.get("actors", ""),
        help="Enter a name to search for actors."
    )

    # Add a search button
    if st.sidebar.button("Search"):
        # Define the payload
        payload = {
            **st.session_state.filters
        }

        # Fetch data using the cached function
        st.session_state.table_data = fetching_movies(payload)

    # Display the table if data is available
    if not st.session_state.table_data.empty:
        df = st.session_state.table_data

        # Order these columns and keep the rest as they are
        important_columns = ['title', 'year', 'genre', 'avg_vote', 'votes', 'language', 'duration', 'actors']
        other_columns = [col for col in df.columns if col not in important_columns]
        df = df[important_columns + other_columns]

        # Display the interactive table
        st.write(f"Showing {len(df)} movies with the selected filters:")
        st.dataframe(df)
    else:
        st.write("No data to display. Please adjust your filters or click 'Search'.")

elif page == "Insights":    
    st.title("Insights")
    # Dynamic plot
    x_col = st.selectbox(
        "Select a variable:",
        options = ['year', 'avg_vote', 'votes'], # For now, only take numerical values. Strings will be implemented in the future.
        index=0
    )
    y_col = st.selectbox(
        "Select a variable (optional):",
        options = ['year', 'avg_vote', 'votes'], # For now, only take numerical values. Strings will be implemented in the future.
        index=0
    )
    selected_plot = st.selectbox(
        "Select a plot:",
        options=['scatter', 'hist', 'bar', 'box'],
        index=0
    )

    # Add a search button
    if st.button("Search"):
        # Define the payload
        payload = {"x-axis": x_col}
        if y_col != "None":
            payload["y-axis"] = y_col

        # Fetch data from the backend
        column_data = fetching_columns(payload)

        # Display the plot if data is available
        try:
            # Convert JSON data to a DataFrame
            data = pd.DataFrame(column_data)

            x_data = data[x_col]
            y_data = data[y_col]

            # Make the plot here
            dynamic_plot(x_data, y_data, selected_plot)
        except Exception as e:
            st.write(e)

# Movie rating prediction
elif page == "Movie rating prediction":
    st.title("Movie rating prediction")
    # Add analysis code here
