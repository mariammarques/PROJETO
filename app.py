# Importing the necessary packages and data
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import exceptions
import pandas as pd
import plotly.graph_objs as go
from Datasets import tracks_df, artists_df, artists_df_artists_tab, tracks_df_tracks_tab, df_3, df_4
import scipy
from scipy import spatial
from random import randint

############################################### INTERACTIVE COMPONENTS GERAL VIEW ######################################

# Creating the range slider for the year choice
slider_year = dcc.RangeSlider(
    id='year_slider',
    min=tracks_df['release_year'].min(),
    max=tracks_df['release_year'].max(),
    marks={str(i): '{}'.format(str(i)) for i in
           [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2021]},
    value=[1920, tracks_df['release_year'].max()],
    tooltip={"placement": "bottom", "always_visible": True},
    step=1
)

# Getting every year on the dataset, to create a dropdown menu
year_options = [dict(label=year, value=year) for year in tracks_df['release_year'].sort_values().unique()]

# Creating a list of colors with the same length as the different number of years that we have
year_colors = []
for i in range(len(year_options)):
    year_colors.append(
        'rgba(' + str(randint(0, 255)) + ',' + str(randint(0, 255)) + ',' + str(randint(0, 255)) + '0.6)')

# Creating the dropdown to select the years
dropdown_year = dcc.Dropdown(
    id='year_options',
    options=year_options,
    value=[2021, 1965],
    multi=True
)

# Creating the options for a checklist, to choose different music attributes
music_attributes = [dict(label=att, value=att) for att in ['danceability', 'energy', 'speechiness', 'acousticness',
                                                           'instrumentalness', 'liveness', 'valence']]
# Creating the checklist, to choose different music attributes
checklist_music_att = dcc.Checklist(
    id='music_att_check',
    options=music_attributes,
    value=['danceability', 'energy', 'acousticness', 'instrumentalness']
)

# Creating the radio items, to choose the popularity level that we want to see
checklist_popularity = dcc.RadioItems(
    id='popularity_check',
    options=[
        {'label': 'Not Popular', 'value': 1},
        {'label': 'Unpopular', 'value': 2},
        {'label': 'Moderately Popular', 'value': 3},
        {'label': 'Very Popular', 'value': 4},
        {'label': 'Extremely Popular', 'value': 5},
    ],
    value=2
)

# Creating the options for a dropdown with only the 30 most popular artists
top30_artists_options = [dict(label=name, value=''.join(df_4.index[df_4['name'] == name])) for name in
                         df_4['name'].unique()]

# Creating the dropdown with only the 30 most popular artists (default: Eminem)
top30_artists = dcc.Dropdown(
    id='top30_dropdown',
    options=top30_artists_options,
    value='7dGJo4pcD2V6oG8kP0tJRR'
)

############################################# INTERACTIVE COMPONENTS ARTISTS FINDER ####################################

# Get every Artists-ID combination
artists_options_artists_tab1 = []
for index, row in artists_df_artists_tab.iterrows():
    artists_options_artists_tab1.append(dict(label=row['name'], value=index))

# Get every Artists-ID combination V2
artists_options_artists_tab2 = []
for index, row in artists_df_artists_tab.iterrows():
    artists_options_artists_tab2.append(dict(label=row['name'], value=index))

# 1st Dropdown with the artists names and selecting 'Wolfgang Amadeus Mozart' as the default value
dropdown_artists_artists_tab1 = dcc.Dropdown(
    id='artists_dropdown_artists_tab1',
    options=artists_options_artists_tab1,
    value='4NJhFmfw43RLBLjQvxDuRS',
    placeholder='Select the first artist'
)

# 2nd Dropdown with the artists names and selecting 'Harry Styles' as the default value
dropdown_artists_artists_tab2 = dcc.Dropdown(
    id='artists_dropdown_artists_tab2',
    options=artists_options_artists_tab2,
    value='6KImCVD70vtIoJWnq6nGn3',
    placeholder='Select the second artist'
)

# Checklist with the music attributes
music_attributes_options = [dict(label=music_attribute, value=music_attribute) for music_attribute in
                            ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                             'valence']]

checklist_music_attributes_artists_tab = dcc.Checklist(
    id='music_att_checklist_artists_tab',
    options=music_attributes_options,
    value=['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
)

############################################# INTERACTIVE COMPONENTS MUSIC DISCOVER ####################################

# Get every Track-ID combination
tracks_options_tracks_tab = []
for index, row in tracks_df_tracks_tab.iterrows():
    tracks_options_tracks_tab.append(dict(label=row.name_track, value=index))

# Dropdown with the tracks names and selecting 'Come Together' as the default value
dropdown_tracks_tracks_tab = dcc.Dropdown(
    id='tracks_dropdown_tracks_tab',
    options=tracks_options_tracks_tab,
    value='2EqlS6tkEnglzr7tkKAAYD',
    multi=False
)

# List with the track features, to use below
track_features = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness']

################################################## APP #################################################################

# Creating the app
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    # Dash app title
    html.Div([
        html.Img(src='/assets/Spotify_Logo.png'),
        html.H1('Music Searcher')
    ], id='Title row', className='title_box'),
    # Tabs Container
    dcc.Tabs(
        id='tabs_container',
        value='geral_view_tab',
        parent_className='tabs',
        children=[
            # First Tab
            dcc.Tab(
                label='General View',
                value='geral_view_tab',
                className='tab1',
                selected_className='tab1_selected',
                id='first tab'
            ),
            # Second Tab
            dcc.Tab(
                label='Artist Finder',
                value='artist_finder_tab',
                className='tab2',
                selected_className='tab2_selected',
                id='second tab'
            ),
            # Third Tab
            dcc.Tab(
                label='Music Discover',
                value='music_discover_tab',
                className='tab3',
                selected_className='tab3_selected',
                id='third tab'
            )],
        colors={'border': '#1DB954'}
    ),
    # App content
    html.Div(id='tabs_content_graphs'),
    # App footer
    html.Footer([
        html.P(['António Cymbron | Duarte Redinha | Maria João M. Marques', html.Br(),
                'Data Vizualization @ NOVA IMS']),
        html.A('Data Source', title='Go to Kaggle, to find our dataset',
               href='https://www.kaggle.com/datasets/lehaknarnauli/spotify-datasets', target='_blank',
               style={'color': 'white', 'padding-right': '50px'}),
        html.A('Metadata', title='Go to the Github of the project, to learn more about the data',
               href='https://github.com/mariammarques/PROJETO/blob/main/README.md',
               target='_blank', style={'color': 'white'}),
    ], id='footer row', className='footer')
], id='dash app')


