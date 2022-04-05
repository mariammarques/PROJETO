import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go

###################################################### Data & Treatment ################################################################

tracks_df = pd.read_csv('https://media.githubusercontent.com/media/mariammarques/PROJETO/main/Datasets/tracks.csv')
artists_df = pd.read_csv('https://media.githubusercontent.com/media/mariammarques/PROJETO/main/Datasets/artists.csv')

"""
We are going to:
    #1. remove the [ ] from the 'artists' and the 'id_artists' columns
    #2. extract only the year, from the 'release_date' column
    #3. delete the observations with missing values
"""

tracks_df['artists'] = tracks_df['artists'].map(lambda x: x[2:-2])
tracks_df['artists'] = tracks_df['artists'].map(lambda x: x.replace("'",""))
tracks_df['artists'] = tracks_df['artists'].map(lambda x: x.split(','))

tracks_df['id_artists'] = tracks_df['id_artists'].map(lambda x: x[2:-2])
tracks_df['id_artists'] = tracks_df['id_artists'].map(lambda x: x.replace("'",""))
tracks_df['id_artists'] = tracks_df['id_artists'].map(lambda x: x.split(','))

tracks_df['release_date'] = pd.to_datetime(tracks_df.release_date)
tracks_df['release_year'] = tracks_df.release_date.dt.year
tracks_df.drop(columns=['release_date'], inplace = True)
tracks_df = tracks_df.dropna(subset=['name'])
tracks_df["id"].value_counts()
tracks_df.set_index('id', inplace = True)


artists_df = artists_df.dropna(subset=['followers'])
artists_df.drop(columns=['genres'], inplace = True)
artists_df["id"].value_counts()

artists_df.set_index('id', inplace = True)

"""
Ideias de Gráficos:
-- TRACKS --
 > Nº músicas lançadas por ano
 > Caraterísticas das músicas por Popularidade (teia)
 > Avg(Caraterísticas) por Décadas (teia)
 > Avg(Caraterísticas) por Anos (evolução)
 > Músicas mais populares (cards) -> slicers: ano, artista, caraterística

-- ARTISTS --
 > Artistas por Popularidade -> slicers: ano, artista, caraterística
 > "Track Bio" de um artista selecionado + popularidade atual + nº de followers
 
"""

