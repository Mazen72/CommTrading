import dash
import pandas as pd
from dash.dcc import send_data_frame
from dash.dependencies import Input, Output, State

from CommTrading import constants
from CommTrading.HistoricalAnalysis import plotly_visuals, data_processing


def add_ha_callbacks(app: dash.Dash):
    @app.callback(Output('download_excel', 'data'),
                  Input('download_excel_button', 'n_clicks'), State('trade_balance_table', 'data')

        , prevent_initial_call=True)
    def export_to_excel(clicks, data):
        trade_balance_df = pd.DataFrame(data)
        return send_data_frame(trade_balance_df.to_excel, "Balance_of_Trade.xlsx")

    @app.callback(Output('trades_num_fig', 'figure'),
                  [Input('countries_menu1', 'value'), Input('categories_menu1', 'value'),
                   Input('chart_type_options', 'value')]
        , prevent_initial_call=True)
    def update_trades_num_figure(selected_country, selected_category, selected_chart_type):
        df = pd.read_csv(constants.CSV_FILE_DIRECTORY)
        graph_df = data_processing.get_trades_num_figure_df(df, selected_country, selected_category)
        fig = plotly_visuals.get_trades_num_figure(graph_df, selected_chart_type)

        return fig

    @app.callback(Output('trades_balance_fig', 'figure'),
                  Input('countries_menu2', 'value')
        , prevent_initial_call=True)
    def update_trades_balance_figure(selected_country):
        df = pd.read_csv(constants.CSV_FILE_DIRECTORY)
        trades_balance, years = data_processing.get_trade_balance_fig_data(df, selected_country)
        fig = plotly_visuals.get_balance_figure(selected_country, trades_balance, years)

        return fig

    @app.callback(Output('top10_fig', 'figure'),
                  Input('trades_type_options', 'value')
        , prevent_initial_call=True)
    def update_top10_figure(selected_flow):
        df = pd.read_csv(constants.CSV_FILE_DIRECTORY)
        graph_df = data_processing.get_top10_df(df, selected_flow)
        fig = plotly_visuals.get_top10_chart(graph_df, selected_flow)

        return fig
