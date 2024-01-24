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
    