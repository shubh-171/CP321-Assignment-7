import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os


try:
    df = pd.read_csv("FIFA World Cup winners.csv")
except Exception as e:
    raise RuntimeError(f"Failed to load CSV file: {e}")


df = df.rename(columns=lambda x: x.strip().replace(" ", "").replace("-", ""))
df = df.rename(columns={"Winner": "Winner", "Runnerup": "RunnerUp"})  # fixed typo here

df['Winner'] = df['Winner'].replace({'WestGermany': 'Germany'})
df['RunnerUp'] = df['RunnerUp'].replace({'WestGermany': 'Germany'})

win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

app = dash.Dash(__name__)
server = app.server  # Required for deployment on Render

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={'textAlign': 'center'}),

    html.H3("World Cup Winners Choropleth Map"),
    dcc.Graph(id='choropleth',
              figure=px.choropleth(
                  win_counts,
                  locations="Country",
                  locationmode="country names",
                  color="Wins",
                  color_continuous_scale="Viridis",
                  title="FIFA World Cup Wins by Country"
              )),

    html.Br(),

    html.Label("Select a Country:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in sorted(win_counts['Country'])],
        placeholder="Select a country"
    ),
    html.Div(id='country-output'),

    html.Br(),

    html.Label("Select a Year:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': y, 'value': y} for y in sorted(df['Year'])],
        placeholder="Select a year"
    ),
    html.Div(id='year-output')
])


@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_info(country):
    if not country:
        return ""
    wins = win_counts[win_counts['Country'] == country]['Wins'].values[0]
    return f"{country} has won the FIFA World Cup {wins} times."


@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_info(year):
    if not year:
        return ""
    row = df[df['Year'] == year]
    if row.empty:
        return "No data available."
    winner = row['Winner'].values[0]
    runner = row['RunnerUp'].values[0]
    return f"In {year}, {winner} won the World Cup, and {runner} was the runner-up."


if __name__ == '__main__':
    app.run(debug=True)
