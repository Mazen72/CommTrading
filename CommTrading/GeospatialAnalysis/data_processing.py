
def process_map_df(df):
    df_country = df.groupby(['country_or_area'])['commodity'].count()
    df_country = df_country.reset_index()
    df_country.rename(columns={'country_or_area': 'Country/Area', 'commodity': 'Number of Trades'}, inplace=True)
    return df_country