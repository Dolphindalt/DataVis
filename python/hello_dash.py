# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#452255',
    'text': '#772266'
}

app.layout = html.Div(children=[
    html.H1(
        children='Hello Dash',
        style={
            'text-align': 'left',
            'color': colors['text'],
            'font-size': '200px'
        }
           ),

    html.Div(children='''
        Dash: A web application framework for Python.
    ''', style={
            'font-size': '60px',
            'font-family': 'Arial',
            'color': '#dd9922'
    }),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [5, 4, 5], 'type': 'line', 'name': u'Montreal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization',
                'plot_bgcolor': colors['background']
            }
        },
        style={
            'display': 'block',
            'position': 'absolute',
            'bottom': '0',
            'width': '50%'
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)