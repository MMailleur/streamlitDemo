import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
# Assuming df_raw is your DataFrame
# Replace 'Age', 'Value', 'PlayerName' with your actual column names
df = pd.read_csv("datasetMerged.csv")
st.set_page_config(
    page_title="Player Market Price",
    page_icon=":soccer:",  # Change to your preferred icon
    layout="wide"
    
)
# Sidebar with tabs
selected_tab = st.sidebar.radio("Football Market analysis", ["Market Stats :chart:", "Player :athletic_shoe:"])
df_row = df[df["IMG_WyScout"].notnull()].sample(1)
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
    """
, unsafe_allow_html=True)
    


    player_attributes = {
        'Finishing': df_row["Finishing"].iloc[0],
        'Ball control': df_row["Ball control"].iloc[0],
        'Dribbling': df_row["Dribbling"].iloc[0],
        'Sprint speed': df_row["Sprint speed"].iloc[0],
        'Penalties': df_row["Penalties"].iloc[0],
    }

    # Calculate mean values for all players
    mean_attributes = {
        'Finishing': df["Finishing"].mean(),
        'Ball control': df["Ball control"].mean(),
        'Dribbling': df["Dribbling"].mean(),
        'Sprint speed': df["Sprint speed"].mean(),
        'Penalties': df["Penalties"].mean(),
    }

    # Radar Chart for Player Attributes
    fig_attributes = go.Figure()

    fig_attributes.add_trace(go.Scatterpolar(
        r=list(player_attributes.values()),
        theta=list(player_attributes.keys()),
        fill='toself',
        name='Player Attributes'
    ))

    fig_attributes.add_trace(go.Scatterpolar(
        r=list(mean_attributes.values()),
        theta=list(mean_attributes.keys()),
        fill='toself',
        name='Mean Attributes',
        line=dict(color='rgba(255, 0, 0, 0.5)'),  # Customize line color for mean
    ))

    fig_attributes.update_layout(
        margin=dict(t=0, r=75, b=110, l=75),
        height=350,
        width=350,
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 100], tickangle=0),
        ),
        showlegend=True,
    )

    # Create three columns


    # Display image in the first column

    col1, col2, col3 = st.columns((0.5,0.4,0.7),gap="small")
    with col1:
        st.subheader(str(df_row["name"].iloc[0]))
        url = df_row["IMG_WyScout"].iloc[0]
        if isinstance(url, str):
            st.image(url, use_column_width ="Always")  # Manually adjust the width of the image as per requirement
        else:
            st.image("https://cdn5.wyscout.com/photos/players/public/ndplayer_100x130.png", use_column_width =True)

    # Add content to other columns if needed
    with col2:
        st.info(f"Age: {df_row["Age"].iloc[0]} years")
        st.info(f"Height: {df_row["Height"].iloc[0]} cm")
        st.info(f"Footedness: {df_row["foot"].iloc[0]}")
    # Display the Plotly chart in Streamlit app




    with col3:
        st.plotly_chart(fig_attributes)

col11, col22 = st.columns((0.8,0.2))

with col11:
# Sample data for demonstration (replace with your actual data)
    player_stats = {
    'Crossing': df_row['Crossing'].iloc[0],
    'Finishing': df_row['Finishing'].iloc[0],
    'Heading accuracy': df_row['Heading accuracy'].iloc[0],
    'Short passing': df_row['Short passing'].iloc[0],
    'Volleys': df_row['Volleys'].iloc[0],
    'Dribbling': df_row['Dribbling'].iloc[0],
    'Curve': df_row['Curve'].iloc[0],
    'FK Accuracy': df_row['FK Accuracy'].iloc[0],
    'Long passing': df_row['Long passing'].iloc[0],
    'Ball control': df_row['Ball control'].iloc[0],
    'Acceleration': df_row['Acceleration'].iloc[0],
    'Sprint speed': df_row['Sprint speed'].iloc[0],
    'Agility': df_row['Agility'].iloc[0],
    'Reactions': df_row['Reactions'].iloc[0],
    'Balance': df_row['Balance'].iloc[0],
    'Shot power': df_row['Shot power'].iloc[0],
    'Jumping': df_row['Jumping'].iloc[0],
    'Stamina': df_row['Stamina'].iloc[0],
    'Strength': df_row['Strength'].iloc[0],
    'Long shots': df_row['Long shots'].iloc[0],
}
# Convert the dictionary to a DataFrame
    player_df = pd.DataFrame(list(player_stats.items()), columns=['Attribute', 'Player'])
# Find the top 5 stats for the player
    top_5_stats_player = player_df.nlargest(5, 'Player')
# Calculate the mean of the top 5 stats across all players
    mean_top_5_stats_all_players = df[top_5_stats_player['Attribute']].mean()
# Convert the mean values to a DataFrame
    mean_df = pd.DataFrame({'Attribute': mean_top_5_stats_all_players.index, 'Mean': mean_top_5_stats_all_players.values})
# Create separate traces for player and mean bars
    fig_stats_comparison = px.bar(
    pd.concat([top_5_stats_player, mean_df], keys=['Player', 'Mean']),
    x='Attribute',
    y=['Player','Mean'],
    labels={'Player': 'Stats', 'Attribute': 'Attribute'},
    title='Player Top 5 Stats vs Mean of Top 5 Stats for All Players',
)
# Customize the layout
    fig_stats_comparison.update_layout(barmode='group')  # Set barmode to 'group' for side-by-side bars
    fig_stats_comparison.update_layout(
    barmode='group',  # Set barmode to 'group' for side-by-side bars
    margin=dict(t=50, r=50, b=50, l=50),  # Set all margins to zero
) 
st.plotly_chart(fig_stats_comparison)

with col22:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# Display player value as a KPI
    # Display the plot in Streamlit app
    
    total_stats = str(df_row["Total stats"].iloc[0])
    st.metric("Total Stats", total_stats)

    player_value = df_row["Value"].iloc[0]
    player_value_in_millions = player_value / 1e6
# Display player value in millions with formatting
    player_value_formatted = f"${player_value_in_millions:.2f}M"
    st.metric("Player Value", player_value_formatted)