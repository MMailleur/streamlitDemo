import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from utils import load_data, calculate_player_attributes, calculate_mean_attributes,format_market_value\
, generate_player_stats_comparison, generate_player_stats_comparison_graph, generate_player_attributes_comparison_graph
import joblib
from sklearn.ensemble import RandomForestRegressor
# Load data
st.set_page_config(
    page_title="Player Market Price",
    page_icon=":soccer:",  # Change to your preferred icon
    layout="wide"
)
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)
df = load_data("datasetMerged.csv")
best_model = joblib.load('best_model.pkl')
# Set Streamlit page configuration


# Sidebar with tabs
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
    st.title('Market Value Predictor')

    ball_control, dribbling_reflexes = st.columns(2)
    total_power, shooting_handling = st.columns(2)
    age, total_mentality = st.columns(2)
    finishing, passing_kicking = st.columns(2)
    shot_power, international_reputation = st.columns(2)

    with ball_control:
        ball_control = st.slider('Ball Control', min_value=0, max_value=100, value=50)
    with dribbling_reflexes:
        dribbling_reflexes = st.slider('Dribbling / Reflexes', min_value=0, max_value=100, value=50)

    with total_power:
        total_power = st.slider('Total Power', min_value=0, max_value=500, value=250)
    with shooting_handling:
        shooting_handling = st.slider('Shooting / Handling', min_value=0, max_value=100, value=50)

    with age:
        age = st.slider('Age', min_value=15, max_value=40, value=25)
    with total_mentality:
        total_mentality = st.slider('Total Mentality', min_value=0, max_value=500, value=250)

    with finishing:
        finishing = st.slider('Finishing', min_value=0, max_value=100, value=50)
    with passing_kicking:
        passing_kicking = st.slider('Passing / Kicking', min_value=0, max_value=100, value=50)

    with shot_power:
        shot_power = st.slider('Shot Power', min_value=0, max_value=100, value=50)
    with international_reputation:
        international_reputation = st.slider('International Reputation', min_value=1, max_value=5, value=3)

    input_features = {
        'Ball control': ball_control,
        'Dribbling / Reflexes': dribbling_reflexes,
        'Total power': total_power,
        'Shooting / Handling': shooting_handling,
        'Age': age,
        'Total mentality': total_mentality,
        'Finishing': finishing,
        'Passing / Kicking': passing_kicking,
        'Shot power': shot_power,
        'International reputation': international_reputation
    }
 
    input_data = pd.DataFrame([input_features])

    # Make predictions
    input_array = input_data.values
    predictions = best_model.predict(input_array)
    predicted_value = np.exp(predictions[0])
    formatted_value = format_market_value(predicted_value)

    # Display the formatted predicted market value
    st.write(f"Predicted market value is {formatted_value}")