"""
gas_names = ['CO2_emissions', 'GHG_emissions', 'CH4_emissions', 'N2O_emissions', 'F_Gas_emissions']

sectors = ['energy_emissions', 'industry_emissions',
           'agriculture_emissions', 'waste_emissions',
           'land_use_foresty_emissions', 'bunker_fuels_emissions',
           'electricity_heat_emissions', 'construction_emissions',
           'transports_emissions', 'other_fuels_emissions']

######################################################Interactive Components############################################

country_options = [dict(label=country, value=country) for country in df['country_name'].unique()]

gas_options = [dict(label=gas.replace('_', ' '), value=gas) for gas in gas_names]

sector_options = [dict(label=sector.replace('_', ' '), value=sector) for sector in sectors]


dropdown_country = dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['Portugal'],
        multi=True
    )

dropdown_gas = dcc.Dropdown(
        id='gas_option',
        options=gas_options,
        value='CO2_emissions',
    )

dropdown_sector = dcc.Dropdown(
        id='sector_option',
        options=sector_options,
        value=['energy_emissions', 'waste_emissions'],
        multi=True
    )

slider_year = dcc.Slider(
        id='year_slider',
        min=df['year'].min(),
        max=df['year'].max(),
        marks={str(i): '{}'.format(str(i)) for i in
               [1990, 1995, 2000, 2005, 2010, 2014]},
        value=df['year'].min(),
        step=1
    )

radio_lin_log = dcc.RadioItems(
        id='lin_log',
        options=[dict(label='Linear', value=0), dict(label='log', value=1)],
        value=0
    )

radio_projection = dcc.RadioItems(
        id='projection',
        options=[dict(label='Equirectangular', value=0),
                 dict(label='Orthographic', value=1)],
        value=0
    )


##################################################APP###################################################################

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([
        html.H1('Emissions Dashboard'),
    ], id='1st row', className='pretty_box'),
    html.Div([
        html.Div([
            html.Label('Country Choice'),
            dropdown_country,
            html.Br(),
            html.Label('Gas Choice'),
            dropdown_gas,
            html.Br(),
            html.Label('Sector Choice'),
            dropdown_sector,
            html.Br(),
            html.Label('Year Slider'),
            slider_year,
            html.Br(),
            html.Label('Linear Log'),
            radio_lin_log,
            html.Br(),
            html.Label('Projection'),
            radio_projection,
            html.Br(),
            html.Button('Submit', id='button')
        ], id='Iteraction', style={'width': '30%'}, className='pretty_box'),
        html.Div([
            html.Div([
                html.Label(id='gas_1', className='box_emissions'),
                html.Br(),
                html.Label(id='gas_2', className='box_emissions'),
                html.Br(),
                html.Label(id='gas_3', className='box_emissions'),
                html.Br(),
                html.Label(id='gas_4', className='box_emissions'),
                html.Br(),
                html.Label(id='gas_5', className='box_emissions'),
            ], id='Label', style={'display': 'flex'}),
            html.Div([
                dcc.Graph(id='choropleth'),
            ], id='Map', className='pretty_box')
        ], id='Else', style={'width': '70%'})
    ], id='2nd row', style={'display': 'flex'}),
    html.Div([
        html.Div([
            dcc.Graph(id='bar_graph'),
        ], id='Graph1', style={'width': '50%'}, className='pretty_box'),
        html.Div([
            dcc.Graph(id='aggregate_graph')
        ], id='Graph2', style={'width': '50%'}, className='pretty_box')
    ], id='3th row', style={'display': 'flex'})
])


######################################################Callbacks#########################################################


@app.callback(
    [
        Output("bar_graph", "figure"),
        Output("choropleth", "figure"),
        Output("aggregate_graph", "figure"),
    ],
    [
        Input("button", "n_clicks")
    ],
    [
        State("year_slider", "value"),
        State("country_drop", "value"),
        State("gas_option", "value"),
        State("lin_log", "value"),
        State("projection", "value"),
        State('sector_option', 'value')
    ]
)
def plots(n_clicks, year, countries, gas, scale, projection, sector):
    ############################################First Bar Plot##########################################################
    data_bar = []
    for country in countries:
        df_bar = df.loc[(df['country_name'] == country)]

        x_bar = df_bar['year']
        y_bar = df_bar[gas]

        data_bar.append(dict(type='bar', x=x_bar, y=y_bar, name=country))

    layout_bar = dict(title=dict(text='Emissions from 1990 until 2015'),
                      yaxis=dict(title='Emissions', type=['linear', 'log'][scale]),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )

    #############################################Second Choropleth######################################################

    df_emission_0 = df.loc[df['year'] == year]

    z = np.log(df_emission_0[gas])

    data_choropleth = dict(type='choropleth',
                           locations=df_emission_0['country_name'],
                           # There are three ways to 'merge' your data with the data pre embedded in the map
                           locationmode='country names',
                           z=z,
                           text=df_emission_0['country_name'],
                           colorscale='inferno',
                           colorbar=dict(title=str(gas.replace('_', ' ')) + ' (log scaled)'),

                           hovertemplate='Country: %{text} <br>' + str(gas.replace('_', ' ')) + ': %{z}',
                           name=''
                           )

    layout_choropleth = dict(geo=dict(scope='world',  # default
                                      projection=dict(type=['equirectangular', 'orthographic'][projection]
                                                      ),
                                      # showland=True,   # default = True
                                      landcolor='black',
                                      lakecolor='white',
                                      showocean=True,  # default = False
                                      oceancolor='azure',
                                      bgcolor='#f9f9f9'
                                      ),

                             title=dict(
                                 text='World ' + str(gas.replace('_', ' ')) + ' Choropleth Map on the year ' + str(
                                     year),
                                 x=.5  # Title relative position according to the xaxis, range (0,1)

                             ),
                             paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)'
                             )

    ############################################Third Scatter Plot######################################################

    df_loc = df.loc[df['country_name'].isin(countries)].groupby('year').sum().reset_index()

    data_agg = []

    for place in sector:
        data_agg.append(dict(type='scatter',
                             x=df_loc['year'].unique(),
                             y=df_loc[place],
                             name=place.replace('_', ' '),
                             mode='markers'
                             )
                        )

    layout_agg = dict(title=dict(text='Aggregate CO2 Emissions by Sector'),
                      yaxis=dict(title=['CO2 Emissions', 'CO2 Emissions (log scaled)'][scale],
                                 type=['linear', 'log'][scale]),
                      xaxis=dict(title='Year'),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )

    return go.Figure(data=data_bar, layout=layout_bar), \
           go.Figure(data=data_choropleth, layout=layout_choropleth), \
           go.Figure(data=data_agg, layout=layout_agg)


@app.callback(
    [
        Output("gas_1", "children"),
        Output("gas_2", "children"),
        Output("gas_3", "children"),
        Output("gas_4", "children"),
        Output("gas_5", "children")
    ],
    [
        Input("country_drop", "value"),
        Input("year_slider", "value"),
    ]
)
def indicator(countries, year):
    df_loc = df.loc[df['country_name'].isin(countries)].groupby('year').sum().reset_index()

    value_1 = round(df_loc.loc[df_loc['year'] == year][gas_names[0]].values[0], 2)
    value_2 = round(df_loc.loc[df_loc['year'] == year][gas_names[1]].values[0], 2)
    value_3 = round(df_loc.loc[df_loc['year'] == year][gas_names[2]].values[0], 2)
    value_4 = round(df_loc.loc[df_loc['year'] == year][gas_names[3]].values[0], 2)
    value_5 = round(df_loc.loc[df_loc['year'] == year][gas_names[4]].values[0], 2)

    return str(gas_names[0]).replace('_', ' ') + ': ' + str(value_1), \
           str(gas_names[1]).replace('_', ' ') + ': ' + str(value_2), \
           str(gas_names[2]).replace('_', ' ') + ': ' + str(value_3), \
           str(gas_names[3]).replace('_', ' ') + ': ' + str(value_4), \
           str(gas_names[4]).replace('_', ' ') + ': ' + str(value_5),


if __name__ == '__main__':
    app.run_server(debug=True)
"""