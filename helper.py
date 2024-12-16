import numpy as np


def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset = ['Team', 'NOC','Games', 'Year', 'City', 'Sport', 'Event','Medal','region'])
    flag =0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == 2016) & (medal_df['region'] == country)]

    if flag ==1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()

    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def madel_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal','region'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally

def country_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return year,country

def data_over_time(df,col):
    nation_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nation_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return nation_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    top_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Name', 'Medal Count']
    merged_df = top_athletes.merge(df, on='Name', how='left')[
        ['Name', 'Medal Count', 'Sport', 'region']].drop_duplicates('Name')

    return merged_df


def year_wise_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_even_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index = 'Sport', values ='Medal', aggfunc = 'count').fillna(0)

    return pt


def most_successful_country(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    top_athletes = temp_df['Name'].value_counts().reset_index().head(10)
    top_athletes.columns = ['Name', 'Medal Count']
    merged_df = top_athletes.merge(df, on='Name', how='left')[['Name', 'Medal Count', 'Sport', ]].drop_duplicates(
        'Name')

    return merged_df


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df





def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final