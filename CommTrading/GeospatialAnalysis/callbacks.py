import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import html, Patch
from dash.dependencies import Input, Output, State
from dash_iconify import DashIconify

from CommTrading import constants
from CommTrading.GeospatialAnalysis import plotly_visuals, data_processing


def add_ga_callbacks(app: dash.Dash):
    @app.callback(
        Output("map_fig", "figure"),
        Input("gs_button_apply", "n_clicks"),
        State("gs_dropdown_options", "value"),
        prevent_initial_call=True
    )
    def filter_map(clicks, selected_countries):
        df = pd.read_csv(constants.CSV_FILE_DIRECTORY)
        map_df = data_processing.process_map_df(df)

        map_df = map_df[map_df['Country/Area'].isin(selected_countries)]
        patched_figure = Patch()
        patched_figure["data"][0]["locations"] = map_df['Country/Area']
        patched_figure["data"][0]["z"] = map_df['Number of Trades']
        return patched_figure

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

    @app.callback(
        [
            Output("gs_dropdown_icon", "children"),
            Output("gs_dropdown_badge", "children"),
        ],
        [
            Input("gs_dropdown_popover", "is_open"),
            Input("gs_dropdown_options", "value"),
        ],
    )
    def gs_update_dropdown(is_open, selected_materials):

        ctx = dash.callback_context
        initial_call = ctx.triggered[0]["prop_id"] == "."
        up_icon = DashIconify(
            icon="bxs:up-arrow",
            inline=True,
        )

        down_icon = DashIconify(
            icon="bxs:down-arrow",
            inline=True,
        )

        icons_pop_over_mapping = {True: up_icon,
                                  False: down_icon
                                  }
        if initial_call:
            if selected_materials:
                count = len(selected_materials)
                return dash.no_update, count

            else:
                count = 0
                return dash.no_update, count

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == "sc_dropdown_material_id_popover":
            return icons_pop_over_mapping[is_open], dash.no_update

        else:
            if selected_materials:
                count = len(selected_materials)
                return icons_pop_over_mapping[is_open], count

            else:
                count = 0
                return icons_pop_over_mapping[is_open], count

    @app.callback(
        [Output("gs_dropdown_options", "options"),
         Output('gs_no_search_results', 'children')],
        [Input('gs_dropdown_search_input', 'value'),
         Input("gs_dropdown_popover", "is_open")
         ],
        prevent_initial_call=True
    )
    def search_output(
            search_value,
            popover_open
    ):

        df = pd.read_csv(constants.CSV_FILE_DIRECTORY)
        map_df = data_processing.process_map_df(df)
        countries_options = map_df['Country/Area'].unique().tolist()

        ctx = dash.callback_context
        initial_call = ctx.triggered[0]["prop_id"] == "."
        if initial_call:
            return countries_options, ''

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == 'gs_dropdown_search_input':
            matching_countries_options = [option for option in countries_options if
                                          search_value.lower() in option.lower()]
            if not matching_countries_options:
                return [], 'No Results Found..'

            return matching_countries_options, ''

        return countries_options, ''

    @app.callback(
        Output("gs_dropdown_options", "value"),
        [
            Input("gs_dropdown_clear", "n_clicks"),
            Input("gs_dropdown_select", "n_clicks"),
        ],
        State("gs_dropdown_options", "options"),
        prevent_initial_call=True,
    )
    def clear_options(clicks1, clicks2, available_options):

        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "gs_dropdown_clear":
            return []
        else:
            return [option for option in available_options]

    @app.callback(
        Output("gs_button_apply", "disabled"),
        Input("gs_dropdown_options", "value"),
        # prevent_initial_call=True
    )
    def apply_button_state(selected_options):

        if not selected_options:
            return True

        else:
            return False
