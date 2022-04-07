from Datasets import artists_df, tracks_df
import pandas as pd

tracks_df['id_artists'] = tracks_df['id_artists'].map(lambda x: str(x[0]))

#bad_artists = artists_df[artists_df.popularity < 30]
#artists_2delete = bad_artists.index.values.tolist()
#new_artists_df = artists_df.drop(artists_2delete, axis=0)
#good_artists = new_artists_df.index.values.tolist()
#artists_df = artists_df.iloc[good_artists]
#artists_df.merge(tracks_df, left_index=True, right_on=['id_artists'], how='left')

artists_df2 = artists_df[artists_df.popularity >= 30]
artists_df_final = artists_df2.merge(tracks_df, left_index=True, right_on=['id_artists'], how='left')
