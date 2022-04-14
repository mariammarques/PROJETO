# Importing the necessary packages
import pandas as pd

############################################ Data Importing & Data Treatment ###########################################

# Importing the data
tracks_df = pd.read_csv('https://media.githubusercontent.com/media/mariammarques/PROJETO/main/Datasets/tracks.csv')
artists_df = pd.read_csv('https://media.githubusercontent.com/media/mariammarques/PROJETO/main/Datasets/artists.csv')

# Importing the data
#tracks_df = pd.read_csv('C:/Users/maria/Desktop/tracks_30.csv')
#artists_df = pd.read_csv('C:/Users/maria/Desktop/artists_30.csv')

# Removing the [' '] from the 'artists' column
tracks_df['artists'] = tracks_df['artists'].map(lambda x: x[2:-2])
tracks_df['artists'] = tracks_df['artists'].map(lambda x: x.replace("'", ""))
tracks_df['artists'] = tracks_df['artists'].map(lambda x: x.split(','))

# Removing the [' '] from the 'id_artists' column
tracks_df['id_artists'] = tracks_df['id_artists'].map(lambda x: x[2:-2])
tracks_df['id_artists'] = tracks_df['id_artists'].map(lambda x: x.replace("'", ""))
tracks_df['id_artists'] = tracks_df['id_artists'].map(lambda x: x.split(','))

# Extracting the year from the 'release_date' column, creating a new column 'release_year', and dropping the first one
tracks_df['release_date'] = pd.to_datetime(tracks_df.release_date)
tracks_df['release_year'] = tracks_df.release_date.dt.year
tracks_df.drop(columns=['release_date'], inplace=True)

# Deleting the observations with missing values and re-setting the index
tracks_df = tracks_df.dropna(subset=['name'])
tracks_df.set_index('id', inplace=True)

# Deleting the observations with missing values, dropping the column 'genres', and re-setting the index
artists_df = artists_df.dropna(subset=['followers'])
artists_df.drop(columns=['genres'], inplace=True)
artists_df.set_index('id', inplace=True)

# Reducing the dataset to have only the artists with popularity >=30
tracks_df['id_artists'] = tracks_df['id_artists'].map(lambda x: str(x[0]))
#artists_df = artists_df[artists_df.popularity >= 30]
tracks_df = artists_df.merge(tracks_df, left_index=True, right_on=['id_artists'], how='left')
tracks_df = tracks_df.dropna()
tracks_df = tracks_df.iloc[:, 3:]
tracks_df = tracks_df.rename(columns={"name_y": "name_track", "popularity_y": "popularity_track"})

# Creating a new dataframe with only the most popular artists, to reduce waiting time
artists_df_artists_tab = artists_df[artists_df.popularity >= 70]
artists_df_artists_tab = artists_df_artists_tab.merge(tracks_df, left_index = True, right_on=['id_artists'], how='left')
artists_df_artists_tab.dropna(inplace=True)
artists_df_artists_tab = artists_df_artists_tab.loc[:, ["followers", "name", "popularity", "id_artists"]]
artists_df_artists_tab = artists_df_artists_tab.drop_duplicates('id_artists')
artists_df_artists_tab.set_index('id_artists', drop=True, inplace=True)

# Creating a new dataframe with only the most popular tracks, to reduce waiting time
tracks_df_tracks_tab = tracks_df[tracks_df.popularity_track >= 75]

# GERAL TAB DATAFRAMES
# Data for GRAPH 3 (RADAR CHART)
df_3 = tracks_df.copy(deep=True)
df_3.sort_values(by='popularity_track', inplace=True, ascending=False)

# Create a function to "label" the popularity, so we don't unnecessary groups
def popularity_group(pop_value):
    if pop_value <= 10:
        pop_value = 1
    elif pop_value <= 25:
        pop_value = 2
    elif pop_value <= 50:  # Basically, depending on the value of song's popularity
        pop_value = 3  # They will be attributed a new value ranging from 1 to 5
    elif pop_value <= 75:
        pop_value = 4
    elif pop_value <= 100:
        pop_value = 5
    return pop_value

# Changing the popularity value to a new one
df_3['popularity_track'] = df_3['popularity_track'].map(lambda x: popularity_group(x))
df_3 = df_3.groupby('popularity_track').mean()

# Data for GRAPH 4 (Top 30 artists)
df_4 = artists_df.sort_values(by='popularity', ascending=False)
df_4 = df_4[:30]