################################################## TABS CALLBACK #######################################################

# Callback to get the selected tab content
@app.callback(
    Output('tabs_content_graphs', 'children'),
    Input('tabs_container', 'value')
)
# Function to render the content of the tab
def render_content(tab):
    if tab == 'geral_view_tab':
        return html.Div([
            html.Div([
                html.P(
                    ['Use interactive components to explore and discover how much music has changed over the years!'])
            ], id='geral_tab_header', className='tab_header_title'),
            html.Br(),
            # geral tab 2nd row div --> checklist with the music features
            html.Div([
                html.Label('Select the music features that you want to compare', style={'font-weight': '700'}),
                html.Br(),
                html.Br(),
                checklist_music_att,
                html.P(id='error', style={'color': 'red'})
            ], id='geral_tab_2nd_row', style={'width': '96%'}, className='big_box'),
            # geral tab 3rd row div --> radar chart and line chart
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id='radar_chart')
                    ], id='radar_chart_geral', style={'height': '90%'}),
                    html.Div([
                        dropdown_year
                    ], id='drop_year_geral', style={'height': '5%', 'padding': '0 1% 0 1%'}, className='dropdowns2')
                ], id='music_features_and_year', style={'width': '50%'}, className='big_box'),
                html.Div([
                    dcc.Graph(id='line_attributes'),
                ], id='line_graph', style={'width': '50%'}, className='big_box')
            ], id='geral_tab_3rd_row', style={'display': 'flex'}),
            html.Br(),
            # geral tab 1st row div --> graph bar with number of songs released by year
            html.Div([
                html.Div([
                    dcc.Graph(id='songs_year')
                ], id='Number of Songs By Decade Graph'),
                html.Div([
                    html.Label('Use the range slider to explore the evolutions of music production!',
                               style={'font-family': '"Trebuchet MS", Helvetica, sans-serif', 'color': '#FFFFFF',
                                      'font-size': '20px'}),
                    slider_year
                ], id='range_slide_geral_tab', style={'padding': '0 5% 2% 5%'})
            ], id='geral_tab_1st_row', style={'width': '96%'}, className='big_box'),

            # geral tab 4th row div --> radar chart and infos about the chosen popularity level
            html.Div([
                html.Div([
                    html.Label('Select the popularity level that you want to know more about',
                               style={'font-weight': '700'}),
                    html.Br(),
                    html.Br(),
                    checklist_popularity
                ], id='label_&_popularity_levels', style={'width': '96%'}, className='small_box'),
                html.Br(),
                dcc.Graph(id='radar_popularity'),
                html.Div([
                    html.Label(id='avg_loudness', style={'width': '33%', 'font-variant': 'small-caps'},
                               className='small_box'),
                    html.Label(id='avg_tempo', style={'width': '33%', 'font-variant': 'small-caps'},
                               className='small_box'),
                    html.Label(id='avg_year', style={'width': '33%', 'font-variant': 'small-caps'},
                               className='small_box')
                ], id='popularity_labels_info', style={'display': 'flex', 'padding': ' 0 10%'})
            ], id='geral_tab_4th_row', style={'width': '96%'}, className='big_box'),
            html.Br(),
            # geral tab 5th row div --> chosen artist graphs and infos
            html.Div([
                html.Label('Select the artist, from the Top-30 most popular artists, that you want to know more about',
                           style={'font-weight': '700', 'font-variant': 'small-caps'}),
                html.Div([
                    top30_artists
                ], id='top30_artists_dropdown', className='dropdowns'),
                html.Div([
                    dcc.Graph(id='scatter_plot_geral')
                ], id='songs_by_popularity_artist'),
                html.Label(id='artist_name', style={
                    'font-variant': 'small-caps', 'font-size': '25px', 'font-weight': '700'
                }),
                html.Div([
                    html.Label(id='artist_last_release', style={'width': '25%'}, className='small_box'),
                    html.Label(id='artist_most_pop_song', style={'width': '25%'}, className='small_box'),
                    html.Label(id='artist_avg_duration', style={'width': '25%'}, className='small_box'),
                    html.Label(id='artist_avg_tempo', style={'width': '25%'}, className='small_box')
                ], id='chosen_artist_infos', style={'display': 'flex'})
            ], id='geral_tab_5th_row', style={'width': '96%'}, className='big_box')
        ], id='geral tab content')
    elif tab == 'artist_finder_tab':
        return html.Div([
            html.Div([
                html.P(['Who has the most followers? Who has released more songs? How similar to other artists are the'
                        ' artists that you like?', html.Br(), 'Select 2 artists, and find out all of this, and '
                                                              'much more!'
                        ])
            ], id='artist tab header', className='tab_header_title'),
            # artists 1st row Div --> select an artist dropdowns
            html.Div([
                html.Div([
                    dropdown_artists_artists_tab1
                ], id='1st artist dropdown choice', style={'width': '50%'}, className='dropdowns'),
                html.Div([
                    dropdown_artists_artists_tab2,
                ], id='2nd artist dropdown choice', style={'width': '50%'}, className='dropdowns')
            ], id='artists 1st row', style={'display': 'flex'}),
            # artists 2nd row Div --> artists' labels with information
            html.Div([
                html.Div([
                    html.Label(id='artist1_name', style={
                        'font-variant': 'small-caps', 'font-size': '25px', 'font-weight': '700'
                    }),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Label(id='artist1_n_followers', className='small_box'),
                        html.Label(id='artist1_explicit_number', className='small_box')
                    ]),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Label(id='artist1_not_explicit_number', className='small_box'),
                        html.Label(id='artist1_number', className='small_box')
                    ]),
                    html.Br()
                ], id='1st artist information', style={'width': '50%'}, className='big_box'),
                html.Div([
                    html.Label(id='artist2_name', style={
                        'font-variant': 'small-caps', 'font-size': '25px', 'font-weight': '700'
                    }),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Label(id='artist2_n_followers', className='small_box'),
                        html.Label(id='artist2_explicit_number', className='small_box')
                    ]),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Label(id='artist2_not_explicit_number', className='small_box'),
                        html.Label(id='artist2_number', className='small_box')
                    ]),
                    html.Br(),
                ], id='2nd artist information', style={'width': '50%'}, className='big_box')
            ], id='artists 2nd row', style={'display': 'flex'}),
            # artists 3rd row Div --> artists' popularity gauges
            html.Div([
                html.Div([
                    dcc.Graph(id='artist1_gauge')
                ], id='1st artist popularity gauge', style={'width': '50%'}, className='big_box'),
                html.Div([
                    dcc.Graph(id='artist2_gauge')
                ], id='2nd artist popularity gauge', style={'width': '50%'}, className='big_box')
            ], id='artists 3rd row', style={'display': 'flex'}),
            # artists 4th row Div --> select the music features checklist
            html.Div([
                html.Label('Select the music features that you want to compare', style={'font-weight': '700'}),
                html.Br(),
                html.Br(),
                checklist_music_attributes_artists_tab,
                html.P(id='artists_tab_error', style={'color': 'red'})
            ], id='artists 4th row', style={'width': '96%'}, className='big_box'),
            # artists 5th row Div --> artists' musics features comparison
            html.Div([
                html.Div([
                    dcc.Graph(id='artist1_radar_graph')
                ], id='1st artist features', style={'width': '33%'}, className='big_box'),
                # FALTA MUDAR (PQ TBM FALTA FAZER) A CLASSNAME
                html.Div([
                    dcc.Graph(id='artists_radar_graph')
                ], id='1st and 2nd artist features', style={'width': '33%'}, className='big_box'),
                # FALTA MUDAR (PQ TBM FALTA FAZER) A CLASSNAME
                html.Div([
                    dcc.Graph(id='artist2_radar_graph')
                ], id='2nd artist features', style={'width': '33%'}, className='big_box')
                # FALTA MUDAR (PQ TBM FALTA FAZER) A CLASSNAME
            ], id='artists 5th row', style={'display': 'flex'})
        ], id='artists tab content')
    elif tab == 'music_discover_tab':
        return html.Div([
            html.Div([
                html.P(['Want to know more about your favorite song?', html.Br(),
                        'Is it the right one for dancing? Or is it better for melancholic days? Select your track, '
                        'and find out all about it!'])
            ], id='tracks_tab_header', className='tab_header_title'),
            # tracks 1st row Div --> select a track on the dropdown
            html.Br(),
            html.Div([
                html.Label('Select a Track:', style={'font-family': '"Trebuchet MS", Helvetica, sans-serif',
                                                     'color': '#FFFFFF', 'font-size': '15px'})
            ], id='tracks_dropdown_choice_text', style={'width': '100%', 'text-align': 'center'}),
            html.Div([
                dropdown_tracks_tracks_tab,
            ], id='tracks_dropdown_choice',
                style={'text-align': 'center'}, className='dropdowns'),
            html.Br(),
            # track's cards on the left column
            html.Div([
                html.Div([
                    html.Br(),
                    html.Label('About this Song...', style={'font-variant': 'small-caps', 'font-size': '25px',
                                                            'font-weight': '700'}),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Label(id='track_artist', className='small_box')
                    ]),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Label(id='track_year', className='small_box')
                    ]),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Label(id='track_top_feature', className='small_box')
                    ]),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Label(id='track_explicit', className='small_box')
                    ]),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Label(id='track_duration', className='small_box')
                    ]),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Label(id='track_popularity', className='small_box')
                    ]),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Label(id='track_mode', className='small_box')
                    ]),
                    html.Br(),
                    html.Br()
                ], id='tracks_cards_column', style={'width': '25%'}, className='big_box'),
                html.Div([
                    dcc.Graph(id='tracks_funnel')
                ], id='1st graph', style={'width': '55%'}, className='big_box'),
                html.Div([
                    dcc.Graph(id='most_sim_table')
                ], id='2nd graph', style={'width': '20%'}, className='big_box')
            ], id='tracks_1st_part', style={'display': 'flex'}),
            html.Br(),
            html.Div([
                html.Div([
                    dcc.Graph(id='adv_info')
                ], id='tracks_6_plots', style={'width': '100%'}, className='big_box')
            ], id='tracks_6_plots_box', style={'display': 'flex'})
        ])


