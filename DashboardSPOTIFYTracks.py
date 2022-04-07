import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from Datasets import artists_df, tracks_df

################################################## APP #################################################################

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    # Dash app title
    html.Div([
        html.Img(src = '/assets/Spotify_Logo_small.png'),
        html.H1('Music Searcher'),
        html.H3('António Cymbron | Duarte Redinha | Maria João M. Marques'),
        html.H4('Data Vizualization @ NOVA IMS')
    ], id='Website Title', className="title_box"),
    # Tabs Container
    dcc.Tabs(
        id="tabs_container",
        value="geral_view_tab",
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            # First Tab
            dcc.Tab(
                label="Geral View",
                value="geral_view_tab",
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            # Second Tab
            dcc.Tab(
                label="Artist Finder",
                value="artist_finder_tab",
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            # Third Tab
            dcc.Tab(
                label="Music Discover" ,
                value="music_discover_tab",
                className='custom-tab',
                selected_className='custom-tab--selected'
            )
    ]),
    # App content
    html.Div(id='tabs_content_graphs')
])

# Callback to get the selected tab content
@app.callback(
    Output('tabs_content_graphs', 'children'),
    Input('tabs_container', 'value')
)

# Function to render the tab content
def render_content(tab):
    if tab == 'geral_view_tab':
        return html.Div([
            html.Img(src="/assets/tab_geral_tailson.jpeg")
        ])
    elif tab == 'artist_finder_tab':
        return html.Div([
            html.Img(src="/assets/tab_artists_tailson.jpeg")
        ])
    elif tab == 'music_discover_tab':
        return html.Div([
            html.Div([
                html.Img(src="/assets/tab_musics_tailson.jpeg")
            ])
        ])

if __name__ == '__main__':
    app.run_server(debug=True)

########################################################################################################################
"""
Ideias de Gráficos:
-- TAB1: GERAL --
 > Nº músicas lançadas por ano
 > Caraterísticas das músicas por Popularidade (teia)
 > Avg(Caraterísticas) por Décadas (teia)
 > Avg(Caraterísticas) por Anos (evolução)
 > Músicas mais populares (cards) -> slicers: ano, artista, caraterística
 > Artistas por Popularidade -> slicers: ano, artista, caraterística

-- TAB2: ARTISTS --
 > "Track Bio" de um artista selecionado + popularidade atual + nº de followers
 > Comparador de artistas?
 
-- TAB3: TRACKS --
 > info sobre uma música selecionada
"""

########################################### TAB1 Interactive Components ################################################

tracks_options = [dict(label=name, value=name) for name in tracks_df['name_track'].unique()]
dropdown_tracks = dcc.Dropdown(
        id = 'tracks_drop',
        options = tracks_options,
        value=['A Cabritinha'],
        multi=True
    )


artists_options = [dict(label=name, value=name) for name in artists_df['name'].unique()]
dropdown_artists = dcc.Dropdown(
        id = 'artists_option',
        options = artists_options,
        value = ['Quim Barreiros'],
    )


slider_year = dcc.RangeSlider(
        id = 'year_slider',
        min = tracks_df['release_year'].min(),
        max = tracks_df['release_year'].max(),
        marks = {str(i): '{}'.format(str(i)) for i in
               [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2021]},
        value = [tracks_df['release_year'].min(), tracks_df['release_year'].max()],
        tooltip = {"placement": "bottom", "always_visible": True},
        step = 1
    )


explicit_filter = dcc.RadioItems(
        id = 'explicit',
        options = [dict(label = 'No', value = 0),
                 dict(label = 'Yes', value = 1)],
        value=0
    )

########################################### TAB2 Interactive Components ################################################

########################################### TAB3 Interactive Components ################################################