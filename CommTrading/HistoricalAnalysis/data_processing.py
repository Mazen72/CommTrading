import pandas as pd

from CommTrading import constants


def get_top10_df(df, selected_flow):
    df = df[df['flow'] == selected_flow]
    graph_df = df.groupby('country_or_area', sort=False)['commodity'].count()
    graph_df = graph_df.nlargest(10)
    return graph_df


def get_trade_balance_table_df(df):
    df = df.groupby(['country_or_area', 'year', 'flow'])['trade_usd'].sum()
    df = df.reset_index()

    countries = []
    years_ = []
    trades_balance = []
    for country in df['country_or_area'].unique().tolist():
        filtered_country_df = df[df['country_or_area'] == country]
        years = filtered_country_df['year'].unique().tolist()

        for year in years:
            filtered_year_df = filtered_country_df[filtered_country_df['year'] == year]

            exports_df = filtered_year_df[filtered_year_df['flow'] == 'Export']
            if exports_df.empty:
                exports = 0
            else:
                exports = exports_df['trade_usd'].values[0]

            imports_df = filtered_year_df[filtered_year_df['flow'] == 'Import']
            if imports_df.empty:
                imports = 0
            else:
                imports = imports_df['trade_usd'].values[0]

            re_exports_df = filtered_year_df[filtered_year_df['flow'] == 'Re-Export']
            if re_exports_df.empty:
                re_exports = 0
            else:
                re_exports = re_exports_df['trade_usd'].values[0]

            re_imports_df = filtered_year_df[filtered_year_df['flow'] == 'Re-Import']
            if re_imports_df.empty:
                re_imports = 0
            else:
                re_imports = re_imports_df['trade_usd'].values[0]

            trade_balance = (exports + re_exports) - (imports + re_imports)
            trades_balance.append(round(trade_balance, 2))
            years_.append(year)
            countries.append(country)

    new_df = pd.DataFrame()
    new_df['Country or Area'] = countries
    new_df['Year'] = years_
    new_df['Balance of Trade (usd)'] = trades_balance

    return new_df


def get_trade_balance_fig_data(df, selected_country):
    # filtering by country
    df = df[df['country_or_area'] == selected_country]

    # grouping by year and flow
    df = df.groupby(['year', 'flow'])['trade_usd'].sum()
    df = df.reset_index()
    # getting years list
    years = df['year'].unique().tolist()

    # looping through all years to get balance of trades ( Total Exports - Total Imports )
    trades_balance = []
    # looping through years
    for year in years:
        # getting sum of exports of that year
        filtered_df = df[df['year'] == year]

        exports_df = filtered_df[filtered_df['flow'] == 'Export']
        if exports_df.empty:
            exports = 0
        else:
            exports = exports_df['trade_usd'].values[0]

        # getting sum of imports of that year
        imports_df = filtered_df[filtered_df['flow'] == 'Import']
        if imports_df.empty:
            imports = 0
        else:
            imports = imports_df['trade_usd'].values[0]

        # getting sum of re-exports of that year
        re_exports_df = filtered_df[filtered_df['flow'] == 'Re-Export']
        if re_exports_df.empty:
            re_exports = 0
        else:
            re_exports = re_exports_df['trade_usd'].values[0]

        # getting sum of re-imports of that year
        re_imports_df = filtered_df[filtered_df['flow'] == 'Re-Import']
        if re_imports_df.empty:
            re_imports = 0
        else:
            re_imports = re_imports_df['trade_usd'].values[0]

        # getting balance of trade
        trade_balance = (exports + re_exports) - (imports + re_imports)
        # appending to the list
        trades_balance.append(round(trade_balance, 2))

    return trades_balance, years


def get_trades_num_figure_df(df, selected_country, selected_category):
    # a dictionery with the flows types colors
    flow_colors = constants.TRADING_FLOW_COLORS
    # filtering by country
    df = df[df['country_or_area'] == selected_country]
    # filtering by category in case All Categories not chosen
    if selected_category != 'All Categories':
        df = df[df['category'] == selected_category]

    # grouping by year and flow
    df = df.groupby(['year', 'flow'])['commodity'].count()
    df = df.reset_index()

    return df