################################################## GERAL VIEW ##########################################################

# GRAPH1-DECADES OF MUSIC
@app.callback(
    Output('songs_year', 'figure'),
    [Input('year_slider', 'value')])
def update_graph(year):
    # Data for GRAPH 1 (Decades of music)
    df_1 = tracks_df['release_year'].value_counts()
    df_1 = df_1.to_frame()
    df_1.rename(columns={'release_year': 'number_songs'}, inplace=True)
    df_1['release_year'] = df_1.index
    df_1.reset_index(drop=True, inplace=True)
    df_1.sort_values(by=['release_year'], inplace=True)

    filtered_by_time_df = df_1[(df_1['release_year'] >= year[0]) & (df_1['release_year'] <= year[1])]

    scatter_data = dict(type='bar',
                        y=filtered_by_time_df['number_songs'],
                        x=filtered_by_time_df['release_year'])

    scatter_layout = dict(xaxis=dict(title='Decades'),
                          yaxis=dict(title='Number Of Songs')
                          )

    fig = go.Figure(data=scatter_data, layout=scatter_layout)

    fig.update_traces(marker_color='#4B917D')

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0, 0, 0, 0)',
                      font={'color': '#FCF9F4', 'family': '"Trebuchet MS", Helvetica, sans-serif'},
                      title=dict(text="<b>Number of Songs by Decade</b><br><sup>Find out the decade that had the major"
                                      " and the minor musical productions!</sup>"),
                      title_x=0.5,
                      title_y=0.95
                      )

    return fig


# GRAPH2 - Radar Chart
@app.callback(
    [
        Output('radar_chart', 'figure'),
        Output('error', 'children'),
        Output('line_attributes', 'figure'),
    ],
    [
        Input('year_options', 'value'),
        Input('music_att_check', 'value')
    ]
)
# Defining the function to prevent the update, no year is selected
def show_graphs(year, attributes):
    if year == []:
        raise exceptions.PreventUpdate
    else:
        radar_chart, error, line_attributes = show_graphs_geral(year, attributes)
    return radar_chart, error, line_attributes


# Defining the function to raise an error, if at least 3 attributes are not selected
def show_graphs_geral(year, attributes):
    if len(attributes) < 3:
        return dash.no_update, 'Minimum selection possible is 3 attributes!', dash.no_update
    else:
        radar_chart, line_attributes = update_graphs_geral(year, attributes)
    return radar_chart, '', line_attributes


