# PROJETO
Data Visualization Project @ NOVA IMS
<br>Authors: António Cymbron | Duarte Redinha | Maria João Marques
<br>Lisbon, Portugal | April 2022.

# _Music Searcher_ Visualization Product

This project was made under the evaluation criteria for the course of [`Data Visualization`](https://www.novaims.unl.pt/detalhe-disciplinas?d=200176&c=7512&r=2&o=1), part of the curricular plan of the Master in Data Science and Advanced Analytics, with specialization in Data Science, taught at [NOVA Information Management School](https://www.novaims.unl.pt/default).

### Data Source

The data used is the result of specific data treatment for the purpose in-hands in two .csv files - tracks.csv, and artists.csv. Both can be checked here: [`Spotify Datasets`](https://www.kaggle.com/datasets/lehaknarnauli/spotify-datasets?select=tracks.csv).
This dataset is owned by Lehak Narnauli, and had the contribution of Aditya Kumar.

### Metadata

# `tracks.csv`

|Variable                 |Class     |Description |
|:---|:---|:-----------|
|id                       |character | Song unique ID|
|name                     |character | Song Name|
|popularity               |double    | Song Popularity (0-100), where higher is better|
|duration_ms              |double    | Duration of song in milliseconds|
|explicit                 |integer   | Is the song explicit? (0, if No; 1, otherwise)|
|artists                  |character | Song Artist(s)|
|id_artists               |character | Song Artist(s) unique ID|
|release_date	            |character | Date when the Song was Released|
|danceability             |double    | Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. |
|energy                   |double    | Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. |
|key                      |double    | The estimated overall key of the track. Integers map to pitches using standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1. |
|loudness                 |double    | The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.|
|mode                     |double    | Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.|
|speechiness              |double    | Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks. |
|acousticness             |double    | A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.|
|instrumentalness         |double    | Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0. |
|liveness                 |double    | Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live. |
|valence                  |double    | A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). |
|tempo                    |double    | The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. |
|time_signature           |integer   | An indication of rhythm following a clef, generally expressed as a fraction with the denominator defining the beat as a division of a semibreve and the numerator giving the number of beats in each bar. The values range from 0 to 5. |


# `artists.csv`

|Variable                 |Class     |Description |
|:---|:---|:-----------|
|id                       |character | Artist unique ID|
|followers                |double    | Number of followers|
|genres                   |character | Genres attributed|
|name                     |character | Artist Name|
|popularity               |double    | Artist Popularity (0-100), where higher is better|

Enjoy at https://music-discover-april2022.herokuapp.com/
