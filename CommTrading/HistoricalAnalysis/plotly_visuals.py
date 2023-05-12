import plotly.graph_objects as go
from dash import dash_table

from CommTrading import constants


def get_top10_chart(graph_df, selected_flow):
    fig = go.Figure()

    fig.add_trace(go.Bar(name=selected_flow, x=graph_df.index, y=graph_df.astype('int64'),
                         marker_color='#0096eb', orientation='v', text=graph_df.astype('int64'),
                         textposition='auto'))

    fig.update_layout(xaxis_title=None, yaxis_title=None,
                      font=dict(size=12, family='Arial', color='black'), hoverlabel=dict(
            font_size=16, font_family="Rockwell"), plot_bgcolor='white',
                      paper_bgcolor='white', barmode='stack', margin=dict(l=0, r=0, t=40, b=40)
                      )
    fig.update_xaxes(showgrid=False, showline=True, zeroline=False, linecolor='black', visible=True)
    fig.update_yaxes(showgrid=False, showline=True, zeroline=False, linecolor='black',
                     visible=True, showticklabels=True)

    fig.update_traces(texttemplate='<b>%{text}</b>')

    return fig


def get_trade_balance_table(new_df):
    trade_balance_table = dash_table.DataTable(
        id='trade_balance_table',
        columns=[
            {"name": i, "id": i} for i in new_df.columns
        ],
        data=new_df.to_dict("records"), filter_action='native',
        editable=False, page_size=6,
        row_deletable=False,
        style_cell=dict(textAlign='center', border='1px solid black'
                        , backgroundColor='white', color='black', fontSize=14, fontWeight=''),
        style_header=dict(backgroundColor='#0f70e0', color='white',
                          fontWeight='bold', border='1px solid black', fontSize=14),
        style_table={'overflowX': 'auto', 'width': '100%', 'min-width': '100%', 'border': '1px solid black'}
    )

    return trade_balance_table


def get_balance_figure(selected_country, trades_balance, years):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=years, y=trades_balance, mode='lines', name=selected_country,
                   marker_color='#0096eb'
                   ))

    if len(years) <= 12:
        dtick_value = 1

    else:
        dtick_value = 2

    fig.update_layout(xaxis_title='Years', yaxis_title='Balance of Trades (usd)',
                      font=dict(size=11, family='Arial', color='black'), hoverlabel=dict(
            font_size=14, font_family="Rockwell",  # font_color='black', bgcolor='white'
        ), plot_bgcolor='white',
                      paper_bgcolor='white',
                      xaxis=dict(
                          dtick=dtick_value,
                          tickwidth=2,  # tickcolor='#80ced6',
                          ticks="outside",
                          tickson="labels",
                          rangeslider_visible=False
                      ), margin=dict(l=0, r=0, t=30, b=0),

                      # yaxis=dict()
                      )
    fig.update_xaxes(showgrid=False, showline=True, zeroline=True, linecolor='black')
    fig.update_yaxes(showgrid=False, showline=True, zeroline=True, linecolor='black')
    return fig


def get_trades_num_figure(df, selected_chart_type):
    selected_type = ''
    if selected_chart_type == 'Area':
        selected_type = 'one'

    fig = go.Figure()
    for flow in df['flow'].unique():
        graph_df = df[df['flow'] == flow]
        fig.add_trace(
            go.Scatter(x=graph_df['year'], y=graph_df['commodity'].astype('int64'), mode='lines', name=flow,
                       marker_color=constants.TRADING_FLOW_COLORS[flow]
                       , stackgroup=selected_type
                       ))

    if len(df['year'].unique().tolist()) <= 12:
        dtick_value = 1

    else:
        dtick_value = 2

    fig.update_layout(  # title = '<b>Number of Trades Over Years<b>', title_x=0.5,
        xaxis_title='Years', yaxis_title='Number of Trades',
        font=dict(size=11, family='Arial', color='black'), hoverlabel=dict(
            font_size=14, font_family="Rockwell",  # font_color='black', bgcolor='white'
        ), plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            dtick=dtick_value,
            tickwidth=2,  # tickcolor='#80ced6',
            ticks="outside",
            tickson="labels",
            rangeslider_visible=False
        ), margin=dict(l=0, r=0, t=30, b=0)
    )
    fig.update_xaxes(showgrid=False, showline=True, zeroline=False, linecolor='black')
    fig.update_yaxes(showgrid=False, showline=True, zeroline=False, linecolor='black')
    return fig