# Defining the function to update the radar chart and the line graph
def update_graphs_geral(year, attributes):
    # Data for GRAPH 2 (RADAR CHAR)
    attributes.append('release_year')
    df_2 = tracks_df.loc[:, attributes]
    df_2 = df_2.groupby('release_year').mean()
    df_2.sort_values(by=['release_year'], inplace=True)
    df_2_2 = df_2.copy(deep=True)

    # Data for radar chart
    radar_data = []

    for years in year:
        temp_data = dict(release_year=years)
        filtered_by_year_df = df_2.loc[df_2.index == years]
        for column in filtered_by_year_df.columns:
            temp_data[column] = filtered_by_year_df.loc[years, column]

        radar_data.append(temp_data)

    # DataFrame com a data, para o radar é preciso meter a coluna do ano como id para facilitar
    df_radar = pd.DataFrame(radar_data)
    df_radar.index = df_radar['release_year']
    df_radar.drop(columns=['release_year'], inplace=True)

    # Incializar a figure depois de ter o dataset preparado
    fig1 = go.Figure()

    # Arranjar as categorias do radar
    categories = []
    for column in df_radar.columns:
        categories.append(column)

    # Loop para meter para add trace to figure
    # value to access the colors list
    i = 0
    for idx, row in df_radar.iterrows():
        year = idx
        music_char = []
        for element in row:
            music_char.append(element)

        fig1.add_trace(go.Scatterpolar(
            r=music_char,
            theta=categories,
            fill='toself',
            fillcolor=year_colors[i + 1],
            # marker=dict(color='rgb(119,77,19)'),
            name=year
        ))
        i += 1
        fig1.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0.9)',
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    color='#FCF9F4',
                    gridcolor='rgb(179,179,179)'
                ),
                angularaxis=dict(gridcolor='rgb(179,179,179)', color='#FCF9F4'),
                angularaxis_tickfont=dict(size=10)
            ), showlegend=True,
            margin={'b': 30},
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': '#FCF9F4', 'family': '"Trebuchet MS", Helvetica, sans-serif'},
            title={'y': 0.95, 'x': 0.5, 'text': '<b>Which were the strongest features by year?</b>' + '<br>' +
                                                "<sup>Hover your mouse to see more details</sup>"})

    # Line atrributes graph
    # Working with df_2_2
    attribute_data = []
    for att in df_2_2:
        temp_data = dict(
            type='scatter',
            y=df_2_2[att],
            x=df_2_2.index,
            name=att
        )
        attribute_data.append(temp_data)

    scatter_layout = dict(xaxis=dict(title='Year'),
                          yaxis=dict(title='Attributes')
                          )

    fig2 = go.Figure(data=attribute_data, layout=scatter_layout)

    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0, 0, 0, 0.5)',
                       font={'color': '#FCF9F4', 'family': '"Trebuchet MS", Helvetica, sans-serif'},
                       title={'y': 0.95, 'x': 0.5, 'text': '<b>Feature Evolutions by Year</b>' + '<br>' +
                                                           "<sup>Hover your mouse to see more details</sup>"})

    return fig1, fig2


# GRAPH3
@app.callback(
    Output('radar_popularity', 'figure'),
    Output('avg_loudness', 'children'),
    Output('avg_tempo', 'children'),
    Output('avg_year', 'children'),
    [Input('popularity_check', 'value')]
)
def update_radar_pop(popularity):
    # Data for GRAPH 3 (RADAR CHAR) will be df_3
    # Pick the right popularity according to radio check
    popularity_char = df_3.loc[popularity, ['danceability', 'energy', 'speechiness', 'acousticness',
                                            'instrumentalness', 'liveness', 'valence']]

    # Chart ploting
    fig3 = go.Figure(go.Scatterpolar(
        r=popularity_char,
        theta=['danceability', 'energy', 'speechiness', 'acousticness',
               'instrumentalness', 'liveness', 'valence'],
        fill='toself',
        name=popularity
    ))

    fig3.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0.9)',
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                color='#FCF9F4',
                gridcolor='rgb(179,179,179)'
            ),
            angularaxis=dict(gridcolor='rgb(179,179,179)', color='#FCF9F4'),
            angularaxis_tickfont=dict(size=10)
        ), showlegend=False,
        margin={'b': 10},
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#FCF9F4', 'family': '"Trebuchet MS", Helvetica, sans-serif'},
        title={'y': 0.95, 'x': 0.5, 'text': '<b>Which are the features that lead to a "HIT"?</b>' +
                                            "<br><sup>Which are the strongest features by popularity? "
                                            "And the ones that make a song less popular? "
                                            "Use the above radio items and the hover feature to find out!</sup>"})

    # Cards
    avg_loud = round(df_3.loc[popularity, 'loudness'], 2)
    avg_tempo = round(df_3.loc[popularity, 'tempo'])
    avg_year = round(df_3.loc[popularity, 'release_year'])

    return fig3, \
           str('Average loudness: ' + str(avg_loud)), \
           str('Average Tempo: ' + str(avg_tempo)), \
           str('Average Release Year: ' + str(avg_year))


# Artists top 30 info
@app.callback(
    [
        Output('artist_name', 'children'),
        Output('artist_last_release', 'children'),
        Output('artist_most_pop_song', 'children'),
        Output('artist_avg_duration', 'children'),
        Output('artist_avg_tempo', 'children'),
        Output('scatter_plot_geral', 'figure'),
    ],
    [
        Input('top30_dropdown', 'value')
    ]
)
def show_infos(artist_id):
    if artist_id is None:
        raise exceptions.PreventUpdate
    else:
        artist_name, artist_last_release, artist_most_pop_song, artist_avg_duration, artist_avg_tempo, \
        scatter_plot_geral = update_infos(artist_id)
    return artist_name, artist_last_release, artist_most_pop_song, artist_avg_duration, artist_avg_tempo,\
           scatter_plot_geral


