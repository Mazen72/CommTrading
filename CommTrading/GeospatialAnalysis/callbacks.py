import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import html
from dash.dependencies import Input, Output

from CommTrading import constants
from CommTrading.GeospatialAnalysis import plotly_visuals


def add_ga_callbacks(app: dash.Dash):
    @app.callback(
        [Output("graph_tooltip", "show"),
         Output("graph_tooltip", "bbox"),
         Output("graph_tooltip", "children")],
        Input("map_fig", "hoverData")
        , prevent_initial_call=True
    )
    def display_map_hover(hoverData):
        if hoverData is None:
            return False, dash.no_update, dash.no_update

        pt = hoverData["points"][0]
        bbox = pt["bbox"]

        country_div = html.Div('Country: {}'.format(pt['location']), className='table_header',
                               style=dict(fontSize='1.4vh', fontWeight='bold', color='black',
                                          textAlign="left", width='100%'))

        trades_div = html.Div('Number of Trades: {}'.format(pt['z']), className='table_header',
                              style=dict(fontSize='1.4vh', fontWeight='bold', color='black',
                                         textAlign="left", width='100%'))

        df = pd.read_csv(constants.CSV_FILE_DIRECTORY)
        dff = df[df['country_or_area'] == pt['location']]
        dff = dff.groupby(['flow'])['commodity'].count()

        pie = plotly_visuals.get_map_pie(dff)

        children = [country_div, trades_div, dmc.Space(h=10), pie]

        return True, bbox, children
