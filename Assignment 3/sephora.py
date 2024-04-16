import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#Fetch store data from Sephora API
#API Link: https://rapidapi.com/apidojo/api/sephora
def get_store_data(latitude, longitude, radius):
    url = "https://sephora.p.rapidapi.com/stores/list"
    headers = {
        "X-RapidAPI-Key": "5451d414b9msha78109cba638aa7p114042jsn4c6d549abdd8", # My Rapid API Key
        "X-RapidAPI-Host": "sephora.p.rapidapi.com"
    }
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Sephora Store Locator"),
    dcc.Input(id='latitude-input', type='text', placeholder='Latitude'),
    dcc.Input(id='longitude-input', type='text', placeholder='Longitude'),
    dcc.Input(id='radius-input', type='text', placeholder='Radius (in miles)'),
    html.Button('Search', id='search-button', n_clicks=0),
    html.Div(id='store-output')
])

@app.callback(
    Output('store-output', 'children'),
    [Input('search-button', 'n_clicks')],
    [dash.dependencies.State('latitude-input', 'value'),
     dash.dependencies.State('longitude-input', 'value'),
     dash.dependencies.State('radius-input', 'value')]
)
def update_store_output(n_clicks, latitude, longitude, radius):
    if n_clicks > 0 and latitude and longitude and radius:
        store_data = get_store_data(latitude, longitude, radius)
        stores = store_data.get('stores', [])
        if stores:
            store_list = html.Ul([
                html.Li(f"{store.get('name', 'Unknown')} - {store.get('address', 'Unknown')}, "
                        f"{store.get('city', 'Unknown')}, {store.get('state', 'Unknown')} {store.get('postal_code', 'Unknown')}")
                for store in stores
            ])
            return store_list
        else:
            return html.P("No stores found in the specified location and radius.")
    else:
        return html.P("Enter latitude, longitude, and radius, then click 'Search' to find stores.")

if __name__ == '__main__':
    app.run_server(debug=True)
