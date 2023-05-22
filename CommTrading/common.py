import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

button_style = dict(
    fontSize="0.8rem",
    backgroundColor="#0096eb",
    borderColor="grey",
    color="white",
    fontWeight=500,
)

select_all_btn_style = dict(
    fontSize="0.8rem",
    backgroundColor="transparent",
    borderColor="grey",
    color="black",
    fontWeight=500,
    display="inline-block",
)

clear_all_btn_style = dict(
    fontSize="0.8rem",
    backgroundColor="transparent",
    borderColor="grey",
    color="black",
    fontWeight=500,
    display="inline-block",
)

search_font = 'black'
search_font_size = '0.938rem'
search_bg = '#EFEFEF'
search_bg_radius = '1rem'
search_border = '#EFEFEF'
search_width = '100%'
search_font_weight = 500


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


def create_custom_dropdown(
        filter_name,
        filter_options,
        filter_value,
        filter_style,
        filter_id,
        options_id,
        popover_id,
        badge_id,
        icon_id,
        search_input_id,
        no_results_id,
        clear_id="",
        select_all_id="",
        apply_id="",
        select_type="multi"
):
    """
    takes the custom dropdown filter needed parameters and returns a div where the
    custom dropdown exist and then to make it interactive a callback needed same
    as the one called update_materials_dropdown in sc callbacks
        Parameters:
                filter_name: the text will be written on the custom filter (EX: Selected Materials)
                filter_options: list of options either a normal list or {label, value} list of dictionaries
                filter_value: initial value of the filter
                filter_style: the style of the div that the filter inside so that we can have freedom
                              to make it inline to other component or at the center of a row.. etc
                filter_id: the button component id (the outer body of the filter that opens options on click)
                options_id: the checklist or radioitems component id (where it holds the materials labels)
                popover_id: the popover component id (pops up upon clicking and show options)
                badge_id: the badge component id (number of selected options)
                icon_id: the Dash-Iconify icon id (which is whether up or down arrow)
                select_type: in case we want to make same filter but for single select pass 'single'
                search_input_id: id of search input
                no_results_id: id of no search results div
                clear_id: a button to clear all options selected
                select_all_id: a button to select all options available
        Returns:
                html.Div where the new component inside it
    """

    filter_button_icon = html.Div(
        DashIconify(
            icon="bxs:down-arrow",
            inline=True,
        ),
        id=icon_id,
        style=dict(
            display="inline-block",
            fontSize="0.85rem",
            paddingLeft="0.5rem",
            color="#575F6C",
        ),
    )

    filter_filter_text = html.Div(
        children=filter_name,
        style=dict(
            display="inline-block",
            fontSize="1rem",
        ),
    )

    filter_badge = dbc.Badge(
        len(filter_value),
        color="#0096eb",
        text_color="white",
        className="ms-1",
        id=badge_id,
        style=dict(display="", fontSize="0.8rem"),
    )

    filter_filter_content = html.Div(
        children=[filter_filter_text, filter_badge, filter_button_icon],
        style=dict(display="inline-block"),
        className="",
    )

    filter_filter_button = dbc.Button(
        id=filter_id,
        n_clicks=0,
        children=filter_filter_content,
        outline=False,
        size="lg",
        class_name="filter_button",  # increase width
        style=dict(
            backgroundColor="white",
            color="black",
            border="0.1rem solid #0096eb",
        ),
    )

    search_input = dbc.Input(
        id=search_input_id,
        placeholder='Search Here..',
        className='dropdown_search',
        value='',
        debounce=False,
        type='search',
        autoComplete='off',
        style=dict(color=search_font, fontWeight=search_font_weight,
                   textAlign='left',  # borderRadius=ms.search_bg_radius,
                   width='95%', backgroundColor=search_bg,
                   border='0.05rem solid {}'.format(search_border))
    )
    no_result_div = html.Div(
        children='',
        id=no_results_id,
        style=dict(
            fontFamily="Open Sans",
            fontWeight=600,
            color="#656565",
            paddingTop="0.5rem",
            fontSize="0.95rem",
            textAlign='left',
        ),
    )

    if select_type == "single":
        clear_all_icon = DashIconify(
            icon="mdi:clear-outline",
            color="black",
            inline=True,
            style=dict(fontSize="0.8rem", verticalAlign="center"),
        )

        clear_all_text = html.Div(
            children="Clear All",
            style=dict(
                paddingLeft="0.3rem",
                display="inline-block",
                verticalAlign="center",
            ),
        )

        clear_all_btn_content = html.Div([clear_all_icon, clear_all_text])

        clear_all = dbc.Button(
            children=clear_all_btn_content,
            id=clear_id,
            disabled=False,
            class_name="",
            n_clicks=0,
            size="sm",
            style=select_all_btn_style,
        )

        materials_radiolist = dbc.RadioItems(
            options=filter_options,
            value=filter_value,
            label_class_name="options_label",
            id=options_id,
            input_checked_style=dict(backgroundColor="#0096eb"),
            persistence=True,
            persistence_type="session",
            style=dict(overflowY="auto", maxHeight="10rem"),
        )

        filter_popover_content = [search_input, dmc.Space(h=12), materials_radiolist,
                                  no_result_div, html.Hr(), clear_all]

    else:

        select_all_icon = DashIconify(
            icon="fluent:select-all-on-24-regular",
            color="black",
            inline=True,
            style=dict(fontSize="0.8rem", verticalAlign="center"),
        )

        select_all_text = html.Div(
            children="Select All",
            style=dict(
                paddingLeft="0.3rem",
                display="inline-block",
                verticalAlign="center",
            ),
        )

        select_all_btn_content = html.Div([select_all_icon, select_all_text])

        select_all = dbc.Button(
            children=select_all_btn_content,
            id=select_all_id,
            disabled=False,
            class_name="",
            n_clicks=0,
            size="sm",
            style=select_all_btn_style,
        )

        clear_all_icon = DashIconify(
            icon="mdi:clear-outline",
            color="black",
            inline=True,
            style=dict(fontSize="0.8rem", verticalAlign="center"),
        )

        clear_all_text = html.Div(
            children="Clear All",
            style=dict(
                paddingLeft="0.3rem",
                display="inline-block",
                verticalAlign="center",
            ),
        )

        clear_all_btn_content = html.Div([clear_all_icon, clear_all_text])

        clear_all = dbc.Button(
            children=clear_all_btn_content,
            id=clear_id,
            disabled=False,
            class_name="",
            n_clicks=0,
            size="sm",
            style=clear_all_btn_style,
        )

        left_buttons_group = dmc.Group(children=[select_all, clear_all],
                                       position='left',
                                       align='center'
                                       )

        apply_button = dbc.Button(
            children='Apply Filters',
            id=apply_id,
            size='md',
            style=button_style
        )

        lower_buttons_group = dmc.Group(children=[left_buttons_group, apply_button],
                                        position='apart',
                                        align='center'
                                        )

        materials_checklist = dbc.Checklist(
            options=filter_options,
            value=filter_value,
            label_class_name="options_label",
            id=options_id,
            input_checked_style=dict(backgroundColor="#0096eb"),
            persistence=True,
            persistence_type="session",
            style=dict(overflowY="auto", maxHeight="10rem", paddingLeft="0.3rem",
                       ),
        )

        materials_checklist = dbc.Spinner([materials_checklist],
                                          size="md", color="primary", type="border",
                                          fullscreen=False)

        filter_popover_content = [search_input, dmc.Space(h=12), materials_checklist,
                                  no_result_div, html.Hr(), lower_buttons_group]

    filter_pop_over = dbc.Popover(
        children=filter_popover_content,
        body=True,
        offset=0.7,
        target=filter_id,
        class_name="pop_up",
        hide_arrow=True,
        trigger="legacy",
        placement="bottom-start",
        id=popover_id,
        is_open=False,
        style=dict(width="30rem", maxWidth="50%"),
    )

    filter_div = html.Div([filter_filter_button, filter_pop_over], style=filter_style)

    return filter_div
