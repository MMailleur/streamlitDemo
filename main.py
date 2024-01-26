import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from utils import load_data, calculate_player_attributes, calculate_mean_attributes, generate_player_stats_comparison, generate_player_stats_comparison_graph, generate_player_attributes_comparison_graph

# Load data
df = load_data("datasetMerged.csv")

# Set Streamlit page configuration
st.set_page_config(
    page_title="Player Market Price",
    page_icon=":soccer:",  # Change to your preferred icon
    layout="wide"
)

# Sidebar with tabs
selected_tab = st.sidebar.radio("Football Market analysis", ["Market Stats :chart:", "Player :athletic_shoe:"])

# Dropdown to select a country
selected_country = st.sidebar.selectbox("Select a Country", df["PAYS"].dropna().unique())

# Filter player names based on the selected country
filtered_players = df[df["PAYS"] == selected_country]["name"].unique()

# Dropdown to select a player from the filtered list
selected_player = st.sidebar.selectbox("Select a Player", filtered_players)

# Filter the DataFrame based on the selected player
df_row = df[df["name"] == selected_player]

# Main content based on selected tab
if selected_tab == "Market Stats :chart:":
    # Create the scatter plot with player names as tooltips
    fig = px.scatter(df, x='Age', y='Value', hover_data=['name'],
                     title='Age vs Market Value with Player Names')

    # Display the plot in Streamlit app
    st.plotly_chart(fig)

if selected_tab == 'Player :athletic_shoe:':
    st.markdown(
        """
        <div style="background-color: black; color: white; padding: 1rem; text-align: center; font-size: 2rem; font-weight: bold; margin-bottom: 2rem; width: 100%; box-sizing: border-box;">
            Player Individual Stats
        </div>
        """,
        unsafe_allow_html=True
    )

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