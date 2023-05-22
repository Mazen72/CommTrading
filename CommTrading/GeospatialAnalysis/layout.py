import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import dcc, html

from CommTrading import constants, common
from CommTrading.GeospatialAnalysis import plotly_visuals, data_processing


def get_map_col(df):
    info_text = html.Div('Hover over a country to see more info..', className='table_header',
                         style=dict(fontSize='1.6vh', paddingTop='1rem', color='black',
                                    textAlign="left", paddingLeft='2rem', paddingBottom='1rem'))

    map_df = data_processing.process_map_df(df)
    unique_countries = map_df['Country/Area'].unique().tolist()
    countries_dropdown = common.create_custom_dropdown(
        filter_name="Selected Countries",
        filter_options=unique_countries,
        filter_value=unique_countries,
        filter_style=dict(padding='', width='fit-content'),
        filter_id="gs_dropdown",
        options_id="gs_dropdown_options",
        popover_id="gs_dropdown_popover",
        badge_id="gs_dropdown_badge",
        icon_id="gs_dropdown_icon",
        search_input_id='gs_dropdown_search_input',
        no_results_id='gs_no_search_results',
        clear_id="gs_dropdown_clear",
        select_all_id="gs_dropdown_select",
        apply_id='gs_button_apply'
    )

    countries_dropdown = dmc.Group(countries_dropdown, position='center')

    map_fig = plotly_visuals.get_map_figure(map_df)

    map_graph = dcc.Graph(figure=map_fig, config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                          id='map_fig', className='', clear_on_unhover=True,
                          style=dict(width='100%', height=''))

    map_graph = dbc.Spinner([map_graph],
                            size="lg", color="primary", type="border",
                            fullscreen=False, delay_show=1000)

    graph_tooltip = dcc.Tooltip(id="graph_tooltip")

    map_header = common.header_with_icon_div(icon_name='tabler:world-search',
                                             header_text='Countries Overall Number of Trades',
                                             icon_color='#272727',
                                             icon_size='1.5rem',
                                             header_size='1.2rem'
                                             )

    map_card = dmc.Card(children=[dmc.CardSection(map_header,
                                                  withBorder=True,
                                                  inheritPadding=True,
                                                  py='sm',
                                                  style=dict(paddingLeft='1rem')
                                                  ),
                                  dmc.Space(h=7),
                                  countries_dropdown,
                                  info_text,
                                  dmc.Center(map_graph),
                                  graph_tooltip
                                  ],
                        withBorder=True,
                        shadow="sm",
                        radius="md",

                        )

    map_col = dmc.Col(map_card,
                      xs=12, sm=12, md=12, lg=10, xl=10,
                      style=dict(paddingTop=''))

    return map_col


def geospatial_analysis_layout():
    df = pd.read_csv(constants.CSV_FILE_DIRECTORY)

    map_col = get_map_col(df)

    layout = dmc.Grid([map_col], justify='center')

    return layout
