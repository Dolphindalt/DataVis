import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

data_path = "../data/PovertyEstimatesCounties.xls"

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

pdf = pd.read_excel("https://katie.mtech.edu/classes/csci444/notebooks/data/PovertyEstimatesCounties.xls", sheet_name="Poverty Data 2016", skiprows=range(3))
pdf = pdf[pdf['FIPStxt']%1000 != 0]
states = pdf['State'].unique()
columns = list(pdf)

app.layout = html.Div([
    html.Div([
    
        html.Div([
            dcc.Dropdown(
                id='state',
                options=[{'label': i, 'value': i} for i in states],
                value='AZ'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='x_axis',
                options=[{'label': i, 'value': i} for i in columns],
                value=columns[7]
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='y_axis',
                options=[{'label': i, 'value': i} for i in columns],
                value=columns[10]
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        
        dcc.Graph(id='pov-graph')
    
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
    return {
        'data': [dict(
            x=pdf[x_axis],
            y=pdf[y_axis],
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