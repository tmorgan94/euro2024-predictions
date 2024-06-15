import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title('⚽ Euro 2024 - Prediction Game')

# Mapping for country flags
country_flags = {
    "Germany": "🇩🇪",
    "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Spain": "🇪🇸",
    "Croatia": "🇭🇷",
    "Serbia": "🇷🇸",
    "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Austria": "🇦🇹",
    "France": "🇫🇷",
    "Portugal": "🇵🇹",
    "Czech Republic": "🇨🇿",
    "Switzerland": "🇨🇭",
    "Italy": "🇮🇹",
    "Denmark": "🇩🇰",
    "Netherlands": "🇳🇱",
    "Belgium": "🇧🇪",
    "Romania": "🇷🇴",
    "Hungary": "🇭🇺",
    "Slovenia": "🇸🇮",
    "Ukraine": "🇺🇦"
}

# Read data from CSV
results = pd.read_csv('data/results.csv')
filtered_results = results.dropna(subset=['actual_score'])

# Find the latest matchday
latest_matchday = filtered_results['matchday'].max()

# Filter data based on the latest matchday
filtered_results = filtered_results[filtered_results['matchday'] == latest_matchday]

# Create a dynamic heading
st.header(f"Matchday {latest_matchday}")

# Display the filtered data
columns = st.columns(5)
for i, (index, row) in enumerate(filtered_results.iterrows()):
    col = columns[i % 5]
    home_flag = country_flags.get(row['home'], "🏴")
    away_flag = country_flags.get(row['away'], "🏴")
    col.metric(f"{home_flag} v {away_flag}", row['actual_score'])

st.header('Highlights')

# Load your overall standings DataFrame
overall_standings_df = pd.read_csv('data/overall_standings.csv')

# Find the current leader
current_leader = overall_standings_df.loc[overall_standings_df['position'] == 1, 'name'].values[0]

# Find the biggest gainer
# First, identify the maximum rank change
max_rank_change = overall_standings_df['rank_change'].max()

# Then, filter the DataFrame to include only players with the maximum rank change
potential_biggest_gainers = overall_standings_df[overall_standings_df['rank_change'] == max_rank_change]

# If there's only one potential biggest gainer, select it directly
if len(potential_biggest_gainers) == 1:
    biggest_gainer = potential_biggest_gainers.iloc[0]['name']
else:
    # If there are multiple potential biggest gainers, break the tie using latest matchday points
    latest_matchday_points = potential_biggest_gainers.groupby('name')['cumulative_total_points'].last()
    biggest_gainer = latest_matchday_points.idxmax()

# Find the biggest loser
# First, identify the minimum rank change
min_rank_change = overall_standings_df['rank_change'].min()

# Then, filter the DataFrame to include only players with the minimum rank change
potential_biggest_losers = overall_standings_df[overall_standings_df['rank_change'] == min_rank_change]

# If there's only one potential biggest loser, select it directly
if len(potential_biggest_losers) == 1:
    biggest_loser = potential_biggest_losers.iloc[0]['name']
else:
    # If there are multiple potential biggest losers, break the tie using latest matchday points
    latest_matchday_points = potential_biggest_losers.groupby('name')['cumulative_total_points'].last()
    biggest_loser = latest_matchday_points.idxmin()

# Define CSS styling for the cards
css = """
<style>
.metric-card {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.card-title {
    font-size: 18px;
    font-weight: normal;
}
.card-value {
    font-size: 24px;
    font-weight: bold;
}
</style>
"""

# Display the CSS styling
st.markdown(css, unsafe_allow_html=True)

# Display the metrics using st.metric within three columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3 class="card-title">🏆 Leader</h3>
            <p class="card-value">{current_leader}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3 class="card-title">🔥 Biggest Gainer</h3>
            <p class="card-value">{biggest_gainer}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3 class="card-title">💀 Biggest Loser</h3>
            <p class="card-value">{biggest_loser}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.header('Points')

# read data 
points_by_name = pd.read_csv('data/points_by_name.csv')

# Create the bar chart
fig = px.bar(points_by_name, x='name', y='total_points', 
             color='name',
             labels={'name': 'Name', 'Points': 'Total Points'},
             title='Euro 2024 Total Points by Name',  # Updated title
             color_discrete_sequence=['#ffd700', '#C0C0C0', '#B87333', # gold, silver, bronze for 1st, 2nd, 3rd
                                      '#F64271', '#F64271', '#F64271', '#F64271', '#F64271', '#F64271', '#F64271', '#F64271', '#F64271', '#F64271'])  # red for all others

# Customize the layout
fig.update_layout(
    xaxis_title=' ',
    yaxis_title='Total Points',
    font=dict(family='Arial', size=12),
    title_font=dict(family='Arial', size=16),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False,  # Hide the legend
    legend_title_text='Legend',
    legend_font=dict(family='Arial', size=10),
    legend_traceorder='reversed'
)

# Display the plot in Streamlit app
st.plotly_chart(fig)

# Read data
vs_mean_match_code_df = pd.read_csv('data/vs_mean_match_code_df.csv')

