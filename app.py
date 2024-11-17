import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import gdown


# Set the page layout to wide
st.set_page_config(layout="wide")

# Sidebar navigation with headers
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Homepage", "Descriptive Analysis", "Predictive Analysis 1", "Predictive Analysis 2"])

# Homepage
if page == "Homepage":
    st.title("Welcome to the IMDb Project")
    st.write("Explore the different analyses we've created for movie recommendations and insights based on extensive IMDb datasets of close to 86.000 movies.")
    st.write("")
    st.write("Navigate to the different analyses using the sidebar.")
    st.write("")
    st.write("We are Kiki, Anouck, Menno, Michiel and Tom of Case 10 Group 1.")

# Descriptive Analysis
elif page == "Descriptive Analysis":
    st.title("Descriptive Analysis")
    st.write("Here, you can explore which variables contribute most to e.g. ratings via PCA analysis.")

    # Download CSV file from Google Drive
    url = "https://drive.google.com/uc?id=https://drive.google.com/file/d/13TfN-gIkjs-QKKtBcJI5AWzGWp8OjySs/view?usp=drive_link"
    output = "IMDb_movies.csv"
    gdown.download(url, output, quiet=False)

    # Read the downloaded CSV
    df = pd.read_csv(output)

    # Display the table with top N rows
    st.write("Interactive Table of all Movies:")

    # Configure AgGrid for interactive table
    grid_options = GridOptionsBuilder.from_dataframe(df)
    grid_options.configure_pagination(enabled=True, paginationAutoPageSize=100)  # Enable pagination
    grid_options.configure_default_column(editable=True, sortable=True, filterable=True)  # Enable sorting and filtering

    # Display the interactive table
    AgGrid(df, gridOptions=grid_options.build())

# Predictive Analysis 1
elif page == "Predictive Analysis 1":
    st.title("Predictive Analysis 1")
    st.write("This section provides movie recommendations using machine learning, based on user input.")
    # Add predictive analysis code here

# Predictive Analysis 2
elif page == "Predictive Analysis 2":
    st.title("Predictive Analysis 2")
    st.write("Use this section to predict the rating of a new movie based on selected variables.")
    # Add Predictive analysis code here
