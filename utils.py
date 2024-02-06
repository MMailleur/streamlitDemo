# utils.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def calculate_player_attributes(df_row):
    player_attributes = {
        'Finishing': df_row["Finishing"].iloc[0],
        'Ball control': df_row["Ball control"].iloc[0],
        'Dribbling': df_row["Dribbling"].iloc[0],
        'Sprint speed': df_row["Sprint speed"].iloc[0],
        'Penalties': df_row["Penalties"].iloc[0],
    }
    return player_attributes

def calculate_mean_attributes(df):
    mean_attributes = {
        'Finishing': df["Finishing"].mean(),
        'Ball control': df["Ball control"].mean(),
        'Dribbling': df["Dribbling"].mean(),
        'Sprint speed': df["Sprint speed"].mean(),
        'Penalties': df["Penalties"].mean(),
    }
    return mean_attributes

def generate_player_stats_comparison(df_row, df):
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

    return top_5_stats_player, mean_df

def generate_player_stats_comparison_graph(top_5_stats_player, mean_df):
    # Create separate traces for player and mean bars
    fig_stats_comparison = px.bar(
        pd.concat([top_5_stats_player, mean_df], keys=['Player', 'Mean']),
        x='Attribute',
        y=['Player', 'Mean'],
        labels={'Player': 'Stats', 'Attribute': 'Attribute'},
        title='Player Top 5 Stats vs Mean of Top 5 Stats for All Players',
    )

    # Customize the layout
    fig_stats_comparison.update_layout(barmode='group')  # Set barmode to 'group' for side-by-side bars
    fig_stats_comparison.update_layout(
        # Set barmode to 'group' for side-by-side bars
        margin=dict(t=50, r=50, b=50, l=50),  # Set all margins to zero
        width=600,
        height=400
    )

    return fig_stats_comparison

def generate_player_attributes_comparison_graph(player_attributes, mean_attributes):
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
        margin=dict(t=20, r=75, b=110, l=75),
        height=300,
        width=400,
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 100], tickangle=0),
        ),
        showlegend=True,
    )

    return fig_attributes

def format_market_value(value):
    if value >= 1e6:  # If the value is greater than or equal to 1 million
        return f"{value / 1e6:.1f}M€"
    elif value >= 1e3:  # If the value is greater than or equal to 1 thousand
        return f"{value / 1e3:.0f}k€"
    else:  # For values less than 1 thousand
        return f"{value:.0f}€"