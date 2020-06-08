import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import random

# Dalton Caron
# I used the defaulty data but you may need to change the 
# directory to run it on line 18.

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_excel('../data/hw7data.xls')
mgraph_fake = list(df['Item'].dropna())
mgraph_columns = []
[ mgraph_columns.append([mgraph_fake[i], i]) for i in range(0, len(mgraph_fake))]
mgraph_columns = mgraph_columns[26:49]

app.layout = html.Div([
    html.H1(children='''My Humble Food Board''',
        style={'text-align': 'center', 'color': '#0022DD'}),

    html.Div([

        dcc.Graph(
            id='multigraph',
            style={
                    'rect': {
                        'width': '1px',
                        'color': 'red',
                        'background': 'blue'
                    }
                }
        ),

        html.Div(children='Y Axis Items'),
            
        html.Div([
            dcc.Dropdown(
                id='y_axis1',
                options=[{'label': i[0], 'value': i[1]} for i in mgraph_columns],
                value=mgraph_columns[4][1],
                multi=True
            )
        ],
        style={'width': '48%', 'display': 'inline-block'})
    ]),

    html.Div([

        dcc.Graph(
            id='bivargraph',
            style={
                    'rect': {
                        'width': '1px',
                        'color': 'red',
                        'background': 'blue'
                    }
                }
        ),

        html.Div([
            html.Div(children='X Axis Variable'),
                
            html.Div([
                dcc.Dropdown(
                    id='xvar',
                    options=[{'label': i[0], 'value': i[1]} for i in mgraph_columns],
                    value=mgraph_columns[1][1]
                )
            ],
            style={'width': '70%', 'display': 'block'}),
        ], style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            html.Div(children='Y Axis Variable'),
                
            html.Div([
                dcc.Dropdown(
                    id='yvar',
                    options=[{'label': i[0], 'value': i[1]} for i in mgraph_columns],
                    value=mgraph_columns[4][1]
                )
            ],
            style={'width': '70%', 'display': 'block'}),
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),

    html.Div([

        dcc.Graph(
            id='bargraph',
            style={
                    'rect': {
                        'width': '1px',
                        'color': 'red',
                        'background': 'blue'
                    }
                }
        ),

        dcc.Slider(
            id='yearslider',
            min=2000,
            max=2017,
            marks={i: '{}'.format(i) for i in range(200,2018)},
            value=2000,
        ),

        html.Div(children='Bar Items'),
        
        html.Div([
            dcc.Dropdown(
                id='barsel',
                options=[{'label': i[0], 'value': i[1]} for i in mgraph_columns],
                value=mgraph_columns[4][1],
                multi=True
            )
        ],
        style={'width': '48%', 'display': 'inline-block'})

    ])

])

@app.callback(
    Output('multigraph', 'figure'),
    [
        Input('y_axis1', 'value'),
    ]
)
def update_multigraph(y_axis1):
    x_axis = [i for i in range(2000, 2018)]
    if type(y_axis1) != list:
        y_axis1 = [y_axis1]
    fig = go.Figure()
    fig.update_layout(title="Expenditures Over The Years")
    if y_axis1 != None:
        for index in y_axis1:
            label1 = mgraph_columns[index-26][0].replace("_", " ")
            fig.add_trace(
                go.Scatter(
                    x=x_axis, 
                    y=df.iloc[index, :],
                    mode="lines+markers",
                    name=label1
                )
            )
    return fig

@app.callback(
    Output('bivargraph', 'figure'),
    [
        Input('xvar', 'value'),
        Input('yvar', 'value')
    ]
)
def update_bivargraph(xvar, yvar):
    fig = go.Figure()
    year = [i for i in range(2000, 2018)]
    fig.update_layout(title="Bivariate Data Graph")
    if xvar != None and yvar != None:
        x1 = df.iloc[xvar, :]
        y1 = df.iloc[yvar, :]
        labelx = mgraph_columns[xvar-26][0].replace("_", " ")
        labely = mgraph_columns[yvar-26][0].replace("_", " ")
        fig.add_trace(
            go.Scatter(
                x=x1, 
                y=y1,
                mode="markers",
                text=year,
                name=labelx + " vs " + labely
            )
        )
        fig.update_xaxes(title_text=labelx)
        fig.update_yaxes(title_text=labely)
    return fig

@app.callback(
    Output('bargraph', 'figure'),
    [
        Input('barsel', 'value'),
        Input('yearslider', 'value'),
    ]
)
def update_bargraph(barsel, yearslider):
    year = yearslider
    if barsel != None:
        if type(barsel) != list:
            barsel = [barsel]
        x = []
        y = []
        colors = []
        for index in barsel:
            label1 = mgraph_columns[index-26][0].replace("_", " ")
            x.append(label1)
            y.append(df.iloc[index, :][year])
        fig = go.Figure([go.Bar(x=x, y=y, text=y, textposition='auto')])
        fig.update_layout(title="By Year Expenditures")
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)