import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def header_with_icon_div(icon_name, header_text, icon_color, icon_size, header_size):
    icon = DashIconify(icon=icon_name, color=icon_color, inline=True,
                       style=dict(fontSize=icon_size, verticalAlign='center'))

    header = html.Div(children=header_text,
                      style=dict(fontWeight='bold',
                                 color='#272727', fontSize=header_size, fontFamily='Circular Std',

                                 ))

    final_div = dmc.Group(children=[icon, header],
                          align='center',
                          spacing=8
                          )

    return final_div


def content_with_icon_div(icon_name, icon_bg_color, title_text, content_data, div_style=None):
    icon = dmc.ThemeIcon(
        size="xl",
        color=icon_bg_color,
        variant="filled",
        style=dict(marginTop=''),
        children=DashIconify(icon=icon_name, inline=True,
                             style=dict(
                                 fontSize='1.5rem',
                             )
                             )

    )

    title = html.Div(
        children=title_text,
        style=dict(
            display='inline-block',
            color='#343434',
            textAlign="left",
            fontWeight=600,
            fontSize='0.75rem',
            paddingLeft="0.6rem",
        ),
    )

    data = html.Div(content_data,
                    style=dict(
                        color='black',
                        display="inline-block",
                        fontFamily='Circular Std',
                        paddingLeft="0.7rem",
                        fontWeight=600,
                        fontSize='1.2rem',
                    ))
    content_div = dmc.Stack(children=[title, data],
                            spacing=0,
                            style=dict(width='')
                            )

    final_div = dmc.Grid(children=[icon, content_div],
                         align="flex-start",
                         justify="flex-start",
                         gutter="xl",
                         style=dict(padding='0.5rem')
                         )

    return final_div