def update_infos(artist_id):
    # Get tracks related to artist chosen
    df_4_ = df_4.loc[df_4.index == artist_id, :]
    tracks_of_artist = df_4_.merge(tracks_df, left_index=True, right_on=['id_artists'], how='left')
    tracks_of_artist = tracks_of_artist.iloc[:, 3:]
    # Cards
    release_year_last = tracks_of_artist.loc[(tracks_of_artist['id_artists'] == artist_id), 'release_year'].max()
    most_popular_id = tracks_of_artist['popularity_track'].idxmax()
    most_popular_song = tracks_of_artist.loc[tracks_of_artist.index == most_popular_id]
    avg_duration = tracks_of_artist['duration_ms'].mean()
    avg_duration = convert_time(avg_duration)
    avg_tempo = tracks_of_artist['tempo'].mean()

    # Scatter Plot Geral
    data_scatter = tracks_of_artist[['popularity_track', 'release_year']].groupby('release_year').mean()
    songs_per_year = tracks_of_artist[['name_track', 'release_year']].groupby('release_year').count()
    data_scatter = data_scatter.join(songs_per_year)
    scatter_fig = go.Figure()
    scatter_fig.add_trace(go.Scatter(
        x=data_scatter.index.tolist(),
        y=data_scatter.name_track.tolist(),
        text=data_scatter.popularity_track.tolist(),
        mode='markers',
        marker=dict(color='#EF553B', size=(data_scatter.popularity_track + 10).tolist(), line=dict(color='#F7816D',
                                                                                                   width=3)),
        hovertemplate='<br>Year: %{x}<br>Number of Songs Released: %{y}<br>Average Popularity: %{text}<extra></extra>'
    ))

    scatter_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0, 0, 0, 0.5)',
                              font={'color': '#FCF9F4', 'family': '"Trebuchet MS", Helvetica, sans-serif'},
                              title={'y': 0.95, 'x': 0.5, 'text': '<b>Average Popularity of Songs Released by Year</b>'
                                                                  + "<br><sup>Hover your mouse to see more details"
                                                                    "</sup>"})

    scatter_fig.update_yaxes(title='Nº of Songs Released')
    scatter_fig.update_xaxes(title='Year')

    return str('Informations about ' + str(df_4_['name'][0])), \
           str('Last single released in ' + str(release_year_last)), \
           str('Most Popular song is ' + str(most_popular_song.iloc[:, 0][0]) + ' with a popularity score of '
               + str(most_popular_song.iloc[:, 1][0])), \
           str('Average Song duration of the artist is ' + str(avg_duration) + ' minutes'), \
           str('Average Tempo of the artist is ' + str(round(avg_tempo))), \
           scatter_fig


# func to get number of followers with the desired format
def followers_number(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


# Function to convert milliseconds to minutes and seconds
def convert_time(milsecs):
    milsecs = int(milsecs)
    seconds = (milsecs / 1000) % 60
    seconds = int(seconds)
    minutes = (milsecs / (1000 * 60)) % 60
    minutes = int(minutes)

    return "%d:%d" % (minutes, seconds)


#################################################### ARTISTS FINDER ####################################################

@app.callback(
    [
        Output('artist1_radar_graph', 'figure'),
        Output('artists_radar_graph', 'figure'),
        Output('artist2_radar_graph', 'figure'),
        Output('artists_tab_error', 'children')
    ],
    [
        Input('artists_dropdown_artists_tab1', 'value'),
        Input('artists_dropdown_artists_tab2', 'value'),
        Input('music_att_checklist_artists_tab', 'value')
    ]
)
# Defining the function to prevent the update, if 2 artists are not selected
def show_radars(artist_name1, artist_name2, music_attributes):
    if artist_name1 is None or artist_name2 is None:
        raise exceptions.PreventUpdate
    else:
        artist1_radar_graph, artists_radar_graph, artist2_radar_graph, \
        artists_tab_error = show_radar_graph(artist_name1, artist_name2, music_attributes)
    return artist1_radar_graph, artists_radar_graph, artist2_radar_graph, artists_tab_error


# Defining the function to raise an error, if 3 attributes are not selected
def show_radar_graph(artist_name1, artist_name2, music_attributes):
    if len(music_attributes) < 3:
        return dash.no_update, dash.no_update, dash.no_update, 'Minimum selection possible is 3 attributes!'
    else:
        artist1_radar_graph = update_artist1_radar(artist_name1, music_attributes)
        artists_radar_graph = update_artists_radar(artist_name1, artist_name2, music_attributes)
        artist2_radar_graph = update_artist2_radar(artist_name2, music_attributes)
    return artist1_radar_graph, artists_radar_graph, artist2_radar_graph, ''


# Defining the function to update the radar graph of the first chosen artist vs all artists
def update_artist1_radar(artist_name, music_attributes):
    # Track features, grouped by 'id_artists'
    df_art_radar = tracks_df.loc[:, ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness',
                                     'liveness', 'valence', 'id_artists']]
    df_art_radar = df_art_radar.groupby('id_artists').mean()

    # Filtered dataframe, with only the chosen artist
    chosen_artist_data = df_art_radar.loc[df_art_radar.index == artist_name]

    # Initialize the figure
    radar_figure = go.Figure()

    # Loop to insert the chosen artist data into the figure
    for idx, row in chosen_artist_data.iterrows():
        artist = idx
        chosen_artist_list = []
        for element in row:
            chosen_artist_list.append(element)
        radar_figure.add_trace(go.Scatterpolar(
            r=chosen_artist_list,
            theta=music_attributes,
            fill='toself',
            fillcolor='rgba(29, 185, 84, 0.9)',
            marker=dict(color='rgb(19,119,54)'),
            name=artists_df.loc[artist, 'name']
        ))

    # Loop to insert all the artists' data into the figure
    radar_figure.add_trace(go.Scatterpolar(
        r=df_art_radar.mean().tolist(),
        theta=music_attributes,
        fill='toself',
        fillcolor='rgba(185, 120, 29,0.6)',
        marker=dict(color='rgb(119,77,19)'),
        name='All artists'
    ))

    # Update layout of the radar graph
    radar_figure.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0.9)',
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                color='#FCF9F4',
                gridcolor='rgb(179,179,179)'
            ),
            angularaxis=dict(gridcolor='rgb(179,179,179)', color='#FCF9F4'),
            angularaxis_tickfont=dict(size=10)
        ), showlegend=False,
        margin={'b': 5},
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#FCF9F4'},
        title={'y': 0.95, 'x': 0.5, 'text': '<b>' + str(artists_df.loc[artist, 'name']) + '<br>' +
                                            "vs<br>All Artists</b><br><span style='font-size:0.8em'>Comparison of the "
                                            "average characteristics of their songs<br><span style='font-size:0.6em'>"
                                            "Hover your mouse to see what artist corresponds to each color"}
    )
    return radar_figure


