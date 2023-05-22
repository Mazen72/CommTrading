import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import dcc, html
from dash.dcc import Download
from dash_iconify import DashIconify

from CommTrading import constants, common
from CommTrading.HistoricalAnalysis import plotly_visuals, data_processing


def get_kpis_cols(df):
    countries_num = df['country_or_area'].nunique()

    years_range = '{} - {}'.format(df['year'].min(), df['year'].max())

    comm_types = df['category'].nunique()

    comm_products = df['commodity'].nunique()

    flows_count = df['flow'].value_counts()
    total_imports = flows_count['Import'] + flows_count['Re-Import']
    total_exports = flows_count['Export'] + flows_count['Re-Export']
    titles = ['No. Countries', 'Years Range', 'No. Categories',
              'No. Products', 'Total Imports', 'Total Exports']
    values = [countries_num, years_range, comm_types, comm_products, total_imports, total_exports]

    icons = ['fluent-mdl2:world', 'material-symbols:date-range',
             'material-symbols:category', 'fluent-mdl2:product-variant',
             'solar:import-linear', 'solar:export-linear'
             ]
    stats_cols = []
    for title, value, icon in zip(titles, values, icons):
        div = common.content_with_icon_div(icon, constants.DASHBOARD_MAIN_COLOR1, title, value)
        card = dmc.Card(children=[div],
                        withBorder=True,
                        shadow="sm",
                        radius="md",

                        )
        col = dmc.Col(children=card,
                      xl=2, lg=2, md=4, sm=6, xs=6, span=6,
                      style=dict()
                      )
        stats_cols.append(col)

    return stats_cols


def get_trades_num_col(df):
    countries = df['country_or_area'].unique().tolist()
    comm_categories = df['category'].unique().tolist()
    comm_categories.insert(0, 'All Categories')

    countries_menu1 = dmc.Select(
        data=[{'label': country, 'value': country} for country in countries],
        value=countries[4], label='Country',
        id='countries_menu1', searchable=True,
        style=dict(width='')
    )

    categories_menu1 = dmc.Select(
        data=[{'label': category, 'value': category} for category in comm_categories],
        value=comm_categories[0], label='Category',
        id='categories_menu1', searchable=True,
        style=dict(width='')
    )

    chart_types = [['Area', 'Area Chart'], ['Line', 'Line Chart']]
    chart_type_options = dmc.RadioGroup(children=[dmc.Radio(l, value=v) for v, l in chart_types],
                                        value='Area',
                                        id="chart_type_options",
                                        label="Chart Type",
                                        size="xs",
                                        mt=5,
                                        offset=4
                                        )

    options1_row = dmc.Group(children=[countries_menu1, categories_menu1, chart_type_options],
                             spacing=15,
                             align='center',
                             position='left'
                             )

    trades_num_df = data_processing.get_trades_num_figure_df(df, countries[4], comm_categories[0])
    trades_num_fig = plotly_visuals.get_trades_num_figure(trades_num_df, 'Area')
    trades_num_graph = dcc.Graph(figure=trades_num_fig,
                                 config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                                 id='trades_num_fig', className='trades_num_graph',
                                 style=dict(width='', height=''))

    trades_num_graph = dbc.Spinner([trades_num_graph], size="lg", color="primary", type="border",
                                   fullscreen=False)

    trades_num_header = common.header_with_icon_div(icon_name='icon-park-outline:trend-two',
                                                    header_text='Number of Trades',
                                                    icon_color='#272727',
                                                    icon_size='1.5rem',
                                                    header_size='1.2rem'
                                                    )
    trades_num_card = dmc.Card(children=[dmc.CardSection(trades_num_header,
                                                         withBorder=True,
                                                         inheritPadding=True,
                                                         py='sm',
                                                         style=dict(paddingLeft='1rem')
                                                         ),
                                         dmc.Space(h=7),
                                         options1_row,
                                         trades_num_graph
                                         ],
                               withBorder=True,
                               shadow="sm",
                               radius="md",

                               )
    trades_num_col = dmc.Col([trades_num_card],
                             xs=12, sm=12, md=6, lg=6, xl=6,
                             style=dict()
                             )
    return trades_num_col


def get_trades_balance_col(df):
    countries = df['country_or_area'].unique().tolist()

    countries_menu2 = dmc.Select(
        data=[{'label': country, 'value': country} for country in countries],
        value=countries[2], label='Country',
        id='countries_menu2', searchable=True,
        style=dict(maxWidth='40%')
    )

    trades_balance, years = data_processing.get_trade_balance_fig_data(df, countries[2])
    trades_balance_fig = plotly_visuals.get_balance_figure(countries[2], trades_balance, years)
    trades_balance_graph = dcc.Graph(figure=trades_balance_fig,
                                     config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                                     id='trades_balance_fig', className='trades_balance_graph',
                                     style=dict(width='', height=''))

    trades_balance_graph = dbc.Spinner([trades_balance_graph], size="lg", color="primary", type="border",
                                       fullscreen=False)

    trades_balance_header = common.header_with_icon_div(icon_name='vaadin:scale-unbalance',
                                                        header_text='Balance of Trades (exports-imports)',
                                                        icon_color='#272727',
                                                        icon_size='1.5rem',
                                                        header_size='1.2rem'
                                                        )

    trades_balance_card = dmc.Card(children=[dmc.CardSection(trades_balance_header,
                                                             withBorder=True,
                                                             inheritPadding=True,
                                                             py='sm',
                                                             style=dict(paddingLeft='1rem')
                                                             ),
                                             dmc.Space(h=7),
                                             countries_menu2,
                                             trades_balance_graph
                                             ],
                                   withBorder=True,
                                   shadow="sm",
                                   radius="md",

                                   )

    trades_balance_col = dmc.Col([trades_balance_card],
                                 xs=12, sm=12, md=6, lg=6, xl=6,
                                 style=dict())

    return trades_balance_col