# Define the symbols for rank change
def rank_change_symbol(change):
    if change >= 2:
        return '🔥'  # Player moved up in rank by 2 or more
    elif change == 1:
        return '👍'  # Player moved up in rank by 1
    elif change == -1:
        return '😵'  # Player moved down in rank by 1
    elif change <= -2:
        return '💀'  # Player moved down in rank by 2 or more
    else:
        return '🥱'  # No change in rank

# Apply rank change symbols and convert to string
overall_standings_df['rank_change_symbol'] = overall_standings_df['rank_change'].apply(rank_change_symbol)

# Define the column configurations for the DataFrame
column_config = {
    "name": "Name",
    "position": "Rank",
    "rank_change": "Rank Change",
    "rank_change_symbol": "Reaction",
    "cumulative_total_points": "Total Points",
    "points_change": "Latest Matchday Points",
    "difference": st.column_config.LineChartColumn(
        "Trend (Δ vs Mean)",
        y_min=vs_mean_match_code_df['difference'].min(),
        y_max=vs_mean_match_code_df['difference'].max(),
    ),
}

# Reorder the columns
overall_standings_df = overall_standings_df[['name', 'position', 'rank_change', 'rank_change_symbol', 'cumulative_total_points', 'points_change', 'difference']]

# Display the DataFrame with column configurations
st.dataframe(
    overall_standings_df,
    column_config=column_config,
    hide_index=True,
)

st.markdown("""
---            
## Trends
            """)

colors_names = {
    "Corfe": "#FFA500",
    "Ed": "#e4010b",
    "Jay": "#004ea0",
    "Jonny": "#00a85d",
    "Larry": "#ffd600",
    "Luke": "#66c0f4",
    "Marc": "#000000",
    "Peter Popular": "#69ffb4",
    "Rando Randal": "#ff69b4",
    "Tom": "#8a2be2"
}

df_merged = pd.read_csv('data/df_merged.csv')

# Create a new dataframe containing necessary columns
plot_df = df_merged[['timestamp', 'name', 'match_code', 'home', 'away', 'predicted_score', 'actual_score', 'total_points']].copy()

# Get unique match codes from the DataFrame
match_codes_unique = df_merged['match_code'].unique()

# Sort the match codes
match_code_order = sorted(match_codes_unique, key=lambda x: int(x[1:]))

# Convert match_code to categorical and set the order
plot_df['match_code'] = pd.Categorical(plot_df['match_code'], categories=match_code_order, ordered=True)

# Sort the dataframe based on match_code order
plot_df = plot_df.sort_values(by='match_code')

# Calculate the cumulative sum of total_points
plot_df['cumulative_total_points'] = plot_df.groupby('name')['total_points'].cumsum()

# Assuming plot_df is your dataframe

# Add initial data points for each player
initial_points = plot_df[['name']].drop_duplicates()
initial_points['match_code'] = 'M00'
initial_points['cumulative_total_points'] = 0
initial_points['home'] = ''
initial_points['away'] = ''
initial_points['total_points'] = 0
initial_points['predicted_score'] = ''
initial_points['actual_score'] = ''

# Concatenate the initial points with the original dataframe
plot_df = pd.concat([initial_points, plot_df], ignore_index=True).sort_values(by=['name', 'match_code'])

# Create traces for each name
traces = []
for name, group in plot_df.groupby('name'):
    trace = go.Scatter(
        x=group['match_code'], 
        y=group['cumulative_total_points'], 
        mode='lines+markers', 
        name=name,
        text=group.apply(lambda row: f"Player: {row['name']}<br>{row['home']} vs {row['away']}<br>Matchday Points: {row['total_points']}<br>Predicted Score: {row['predicted_score']}<br>Actual Score: {row['actual_score']}", axis=1),
        hovertemplate='<b>%{text}</b><br>Match: %{x}<br>Cumulative Points: %{y}<extra></extra>',
        line=dict(color=colors_names[name])
    )
    traces.append(trace)

# Create the layout
layout = go.Layout(
    title='Cumulative Points Over Time',
    xaxis=dict(title=' '),
    yaxis=dict(title='Cumulative Total Points'),
    legend=dict(orientation='v')
)

# Create the figure
fig = go.Figure(data=traces, layout=layout)

# Streamlit app
st.plotly_chart(fig)

vs_mean_df = pd.read_csv('data/vs_mean_df.csv')

# Plotly line graph
fig = px.line(
    vs_mean_df, 
    x='stage_detail', 
    y='difference', 
    color='name', 
    color_discrete_map=colors_names,
    markers=True, 
    labels={'stage_detail': 'Matchday', 'difference': 'Difference from Mean'},
    title='Difference from Mean Total Points by Matchday'
)

# Customize the layout to match the previous bar plot
fig.update_layout(
    xaxis_title='Matchday',
    yaxis_title='Difference from Mean',
    font=dict(family='Arial', size=12),
    title_font=dict(family='Arial', size=16),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend_title_text=' ',
    legend_font=dict(family='Arial', size=10),
    yaxis=dict(gridcolor='rgba(0,0,0,0)')  # Set gridline color to transparent
)

# Streamlit app
st.plotly_chart(fig)