# Defining the function to update the radar graph of the second chosen artist vs all artists
def update_artist2_radar(artist_name, music_attributes):
    # Track features, grouped by 'id_artists'
    df_art_radar = tracks_df.loc[:, ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness',
                                     'liveness', 'valence', 'id_artists']]
    df_art_radar = df_art_radar.groupby('id_artists').mean()

    # Filtered dataframe, with only the chosen artist
    chosen_artist_data = df_art_radar.loc[df_art_radar.index == artist_name]

    # Initialize the figure
    radar_figure = go.Figure()

    # Loop to insert the chosen artist data into the figure
    for idx, row in chosen_artist_data.iterrows():
        artist = idx
        chosen_artist_list = []
        for element in row:
            chosen_artist_list.append(element)
        radar_figure.add_trace(go.Scatterpolar(
            r=chosen_artist_list,
            theta=music_attributes,
            fill='toself',
            fillcolor='rgba(185, 29, 156, 0.9)',
            marker=dict(color='rgb(119,19,100)'),
            name=artists_df.loc[artist, 'name']
        ))

    # Loop to insert all the artists' data into the figure
    radar_figure.add_trace(go.Scatterpolar(
        r=df_art_radar.mean().tolist(),
        theta=music_attributes,
        fill='toself',
        fillcolor='rgba(185, 120, 29,0.6)',
        marker=dict(color='rgb(119,77,19)'),
        name='All artists'
    ))

    # Update layout of the radar graph
    radar_figure.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0.9)',
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                color='#FCF9F4',
                gridcolor='rgb(179,179,179)'
            ),
            angularaxis=dict(gridcolor='rgb(179,179,179)', color='#FCF9F4'),
            angularaxis_tickfont=dict(size=10)
        ), showlegend=False,
        margin={'b': 5},
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#FCF9F4'},
        title={'y': 0.95, 'x': 0.5, 'text': '<b>' + str(artists_df.loc[artist, 'name']) + '<br>' +
                                            "vs<br>All Artists</b><br><span style='font-size:0.8em'>Comparison of the "
                                            "average characteristics of their songs<br><span style='font-size:0.6em'>"
                                            "Hover your mouse to see what artist corresponds to each color"}
    )
    return radar_figure


# Defining the function to update the radar graph of artist1 vs artist2
def update_artists_radar(artist_name1, artist_name2, music_attributes):
    # Track features, grouped by 'id_artists'
    df_art_radar = tracks_df.loc[:, ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness',
                                     'liveness', 'valence', 'id_artists']]
    df_art_radar = df_art_radar.groupby('id_artists').mean()

    # Filtered dataframe, with only the chosen artist
    chosen_artist1_data = df_art_radar.loc[df_art_radar.index == artist_name1]
    chosen_artist2_data = df_art_radar.loc[df_art_radar.index == artist_name2]

    # Initialize the figure
    radar_figure = go.Figure()

    # Loop to insert the chosen artist1 data into the figure
    for idx1, row1 in chosen_artist1_data.iterrows():
        artist1 = idx1
        chosen_artist1_list = []
        for element1 in row1:
            chosen_artist1_list.append(element1)
        radar_figure.add_trace(go.Scatterpolar(
            r=chosen_artist1_list,
            theta=music_attributes,
            fill='toself',
            fillcolor='rgba(29, 185, 84, 0.9)',
            marker=dict(color='rgb(19,119,54)'),
            name=artists_df.loc[artist1, 'name']
        ))

    # Loop to insert the chosen artist2 data into the figure
    for idx2, row2 in chosen_artist2_data.iterrows():
        artist2 = idx2
        chosen_artist2_list = []
        for element2 in row2:
            chosen_artist2_list.append(element2)
        radar_figure.add_trace(go.Scatterpolar(
            r=chosen_artist2_list,
            theta=music_attributes,
            fill='toself',
            fillcolor='rgba(185, 29, 156, 0.6)',
            marker=dict(color='rgb(119,19,100)'),
            name=artists_df.loc[artist2, 'name']
        ))

    # Update layout of the radar graph
    radar_figure.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0.9)',
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                color='#FCF9F4',
                gridcolor='rgb(179,179,179)'
            ),
            angularaxis=dict(gridcolor='rgb(179,179,179)', color='#FCF9F4'),
            angularaxis_tickfont=dict(size=10)
        ), showlegend=False,
        margin={'b': 5},
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#FCF9F4'},
        title={'y': 0.95, 'x': 0.5, 'text': '<b>' + str(artists_df.loc[artist1, 'name']) + '<br>' +
                                            'vs' + '<br>' + str(artists_df.loc[artist2, 'name']) +
                                            "</b><br><span style='font-size:0.8em'>Comparison of the average "
                                            "characteristics of their songs<br><span style='font-size:0.6em'>"
                                            "Hover your mouse to see what artist corresponds to each color"}
    )
    return radar_figure


# Callback with the information about the 2 artists and the popularity gauge graph for both artists
@app.callback(
    [
        Output('artist1_n_followers', 'children'),
        Output('artist1_explicit_number', 'children'),
        Output('artist1_not_explicit_number', 'children'),
        Output('artist1_number', 'children'),
        Output('artist1_gauge', 'figure'),
        Output('artist1_name', 'children'),
        Output('artist2_n_followers', 'children'),
        Output('artist2_explicit_number', 'children'),
        Output('artist2_not_explicit_number', 'children'),
        Output('artist2_number', 'children'),
        Output('artist2_gauge', 'figure'),
        Output('artist2_name', 'children')
    ],
    [
        Input('artists_dropdown_artists_tab1', 'value'),
        Input('artists_dropdown_artists_tab2', 'value')
    ]
)
# Defining the function to prevent the update, if 2 artists are not selected
def show_labels(artist_name1, artist_name2):
    if artist_name1 is None or artist_name2 is None:
        raise exceptions.PreventUpdate
    else:
        artist1_n_followers, artist1_explicit_number, artist1_not_explicit_number, artist1_number, artist1_gauge, \
        artist1_name = update_artists_label(artist_name1)
        artist2_n_followers, artist2_explicit_number, artist2_not_explicit_number, artist2_number, artist2_gauge, \
        artist2_name = update_artists_label(artist_name2)
    return artist1_n_followers, artist1_explicit_number, artist1_not_explicit_number, artist1_number, artist1_gauge, \
           artist1_name, artist2_n_followers, artist2_explicit_number, artist2_not_explicit_number, artist2_number, \
           artist2_gauge, artist2_name


