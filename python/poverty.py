import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

data_path = "../data/PovertyEstimatesCounties.xls"

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

pdf = pd.read_excel("https://katie.mtech.edu/classes/csci444/notebooks/data/PovertyEstimatesCounties.xls", sheet_name="Poverty Data 2016", skiprows=range(3))
pdf = pdf[pdf['FIPStxt']%1000 != 0]
states = pdf['State'].unique()
columns = list(pdf)

#Using our Poverty Estimate spreadsheet with Plotly Express
import numpy as np
import pandas as pd

df2 = pd.read_excel("https://katie.mtech.edu/classes/csci444/notebooks/data/PovertyEstimatesCounties.xls", 
                   sheet_name="Poverty Data 2016", skiprows=range(3),dtype={"FIPStxt": str})
   
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import plotly.express as px

fig = px.choropleth(df2, geojson=counties, locations='FIPStxt', color='PCTPOVALL_2016',
                           color_continuous_scale="YlOrRd",
                           range_color=(0, 50),
                           scope="usa",
                           labels={'PCTPOVALL_2016':'Percent'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

DEFAULT_OPACITY = 0.8

app.layout = html.Div([
    html.Div([
    
        html.H1(children='Poverty Time'),
    
        html.Div(children='Select State'),
    
        html.Div([
            dcc.Dropdown(
                id='state',
                options=[{'label': i, 'value': i} for i in states],
                value='AZ'
            )
        ],
        style={'width': '48%', 'display': 'block'}),
        
        html.Div(children='X Axis'),
        
        html.Div([
            dcc.Dropdown(
                id='x_axis',
                options=[{'label': i, 'value': i} for i in columns],
                value=columns[7]
            )
        ],
        style={'width': '48%', 'display': 'block'}),
        
        html.Div(children='Y Axis'),
        
        html.Div([
            dcc.Dropdown(
                id='y_axis',
                options=[{'label': i, 'value': i} for i in columns],
                value=columns[10]
            )
        ],
        style={'width': '48%', 'display': 'block'}),
        
        dcc.Graph(id='pov-graph')
    
    ]),

    html.Div([

        html.P('Map transparency:',
            style={
                'display':'inline-block',
                'verticalAlign': 'top',
                'marginRight': '10px'
            }
        ),

        html.Div([
            dcc.Slider(
                id='opacity-slider',
                min=0, max=1, value=DEFAULT_OPACITY, step=0.1,
                marks={tick: str(tick)[0:3] for tick in np.linspace(0,1,11)},
            ),
        ], style={'width':300, 'display':'inline-block', 'marginBottom':10}),

        dcc.Graph(
                id = 'county-choropleth',
                figure = fig
            ),
    ])
])

@app.callback(
    Output('pov-graph', 'figure'),
    [
        Input('state', 'value'),
        Input('x_axis', 'value'),
        Input('y_axis', 'value')
    ]
)

def update_graph(state, x_axis, y_axis):
    spdf = pdf[pdf['State'] == state]
    return {
        'data': [dict(
            x=spdf[x_axis],
            y=spdf[y_axis],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.7,
                'line': { 'width': 0.5, 'color': 'white' }
            }
        )],
        'layout': dict(
            xaxis={
                'title': x_axis,
                'type': 'linear'
            },
            yaxis={
                'title': y_axis,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)