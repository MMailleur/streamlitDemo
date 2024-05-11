import hmac
import streamlit as st
import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from sqlalchemy import create_engine
from utils import load_data, calculate_player_attributes, calculate_mean_attributes,format_market_value\
, generate_player_stats_comparison, generate_player_stats_comparison_graph, generate_player_attributes_comparison_graph
import joblib
from sklearn.ensemble import RandomForestRegressor
import math
def load_data_from_base(table,engine):
    return pd.read_sql(f"SELECT * FROM {table}", engine)
engine = create_engine(
    "mysql+mysqlconnector://{user}:{pw}@{host}:{port}/{db}".format(
        user=st.secrets["user"],
        pw=st.secrets["password"],
        host=st.secrets["host"],
        port=st.secrets["port"],
        db=st.secrets["database"],
    )
)
df_player_web_stats = load_data_from_base("player_web_stats",engine)
df_ref_joueurs = load_data_from_base("ref_joueurs",engine)
df = df_player_web_stats.merge(df_ref_joueurs, left_on='name', right_on='Surnom')
best_model = joblib.load('best_model.pkl')
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.


# Load data
st.set_page_config(
    page_title="Player Market Price",
    page_icon=":soccer:",  # Change to your preferred icon
    layout="wide"
)

# Set Streamlit page configuration


#Sidebar with tabs
selected_tab = st.sidebar.radio("Football Market analysis", ["Market Stats :chart:", "Player :athletic_shoe:","Player Market Value IA prediction 🤯"])



# Main content based on selected tab
if selected_tab == "Market Stats :chart:":
    cola,colb = st.columns(2)
    # Create the scatter plot with player names as tooltips
    with cola :
        fig = px.scatter(df, x='Age', y='Value', hover_data=['name'],
                        title='Age vs Market Value with Player Names')
        st.plotly_chart(fig)
    with colb :
        foot_counts = df['foot'].value_counts()
        fig_pie = px.pie(names=foot_counts.index, values=foot_counts.values, title='Distribution of Strong foots')
        st.plotly_chart(fig_pie)

    df_show = df[df.columns[df.columns != "Unnamed: 0"]]
    st.subheader("Dataset Fifa value and player stats")
    st.dataframe(df_show)
if selected_tab == 'Player :athletic_shoe:':
    st.markdown(
        """
        <div style="background-color: black; color: white; padding: 1rem; text-align: center; font-size: 2rem; font-weight: bold; margin-bottom: 2rem; width: 100%; box-sizing: border-box;">
            Player Individual Stats
        </div>
        """,
        unsafe_allow_html=True
    )
    # Dropdown to select a country
    selected_country = st.sidebar.selectbox("Select a Country", df["PAYS"].dropna().unique())

    # Filter player names based on the selected country
    filtered_players = df[df["PAYS"] == selected_country]["name"].unique()

    # Dropdown to select a player from the filtered list
    selected_player = st.sidebar.selectbox("Select a Player", filtered_players)

    # Filter the DataFrame based on the selected player
    df_row = df[df["name"] == selected_player]

    player_attributes = calculate_player_attributes(df_row)

    # Calculate mean values for all players
    mean_attributes = calculate_mean_attributes(df)

    # Radar Chart for Player Attributes

    # Create three columns
    col1, col2, col3 = st.columns((0.3, 0.3, 0.25), gap="small")

    # Display image in the first column
    with col1:
        st.subheader(str(df_row["name"].iloc[0]))
        url = df_row["IMG_WyScout"].iloc[0]
        if isinstance(url, str):
            st.image(url)  # Manually adjust the width of the image as per requirement
        else:
            st.image("https://cdn5.wyscout.com/photos/players/public/ndplayer_100x130.png", use_column_width=True)

    # Add content to other columns if needed
    with col2:
        st.info(f"Age: {df_row['Age'].iloc[0]} years")
        st.info(f"Height: {df_row['Height'].iloc[0]} cm")
        st.info(f"Footedness: {df_row['foot'].iloc[0]}")

    # Display the Plotly chart in Streamlit app
    with col3:
        fig_attributes = generate_player_attributes_comparison_graph(player_attributes, mean_attributes)

        st.plotly_chart(fig_attributes)

    # Two-column layout
    col1, colmidle, col2 = st.columns((0.6, 0.4, 0.2))

    # Player stats comparison chart
    with col1:
        # Sample data for demonstration (replace with your actual data)
        top_5_stats_player, mean_df = generate_player_stats_comparison(df_row, df)

        # Generate graph using the function from utils.py
        fig_stats_comparison = generate_player_stats_comparison_graph(top_5_stats_player, mean_df)

        st.plotly_chart(fig_stats_comparison)

    # Empty space in the second column for visual separation
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        total_stats = str(df_row["Total stats"].iloc[0])
        st.metric("Total Stats", total_stats)

        player_value = df_row["Value"].iloc[0]
        player_value_in_millions = player_value / 1e6
        # Display player value in millions with formatting
        player_value_formatted = f"${player_value_in_millions:.2f}M"
        st.metric("Player Value", player_value_formatted)

        reputation = str(df_row["Best position"].iloc[0])
        st.metric("Best position", reputation)
if selected_tab == 'Player Market Value IA prediction 🤯':
    st.title('🔮 Market Value Predictor')

    st.markdown("""
                Welcome to the Market Value Predictor! Here, you can upload your player data as a CSV file and
                get the predicted market value. The result is stored and can be viewed in the table below.
                Let's get started! 👇
                """)

    # Upload a CSV file
    uploaded_file = st.file_uploader("Please upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the uploaded CSV file into a pandas DataFrame
        player_sample_df = pd.read_csv(uploaded_file, sep=";")
        predictions = best_model.predict(player_sample_df)
        actual_value = math.exp(predictions)

        # Format the actual value with appropriate units
        if actual_value < 1000:
            formatted_value = f"{actual_value:.2f}"
        elif actual_value < 1_000_000:
            formatted_value = f"{actual_value / 1000:.2f}K"
        else:
            formatted_value = f"{actual_value / 1_000_000:.2f}M"
        player_sample_df['log_predict'] = predictions
        player_sample_df['predicted_value_euros'] = formatted_value
        player_sample_df.to_sql('prediction', con=engine, if_exists='append', index=False)
        # Display the formatted predicted market value
        st.markdown(f'<div style="color: green; font-size: 30px;">Predicted market value for the uploaded player data is: {formatted_value} €</div>', unsafe_allow_html=True)
    # Fetch data from base and display it in a table
    st.subheader("Predicted values stored in the database")
    st.dataframe(load_data_from_base("prediction",engine))
