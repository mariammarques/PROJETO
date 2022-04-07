import pandas as pd

############################################ Data & Treatment ##########################################################

#tracks_df = pd.read_csv('https://media.githubusercontent.com/media/mariammarques/PROJETO/main/Datasets/tracks.csv')
#artists_df = pd.read_csv('https://media.githubusercontent.com/media/mariammarques/PROJETO/main/Datasets/artists.csv')

tracks_df = pd.read_csv('Datasets/tracks.csv')
artists_df = pd.read_csv('Datasets/artists.csv')

"""
We are going to:
    #1. remove the [ ] from the 'artists' and the 'id_artists' columns
    #2. extract only the year, from the 'release_date' column
    #3. delete the observations with missing values
"""

tracks_df['artists'] = tracks_df['artists'].map(lambda x: x[2:-2])
tracks_df['artists'] = tracks_df['artists'].map(lambda x: x.replace("'", ""))
tracks_df['artists'] = tracks_df['artists'].map(lambda x: x.split(','))

tracks_df['id_artists'] = tracks_df['id_artists'].map(lambda x: x[2:-2])
tracks_df['id_artists'] = tracks_df['id_artists'].map(lambda x: x.replace("'", ""))
tracks_df['id_artists'] = tracks_df['id_artists'].map(lambda x: x.split(','))

tracks_df['release_date'] = pd.to_datetime(tracks_df.release_date)
tracks_df['release_year'] = tracks_df.release_date.dt.year
tracks_df.drop(columns=['release_date'], inplace=True)
tracks_df = tracks_df.dropna(subset=['name'])
tracks_df.set_index('id', inplace=True)


artists_df = artists_df.dropna(subset=['followers'])
artists_df.drop(columns=['genres'], inplace=True)
artists_df["id"].value_counts()

artists_df.set_index('id', inplace=True)

# Reducing the dataset to have only the artists with popularity >=30
tracks_df['id_artists'] = tracks_df['id_artists'].map(lambda x: str(x[0]))
artists_df = artists_df[artists_df.popularity >= 30]
tracks_df = artists_df.merge(tracks_df, left_index=True, right_on=['id_artists'], how='left')
tracks_df = tracks_df.dropna()
tracks_df = tracks_df.iloc[:, 3:]
tracks_df = tracks_df.rename(columns={"name_y": "name_track", "popularity_y": "popularity_track"})
