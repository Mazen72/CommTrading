import plotly.graph_objects as go
from dash import dcc


def get_map_figure(df_country):
    fig = go.Figure()
    fig.add_trace(go.Choropleth(
        locations=df_country['Country/Area'],
        locationmode='country names',
        colorscale="Viridis",
        z=df_country['Number of Trades'],

        colorbar=dict(len=0.8, yanchor='middle', y=-0.1, thickness=15, x=0.5,
                      ticklen=3, orientation='h',
                      title=dict(font=dict(size=12, color='black'), side='bottom',
                                 text='Number of Trades'),
                      ),
    ))

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0, autoexpand=True), autosize=False,
                      font=dict(color='black', size=10),
                      legend=dict(yanchor="bottom", y=0.5),
                      width=1024, height=580
                      )

    fig.update_geos(fitbounds=False, visible=True,  # projection=dict(type='boggs')
                    )

    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig


def get_map_pie(dff):
    pie = go.Figure(
        data=go.Pie(labels=dff.index, values=dff,  # hole=.3,
                    showlegend=False, sort=False))

    pie.update_traces(hoverinfo='none', textinfo='label+percent', textfont_size=10, textfont_family='Arial',
                      marker=dict(colors=['#1500FF', '#FF8C00', '#3B98F5', '#F5D700'],
                                  line=dict(color='black')),
                      texttemplate='<b>%{label}</br></br>%{percent}</b>')

    pie.update_layout(
        font=dict(size=10, family='Arial', color='black')
        , hoverlabel=dict(font_size=10, font_family="Rockwell")
        , plot_bgcolor='white',
        paper_bgcolor='white', margin=dict(l=0, r=0, t=10, b=0),
    )

    pie_div = dcc.Graph(id='pie', config={'displayModeBar': False, 'displaylogo': False},
                        style=dict(height='22vh', backgroundColor='white', width='22vh'), figure=pie
                        )

    return pie_div
