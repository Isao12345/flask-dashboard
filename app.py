# simple Dash app demonstrating interactive mobile sales charts
# minimal layout, three graphs, and early/oft commits as requested
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import logging

# load local dataset (CSV contains all 2025 mobile sales records)
DATA_PATH = 'synthetic_mobile_sales_2025.csv'
# read into pandas DataFrame for later filtering
df = pd.read_csv(DATA_PATH)

# helper for filtering by brand/country

def filter_df(brand=None, country=None):
    d = df
    if brand is not None:
        d = d[d['Brand'] == brand]
    if country is not None:
        d = d[d['Country'] == country]
    return d

app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}])

logging.basicConfig(level=logging.INFO)
logging.info('app initialized with meta tags')

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
            placeholder='Select brand',
            clearable=False
        ),
        html.Label('Country:'),
        dcc.Dropdown(
            id='country-dd',
            options=[{'label': c, 'value': c} for c in sorted(df['Country'].unique())],
            value=sorted(df['Country'].unique())[0],
            placeholder='Select country',
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
    # filter dataframe by selected brand
    dff = filter_df(brand=brand)
    fig = px.line(dff.groupby('Sale_Month', as_index=False)['Revenue_USD'].sum(),
                  x='Sale_Month', y='Revenue_USD', title=f'Revenue for {brand}', markers=True)
    return fig

@callback(Output('graph2', 'figure'), Input('country-dd', 'value'))
def fig2(country):
    # filter by chosen country
    dff = filter_df(country=country)
    fig = px.bar(dff.groupby('Brand', as_index=False)['Units_Sold'].sum(),
                 x='Units_Sold', y='Brand', orientation='h', title=f'Units in {country}')
    return fig

@callback(
    Output('graph3', 'figure'),
    Input('brand-dd', 'value'),
    Input('country-dd', 'value')
)
def fig3(brand, country):
    # scatter of price vs rating for selected brand/country
    dff = filter_df(brand=brand, country=country)
    if dff.empty:
        # nothing to show
        return px.scatter(title='No data for selected combination')
    fig = px.scatter(dff, x='Price_USD', y='Customer_Rating', size='Units_Sold',
                     title=f'Price vs Rating ({brand} in {country})')
    return fig

if __name__ == '__main__':
    # run the dash server
    app.run(debug=True)

# commit early, commit often!
