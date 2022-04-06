import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from Datasets import artists_df, tracks_df

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
 
-- TAB3: TRACKS --
 > info sobre uma música selecionada
"""

################################################ Interactive Components ################################################

tracks_options = [dict(label=name, value=name) for name in tracks_df['name'].unique()]
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

################################################## APP #################################################################

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    #TÍTULO
    html.Div([
        html.H1('METER AQUI O TITULO DO SITE'),
    ], id = '1st row', className='pretty_box'),
    #AQUI COMEÇA O CÓDIGO DAS TABS
    html.Div([
        dcc.Tabs([
            # tab 1
            dcc.Tab(label = 'NOME DA 1ª TAB', children = [
                #aqui fica o código das visualizações
                html.Div([
                    html.Label("Pick a Track"),
                    dropdown_tracks,
                    html.Br(),
                    html.Label("Pick an Artist"),
                    dropdown_artists,
                    html.Br(),
                    html.Label("Pick a Year"),
                    slider_year,
                    html.Br(),
                    html.Label("Explicit?"),
                    explicit_filter
                ], id = "Interaction", style = {'width': '30%'}, className = 'pretty_box'),
            ], style = {
                #aqui ficam as definições de style da tab
            }, selected_style = {
                #aqui ficam as definições de style da tab quando está selected
            }),
            # tab 2
            dcc.Tab(label='NOME DA 2ª TAB', children=[
                # aqui fica o código das visualizações
            ], style={
                # aqui ficam as definições de style da tab
            }, selected_style={
                # aqui ficam as definições de style da tab quando está selected
            }),
            # tab 3
            dcc.Tab(label='NOME DA 3ª TAB', children=[
                # aqui fica o código das visualizações
            ], style={
                # aqui ficam as definições de style da tab
            }, selected_style={
                # aqui ficam as definições de style da tab quando está selected
            })
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)