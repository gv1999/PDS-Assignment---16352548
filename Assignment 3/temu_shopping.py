pip install dash

import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Function to fetch data from Temu.com Shopping API
def fetch_data(keyword):
    url = "https://temu-com-shopping-api-realtime-api-scrapper-from-temu-com.p.rapidapi.com/search"
    headers = {
        'X-RapidAPI-Key': '74796b5297msh59776bf458fbd47p1aea5fjsnab96a3fd6a70',
        'X-RapidAPI-Host': 'temu-com-shopping-api-realtime-api-scrapper-from-temu-com.p.rapidapi.com'
    }
    params = {'keyword': keyword}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout of the dashboard
app.layout = html.Div([
    dcc.Input(id='keyword-input', type='text', value='shoes'),
    html.Button('Search', id='search-button', n_clicks=0),
    html.Div(id='output-container')
])

# Define callback to update output based on keyword input
@app.callback(
    Output('output-container', 'children'),
    [Input('search-button', 'n_clicks')],
    [dash.dependencies.State('keyword-input', 'value')]
)
def update_output(n_clicks, keyword):
    if n_clicks > 0:
        data = fetch_data(keyword)
        # Process the data and format it for display
        # For simplicity, let's just display the raw JSON data
        return html.Pre(children=str(data))
    else:
        return ''

if __name__ == '__main__':
    app.run_server(debug=True)
