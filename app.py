# simple Dash app demonstrating interactive mobile sales charts
# minimal layout, three graphs, and early/oft commits as requested
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# load local dataset (CSV contains all 2025 mobile sales records)
DATA_PATH = 'synthetic_mobile_sales_2025.csv'
# read into pandas DataFrame for later filtering
df = pd.read_csv(DATA_PATH)

app = Dash(__name__)

# minimal layout with two selectors and three graphs
# selectors live in a centered div
app.layout = html.Div([
    html.H2('Sales Dashboard — Minimal Version', style={'textAlign': 'center'}),
    html.Div([
        html.Label('Brand:'),
        dcc.Dropdown(
            id='brand-dd',
            options=[{'label': b, 'value': b} for b in sorted(df['Brand'].unique())],
            value=sorted(df['Brand'].unique())[0],
            clearable=False
        ),
        html.Label('Country:'),
        dcc.Dropdown(
            id='country-dd',
            options=[{'label': c, 'value': c} for c in sorted(df['Country'].unique())],
            value=sorted(df['Country'].unique())[0],
            clearable=False
        )
    ], style={'width': '40%', 'margin': '20px auto'}),
    html.Div([
        dcc.Graph(id='graph1'),
        dcc.Graph(id='graph2'),
        dcc.Graph(id='graph3')
    ])
])

@callback(Output('graph1', 'figure'), Input('brand-dd', 'value'))
def fig1(brand):
    dff = df[df['Brand'] == brand]
    fig = px.line(dff.groupby('Sale_Month', as_index=False)['Revenue_USD'].sum(),
                  x='Sale_Month', y='Revenue_USD', title=f'Revenue for {brand}')
    return fig

@callback(Output('graph2', 'figure'), Input('country-dd', 'value'))
def fig2(country):
    dff = df[df['Country'] == country]
    fig = px.bar(dff.groupby('Brand', as_index=False)['Units_Sold'].sum(),
                 x='Brand', y='Units_Sold', title=f'Units in {country}')
    return fig

@callback(
    Output('graph3', 'figure'),
    Input('brand-dd', 'value'),
    Input('country-dd', 'value')
)
def fig3(brand, country):
    dff = df[(df['Brand'] == brand) & (df['Country'] == country)]
    fig = px.scatter(dff, x='Price_USD', y='Customer_Rating', size='Units_Sold',
                     title='Price vs Rating')
    return fig

if __name__ == '__main__':
    app.run(debug=True)