def get_top10_col(df):
    flows = df['flow'].unique().tolist()

    trades_type_options = dmc.ChipGroup(children=[dmc.Chip(flow + 's', value=flow) for flow in flows],
                                        value=flows[0],
                                        id="trades_type_options",

                                        )

    top10_df = data_processing.get_top10_df(df, 'Export')
    top10_fig = plotly_visuals.get_top10_chart(top10_df, 'Export')
    top10_graph = dcc.Graph(figure=top10_fig, config={'displaylogo': False,
                                                      'modeBarButtonsToRemove': ['lasso2d', 'pan', 'zoom2d',
                                                                                 'zoomIn2d', 'zoomOut2d',
                                                                                 'autoScale2d']},
                            id='top10_fig', className='trades_balance_graph',
                            style=dict(width='', height=''))

    top10_graph = dbc.Spinner([top10_graph], size="lg", color="primary", type="border",
                              fullscreen=False)

    top10_header = common.header_with_icon_div(icon_name='mdi:arrow-up-right-bold-outline',
                                               header_text='Top 10 Countries with Trades',
                                               icon_color='#272727',
                                               icon_size='1.5rem',
                                               header_size='1.2rem'
                                               )

    top10_card = dmc.Card(children=[dmc.CardSection(top10_header,
                                                    withBorder=True,
                                                    inheritPadding=True,
                                                    py='sm',
                                                    style=dict(paddingLeft='1rem')
                                                    ),
                                    dmc.Space(h=9),
                                    trades_type_options,
                                    top10_graph
                                    ],
                          withBorder=True,
                          shadow="sm",
                          radius="md",

                          )

    top10_col = dmc.Col([top10_card],
                        xs=12, sm=12, md=6, lg=6, xl=6,
                        style=dict(
                        ))

    return top10_col


def get_table_col(df):
    table_df = data_processing.get_trade_balance_table_df(df)
    trades_balance_table = plotly_visuals.get_trade_balance_table(table_df)
    trades_balance_table = dbc.Spinner([trades_balance_table], size="lg", color="primary", type="border",
                                       fullscreen=False)

    table_header = common.header_with_icon_div(icon_name='material-symbols:database-outline',
                                               header_text='Balance of Trade Raw Data',
                                               icon_color='#272727',
                                               icon_size='1.5rem',
                                               header_size='1.2rem'
                                               )

    download_excel = html.Div([Download(id="download_excel")])

    download_excel_button = dmc.Button(
        "Export to Excel", id="download_excel_button", n_clicks=0, size='xs',
        variant='outline',
        leftIcon=DashIconify(icon="ph:export-bold")
    )

    download_excel_div = html.Div([download_excel, download_excel_button])

    trades_balance_table_card = dmc.Card(children=[dmc.CardSection(table_header,
                                                                   withBorder=True,
                                                                   inheritPadding=True,
                                                                   py='sm',
                                                                   style=dict(paddingLeft='1rem')
                                                                   ),
                                                   dmc.Space(h=9),
                                                   download_excel_div,
                                                   dmc.Space(h=7),
                                                   trades_balance_table
                                                   ],
                                         withBorder=True,
                                         shadow="sm",
                                         radius="md",

                                         )

    trades_balance_table_col = dmc.Col([trades_balance_table_card],
                                       xs=12, sm=12, md=6, lg=6, xl=6,
                                       style=dict(
                                       ))

    return trades_balance_table_col


def historical_analysis_layout():
    df = pd.read_csv(constants.CSV_FILE_DIRECTORY)

    trades_num_col = get_trades_num_col(df)

    trades_balance_col = get_trades_balance_col(df)

    top10_col = get_top10_col(df)

    trades_balance_table_col = get_table_col(df)

    stats_cols = get_kpis_cols(df)

    stats_div = dmc.Grid(children=stats_cols,
                         align="center",
                         justify="center",
                         gutter="md",
                         style=dict(paddingLeft='1.5rem', paddingRight='1.5rem')

                         )

    layout = html.Div([stats_div,
                       dmc.Space(h=15),
                       dmc.Grid([trades_num_col,
                                 trades_balance_col, top10_col, trades_balance_table_col],
                                gutter=12, style=dict(paddingLeft='1.3rem', paddingRight='1.3rem')
                                ),
                       dmc.Space(h=20)
                       ])
    return layout