# Defining the function to update the informations about the artist and the popularity gauge graph
def update_artists_label(artist_name):
    # Creating the dataframe with artist_id, followers, popularity, number of songs (total, explicit and non-explicit)
    df_artists_loc = artists_df.loc[:, ['followers', 'popularity']]
    df_artists_total = tracks_df['id_artists'].value_counts().to_frame()
    df_artists_total.rename(columns={'id_artists': 'number of songs'}, inplace=True)
    df_artists_explicit = tracks_df['id_artists'][tracks_df['explicit'] == 1].value_counts().to_frame()
    df_artists_explicit.rename(columns={'id_artists': 'explicit songs'}, inplace=True)
    df_artists_not_explicit = tracks_df['id_artists'][tracks_df['explicit'] == 0].value_counts().to_frame()
    df_artists_not_explicit.rename(columns={'id_artists': 'non explicit songs'}, inplace=True)
    df_artists_label = df_artists_loc.join(df_artists_total)
    df_artists_label = df_artists_label.join(df_artists_explicit)
    df_artists_label['explicit songs'] = df_artists_label['explicit songs'].fillna(0)
    df_artists_label = df_artists_label.join(df_artists_not_explicit)
    df_artists_label['non explicit songs'] = df_artists_label['non explicit songs'].fillna(0)
    df_artists_label

    value_1 = round(df_artists_label.loc[df_artists_label.index == artist_name, 'followers'].tolist()[0])
    value_2 = round(df_artists_label.loc[df_artists_label.index == artist_name, 'explicit songs'].tolist()[0])
    value_3 = round(df_artists_label.loc[df_artists_label.index == artist_name, 'non explicit songs'].tolist()[0])
    value_4 = round(df_artists_label.loc[df_artists_label.index == artist_name, 'number of songs'].tolist()[0])
    value_5 = artists_df.loc[artists_df.index == artist_name, 'name'].tolist()[0]

    gauge_figure = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=df_artists_label.loc[df_artists_label.index == artist_name, 'popularity'].tolist()[0],
        mode='gauge+number+delta',
        delta={'reference': round(df_artists_label['popularity'].mean())},
        gauge={'axis': {'range': [0, 100]},
               'steps': [
                   {'range': [0, 33], 'color': 'lightgray'},
                   {'range': [33, 66], 'color': 'silver'},
                   {'range': [66, 100], 'color': 'darkgray'}]}))

    gauge_figure.update_layout(height=300, margin={'b': 5}, paper_bgcolor='rgba(0,0,0,0)', font={'color': '#FCF9F4'},
                               title={'y': 0.9, 'x': 0.5, 'text': '<b>' + str(value_5) +
                                                                  "'s Popularity</b><br><span style='font-size:0.8em'>"
                                                                  "Measured from 0 to 100, and compared with the "
                                                                  "average popularity"})

    return str('Number of followers: ' + str(value_1)), \
           str('Number of explicit songs: ' + str(value_2)), \
           str('Number of non-explicit songs: ' + str(value_3)), \
           str('Total number of songs: ' + str(value_4)), \
           gauge_figure, str(value_5 + "'s Informations")


################################################## CALLBACKS MUSIC DISCOVER ############################################

# CARDS AT THE LEFT
@app.callback(
    [
        Output("track_artist", "children"),
        Output("track_year", "children"),
        Output("track_top_feature", "children"),
        Output("track_explicit", "children"),
        Output("track_duration", "children"),
        Output("track_popularity", "children"),
        Output("track_mode", "children")
    ],
    [
        Input('tracks_dropdown_tracks_tab', 'value'),
    ]
)
def update_tracks_cards(track_name):
    if track_name is None:
        # PreventUpdate prevents ALL outputs updating
        raise exceptions.PreventUpdate

    value1 = tracks_df.loc[tracks_df.index == track_name, "artists"][0][0]
    value2 = int(tracks_df.loc[tracks_df.index == track_name, "release_year"][0])
    value3 = tracks_df.loc[tracks_df.index == track_name,
                           track_features].transpose().sort_values(by=track_name, ascending=0).index[0].capitalize()
    if tracks_df.loc[tracks_df.index == track_name, "explicit"][0] == 0:
        value4 = 'No'
    else:
        value4 = 'Yes'
    minutes = tracks_df.loc[tracks_df.index == track_name, "duration_ms"][0] / (1000 * 60)
    minutes2 = minutes - (minutes % 1)
    value5 = int(minutes2)
    value6 = int((minutes % 1) * 60)
    value7 = tracks_df.loc[tracks_df.index == track_name, "popularity_track"][0]
    if tracks_df.loc[tracks_df.index == track_name, "mode"][0] == 0:
        value8 = 'No'
    else:
        value8 = 'Yes'

    return str('Artist: ' + str(value1)), \
           str('Release Year: ' + str(value2)), \
           str('Top Feature: ' + str(value3)), \
           str('Explicit?: ' + str(value4)), \
           str('Duration: ' + str(value5) + "min " + str(value6) + "sec"), \
           str('Popularity: ' + str(value7)), \
           str('In a Major Tone?: ' + str(value8))


