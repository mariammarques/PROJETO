from Datasets import artists_df, tracks_df
import pandas as pd

bad_artists = artists_df[artists_df.popularity < 30]

artists_2delete = bad_artists.index.values.tolist()

new_artists_df = artists_df.drop(artists_2delete, axis=0)

good_artists = new_artists_df.index.values.tolist()

