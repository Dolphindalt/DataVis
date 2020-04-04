import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_excel('../data/hw7data.xls')
mgraph_fake = list(df['Item'].dropna())
mgraph_columns = []
[ mgraph_columns.append((mgraph_fake[i], i)) for i in range(0, len(mgraph_fake))]

app.layout = html.Div([

    html.Div(children='Y Axis'),
        
    html.Div([
        dcc.Dropdown(
            id='y_axis',
            options=[{'label': i[0], 'value': i[1]} for i in mgraph_columns],
            value=mgraph_columns[1][1]
        )
    ],
    style={'width': '48%', 'display': 'block'}),

    dcc.Graph(
        id='multigraph',
        style={
                'rect': {
                    'width': '1px',
                    'color': 'red',
                    'background': 'blue'
                }
            }
    )
])

@app.callback(
    Output('multigraph', 'figure'),
    [
        Input('y_axis', 'value')
    ]
)

def update_multigraph(y_axis):
    print(y_axis)
    label = mgraph_columns[y_axis][0]
    print(label)
    return {
        'data': [
            dict(
                x=[i for i in range(2000, 2018)],
                y=df.iloc[y_axis, :],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name="something"
            )
        ],
        'layout': dict(
            xaxis={'title': 'Year'},
            yaxis={'title': label.replace("_", " ")},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)