# CENTERED GRAPH
@app.callback(
    Output('tracks_funnel', 'figure'),
    Input('tracks_dropdown_tracks_tab', 'value')
)
def update_tracks_funnel(track_name):
    if track_name is None:
        # PreventUpdate prevents ALL outputs updating
        raise exceptions.PreventUpdate

    df_tracks_funnel = tracks_df.loc[:, ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness',
                                         'liveness', 'name_track']]

    # Filtered dataframe, with only the chosen artist
    chosen_track = df_tracks_funnel.loc[df_tracks_funnel.index == track_name]

    # Transposing for getting order
    df_funnel_transposed = chosen_track.loc[:, track_features].transpose().sort_values(by=track_name, ascending=0)
    df_funnel_transposed[track_name].values * 100

    # Initialize the figure
    funnel_tracks = go.Figure(
        go.Funnel(
            y=df_funnel_transposed.index.to_list(),
            x=df_funnel_transposed[track_name].values * 100,
            textposition="inside",
            textinfo="label+value",
            opacity=0.65,
            marker={"color": ['rgb(29, 185, 84)', 'rgb(93, 193, 114)', 'rgb(134, 201, 143)', 'rgb(151, 205, 158)',
                              'rgb(185, 211, 187)', 'rgb(217, 217, 217)']},
            connector={"line": {"color": '#FCF9F4', "dash": "dot", "width": 3}},
            hoverinfo='skip'
        )
    )

    funnel_tracks.update_yaxes(showticklabels=False)

    funnel_tracks.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0, 0, 0, 0)',
                                font={'color': '#FCF9F4', 'family': '"Trebuchet MS", Helvetica, sans-serif'},
                                title=dict(text="<b>Track Top Features (%)</b><br>"
                                                "<sup>Find the most relevant features for your selected track."
                                                " Use the zoom feature to have a better look at minor features. "
                                                "<br>Values ranging from 0 to 100, being the last the highest "
                                                "possible value for the respective feature.</sup>"),
                                title_x=0.5,
                                title_y=0.95,
                                autosize=False,
                                width=750,
                                margin={'l': 5, 'r': 5, 'b': 10, 't': 100}
                                )

    return funnel_tracks


# ADVANCED INFO
@app.callback(
    Output("adv_info", "figure"),
    Input('tracks_dropdown_tracks_tab', 'value')
)
def update_tracks_advanced_info(track_name):
    if track_name is None:
        # PreventUpdate prevents ALL outputs updating
        raise exceptions.PreventUpdate

    adv_info = go.Figure()
    adv_info.add_trace(go.Indicator(
        value=int(tracks_df.loc[tracks_df.index == track_name, "tempo"][0]),
        delta={'reference': int(tracks_df.loc[:, "tempo"].mean())},
        gauge={'axis': {'range': [0, int(tracks_df.loc[:, "tempo"].max())]}},
        title={'text': "Tempo (BPM)"},
        domain={'row': 0, 'column': 0}))

    adv_info.add_trace(go.Indicator(
        value=tracks_df.loc[tracks_df.index == track_name, "time_signature"][0],
        delta={'reference': int(tracks_df.loc[:, "time_signature"].mean())},
        gauge={'shape': "bullet",
               'axis': {'range': [0, int(tracks_df.loc[:, "time_signature"].max())]}},
        title={'text': "Time<br>Signature"},
        domain={'x': [0.33, 0.5], 'y': [0.5, 0.75]}))

    adv_info.add_trace(go.Indicator(
        mode="number+delta",
        value=tracks_df.loc[tracks_df.index == track_name, "valence"][0],
        delta={'reference': tracks_df.loc[:, "valence"].mean()},
        title={'text': "Valence"},
        domain={'row': 0, 'column': 2}))

    adv_info.add_trace(go.Indicator(
        mode="delta",
        value=tracks_df.loc[tracks_df.index == track_name, "loudness"][0],
        delta={'reference': int(tracks_df.loc[:, "loudness"].mean())},
        title={'text': "Loudness"},
        domain={'row': 0, 'column': 3}))

    adv_info.update_layout(
        grid={'rows': 1, 'columns': 4, 'pattern': "independent"},
        template={'data': {'indicator': [{
            'mode': "gauge+number+delta"}]}})

    adv_info.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0, 0, 0, 0)',
                           font={'color': '#FCF9F4', 'family': '"Trebuchet MS", Helvetica, sans-serif'},
                           title="<b>Advanced Information</b><br><sup>Find more features' details for your selected "
                                 "track. Indicators are being compared with the respective average (or mode) for all "
                                 "tracks in the database.</sup> ",
                           title_x=0.5,
                           title_y=0.95,
                           autosize=False,
                           height=300,
                           margin={'l': 30, 'r': 5, 'b': 10, 't': 100}
                           )

    return adv_info


# TABLE FOR MOST SIMILAR SONGS
@app.callback(
    Output("most_sim_table", "figure"),
    Input('tracks_dropdown_tracks_tab', 'value')
)
def update_tracks_most_sim_table(track_name):
    if track_name is None:
        # PreventUpdate prevents ALL outputs updating
        raise exceptions.PreventUpdate

    utils_df = tracks_df_tracks_tab.loc[tracks_df_tracks_tab.index == track_name, track_features]
    distance_tracker = scipy.spatial.distance.cdist(tracks_df_tracks_tab.loc[:, track_features], utils_df,
                                                    metric='euclidean')
    get_most_sim_tracks = tracks_df_tracks_tab.loc[:,
                          track_features][distance_tracker
                                          == pd.DataFrame(distance_tracker).nsmallest(4,
                                                                                      columns=[0]).iloc[-3:][0].values]
    if len(get_most_sim_tracks) >= 4:
        get_most_sim_tracks = get_most_sim_tracks[1:]
    get_most_sim_tracks_index = get_most_sim_tracks.index.tolist()
    df_final = tracks_df_tracks_tab.loc[get_most_sim_tracks_index, ["name_track", "artists"]].reset_index(drop=True)
    df_final.index += 1

    colors = ['rgb(29, 185, 84)', 'rgb(134, 201, 143)', 'rgb(201, 214, 202)']
    data = {'Place': df_final.index, 'Color': colors}
    new_df = pd.DataFrame(data)

    most_sim_table = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Place</b>", "Track Name", "Artist"],
            line_color='white', fill_color='white',
            align='center', font=dict(color='black', size=12)
        ),
        cells=dict(
            values=[new_df.Place, df_final.name_track, df_final.artists],
            line_color=[new_df.Color],
            fill_color=[new_df.Color],
            align='center', font=dict(color='black', size=11)
        ))
    ])

    most_sim_table.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0, 0, 0, 0)',
                                 font={'color': '#FCF9F4', 'family': '"Trebuchet MS", Helvetica, sans-serif'},
                                 title="<b>Similar Tracks You Might Like </b><br><sup>Find out other tracks similar "
                                       "to the one selected,<br> based on their features. Table ordered from<br>major"
                                       " to minor track similarity (distance).</sup> ",
                                 title_x=0.5,
                                 title_y=0.95,
                                 autosize=False,
                                 width=300,
                                 margin={'l': 5, 'r': 5, 'b': 10, 't': 150}
                                 )

    return most_sim_table


######################################### END OF THE APP AND RUNNING ###################################################

if __name__ == '__main__':
    app.run_server(debug=True)
