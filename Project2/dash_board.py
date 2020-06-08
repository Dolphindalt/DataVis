import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import random
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

external_stylesheets = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'
    ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

value_range = [2008, 2019]

brewing_materials = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-31/brewing_materials.csv')
beer_taxed = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-31/beer_taxed.csv')
brewer_size = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-31/brewer_size.csv')
beer_states = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-31/beer_states.csv')

# add categorical factors
brewing_materials['type'] = brewing_materials['type'].astype('category')
brewing_materials['data_type'] = brewing_materials['data_type'].astype('category')
brewing_materials['material_type'] = brewing_materials['material_type'].astype('category')
beer_taxed['type'] = beer_taxed['type'].astype('category')
beer_taxed['data_type'] = beer_taxed['data_type'].astype('category')
beer_taxed['tax_status'] = beer_taxed['tax_status'].astype('category')
brewer_size['brewer_size'] = brewer_size['brewer_size'].astype('category')
beer_states['type'] = beer_states['type'].astype('category')
beer_states['state'] = beer_states['state'].astype('category')

# Remove the total category from beer_states
beer_states = beer_states.drop(beer_states.loc[beer_states['state'] == 'total'].index)
beer_states['state'] = beer_states['state'].cat.remove_categories(['total'])

# Remove the total category from brewer_size
brewer_size = brewer_size.drop(brewer_size.loc[brewer_size['brewer_size'] == 'Total'].index)
brewer_size['brewer_size'] = brewer_size['brewer_size'].cat.remove_categories(['Total'])

# Add log of barrels for beer states
beer_states['log_barrels'] = np.log(beer_states['barrels'] + 1)
 
# Log all barrel variables in brewer_size
brewer_size['Log Total Barrels'] = np.log(brewer_size['total_barrels'] + 1)
brewer_size['Log Taxable Removals'] = np.log(brewer_size['taxable_removals'] + 1)
brewer_size['Log Total Shipped'] = np.log(brewer_size['total_shipped'] + 1)

# Make labels look nicer
brewer_size['Total Barrels'] = brewer_size['total_barrels']
brewer_size['Taxable Removals'] = brewer_size['taxable_removals']
brewer_size['Total Shipped'] = brewer_size['total_shipped']
brewer_size['Number of Brewers'] = brewer_size['n_of_brewers']

# Year but as a string
brewer_size['Years'] = brewer_size['year'].astype(str)

# Brewing Materials
# Combine Year and Month into single Date field
brewing_materials['Date'] = pd.to_datetime(brewing_materials[['year', 'month']].assign(DAY=1))

# Beer Taxed
# Combine Year and Month into single Date field
beer_taxed['Date'] = pd.to_datetime(beer_taxed[['year', 'month']].assign(DAY=1))
beer_taxed['Year Current'] = beer_taxed['ytd_current']
beer_taxed['Month Current'] = beer_taxed['month_current']

# Tidy up labels
brewing_materials['Type'] = brewing_materials['type']
brewing_materials['Month Current'] = brewing_materials['month_current']
brewing_materials['Material Type'] = brewing_materials['material_type']
brewing_materials['Year Current'] = brewing_materials['ytd_current']

# precompute all choropleth maps so it loads fast during the presentation
choropleth_list = []
for i in range(value_range[0], value_range[1]+1):
    by_state = beer_states[beer_states['year'] == i]
    fig = go.Figure(
        data = go.Choropleth(
            locations = by_state['state'],
            z = by_state['log_barrels'],
            locationmode = 'USA-states',
            colorscale = 'Reds',
            colorbar_title = 'Barrels'
        )
    )

    fig.update_layout(
        title_text = 'Natural Log of Barrels Produced by State',
        geo_scope='usa', # limite map scope to USA
    )

    choropleth_list.append(fig)

app.layout = html.Div([

    # A glorious title to blow them all away.
    html.Div(
        html.H1(
            children='''Brewing in the USA''',
            className="bg-primary text-light mb-0 text-center rounded-left",
            style={"overflow" : "hidden"}
            ),
        className="p-3 bg-dark"), # End Div
    # End of the title

    # Primary navbar to sit at the top of the page
    html.Nav([

        dcc.Location(id='url', refresh=False),

        html.Div([

            html.Ul([  

                html.Li([
                    dcc.Link("About", href="/", className="nav-link")
                ], className="nav-item"),

                html.Li([
                    dcc.Link("State Totals", href="/states", className="nav-link")
                ], className="nav-item"),

                html.Li([
                    dcc.Link("Brewer Size", href="/size", className="nav-link")
                ], className="nav-item"),

                html.Li([
                    dcc.Link("Brewing Materials", href="/materials", className="nav-link")
                ], className="nav-item"),

                html.Li([
                    dcc.Link("Taxes ☹️", href="/taxes", className="nav-link")
                ], className="nav-item")

            ], className="navbar-nav") # End Ul

        ], className="justify-content-between navbar-collapse collapse") # End Div

    ], className="navbar navbar-expand-sm bg-dark navbar-dark"), # End Nav
    # End of the primary navbar

    # Render everything here :)
    html.Div(
        html.Div(
            html.Div(id='page-content', className="col-sm"),
            style={"grid-area":"main"},
            className="row"
        ),
        className="container mt-4"
    )

])

# Page routing callback and functions.
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/":
        return home_layout
    elif pathname == "/states":
        return states_layout
    elif pathname == "/size":
        return brewer_size_layout
    elif pathname == "/materials":
        return brewing_materials_layout
    elif pathname == "/taxes":
        return taxes_layout
    else:
        return not_found_layout

home_layout = html.Div([
        html.H3('Welcome', className="text-center mb-5"),
        html.P('In this epic display, you will observe \
            data on beer production from the Alcohol and Tobacco Tax and Trade Bureau.', className="mt-2 mb-2"),

        html.P('The data is comprised of three main artifacts:'),

        html.Ul([
            html.Li([html.P("State-level beer production by year (2008-2019)")]),
            html.Li([html.P("Number of brewers by production size by year (2008-2019)")]),
            html.Li([html.P("Monthly beer stats aggregated across the US (2008-2019)")]),
        ]),
        
        html.P("Notes about the data:"),

        html.Ul([

            html.Li([html.P("A barrel of beer for this data is 31 gallons")]),
            html.Li([html.P("Most data is in barrels removed/taxed or produced")]),
            html.Li([html.P("Removals = \"Total barrels removed subject to tax by the breweries comprising the named strata of data\", essentially how much was produced and removed for consumption.")]),

        ]),

        html.P('All of the data used in this project can be found at the link below:',
            className="mt-2 mb-2"),
        html.A("Tidy Tuesday: Fun New Datasets Every Week", href="https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-03-31")
    ], className="jumbotron")

# Layout for the states page
states_layout = html.Div([
        html.Hr(),
        html.Img(
            src=app.get_asset_url("states_cat_plot.png"),
            style={"width":"80%%", "height":"90%%"}
            ),
        html.Hr(),
        html.Img(
            src=app.get_asset_url("states_cat_plot_log.png"),
            style={"width":"80%%", "height":"90%%"}
            ),
        html.Hr(),
        dcc.Graph(
            id='state_graph',
            animate=True,
            style={
                    'rect': {
                        'width': '1px',
                        'color': 'red',
                        'background': 'red'
                    }
                }
        ),
        dcc.Slider(
            id='state_year_slider',
            min=value_range[0],
            max=value_range[1],
            step=1,
            value=value_range[0],
            marks={i: '{}'.format(i) for i in range(value_range[0],value_range[1]+1)}
        ),
        html.Hr(),
    ])

# Callbacks for states page
@app.callback(
    Output('state_graph', 'figure'),
    [
        Input('state_year_slider', 'value')
    ]
)
def update_states_page(state_year_slider):
    return choropleth_list[state_year_slider-value_range[0]]

# Callbacks for brewer size
@app.callback(
    Output('brewer_size_graph', 'figure'),
    [
        Input('brewer_size_xvar_1', 'value'),
        Input('brewer_size_yvar_1', 'value')
    ]
)
def update_brewer_size_graph(brewer_size_xvar_1, brewer_size_yvar_1):
    fig = px.scatter(brewer_size, x=brewer_size_xvar_1, y=brewer_size_yvar_1, color="year")
    fig.update_layout(coloraxis_colorbar=dict(
        title="Year",
        ticktext=[str(i) for i in range(value_range[0], value_range[1]+1)],
        lenmode="pixels", len=100,
    ))
    fig.update_layout(
        title_text = 'Brewer Size Information'
    )
    return fig

brewer_size_labels = ['Log Total Barrels', 'Log Taxable Removals', 'Log Total Shipped', 'Total Barrels', 'Taxable Removals', 'Total Shipped', 'Number of Brewers']
brewer_size_labels = [{'label': i, 'value': i} for i in brewer_size_labels]

# Layout for brewer size
brewer_size_layout = html.Div([
    html.Hr(),
    html.Div([
        dcc.Graph(
            id='brewer_size_graph',
            style={
                    'rect': {
                        'width': '1px',
                        'color': 'red',
                        'background': 'blue'
                    }
                }
        ),
    ]),
    html.Div([
        html.Div([
            html.Div(children='X Axis Variable'),
                
            html.Div([
                dcc.Dropdown(
                    id='brewer_size_xvar_1',
                    options=brewer_size_labels,
                    value='Number of Brewers'
                )
            ],
            style={'width': '100%', 'display': 'block'}),
        ], className="col-xs-6 col-md-4"),

        html.Div([
            html.Div(children='Y Axis Variable'),
                
            html.Div([
                dcc.Dropdown(
                    id='brewer_size_yvar_1',
                    options=brewer_size_labels,
                    value="Log Total Barrels"
                )
            ],
            style={'width': '100%', 'display': 'block'}),
        ], className="col-xs-6 col-md-4"),
    ], className="row"),
    html.Hr()
])

# Brewing materials callback
@app.callback(
    Output('difference_graph', 'figure'),
    [
        Input('material_type_1', 'value'),
        Input('material_type_2', 'value')
    ]
)
def update_brewing_material_by_type_graph(type, type2):
    data = brewing_materials[brewing_materials['type'] == type]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['Month Current'],
            marker=dict(color="blue", size=5),
            mode="lines",
            name=type
        )
    )

    data = brewing_materials[brewing_materials['type'] == type2]

    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['Month Current'],
            marker=dict(color="red", size=5),
            mode="lines",
            name=type2
        )
    )

    fig.update_layout(
        title_text = 'Total Material Used',
        xaxis_title="Year",
        yaxis_title="Month Current Total",
    )

    return fig

@app.callback(
    Output('total_material_by_type_graph', 'figure'),
    [
        Input('material_year_slider', 'value')
    ]
)
def update_brewing_material_graph(year):
    data = brewing_materials[brewing_materials['year'] == year]
    data = data.groupby(['Material Type'])['Year Current'].sum().reset_index()
    indexNames = data[ data['Material Type'] == "Grain Products" ].index
    data.drop(indexNames , inplace=True)

    indexNames = data[ data['Material Type'] == "Non-Grain Products" ].index
    data.drop(indexNames , inplace=True)
    fig = px.bar(data, x='Material Type', y='Year Current', text='Material Type')
    fig.update_layout(
        title_text = 'Total Material By Type Used',
    )
    return fig

# Brewing materials layout
brewing_materials_layout = html.Div([
    html.Hr(),

    dcc.Graph(
        id='difference_graph',
        style={
                'rect': {
                    'width': '1px',
                    'color': 'red',
                    'background': 'blue'
                }
            }
    ),

    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='material_type_1',
                    options=[{'label': i, 'value': i} for i in brewing_materials['type'].unique()],
                    value='Malt and malt products'
                )
            ],
            style={'width': '75%', 'display': 'block'}),
        ],className="col-xs-12 col-md-6"),

        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='material_type_2',
                    options=[{'label': i, 'value': i} for i in brewing_materials['type'].unique()],
                    value='Corn and corn products'
                )
            ],
            style={'width': '75%', 'display': 'block'}),
        ], className="col-xs-12 col-md-6"),
    ], className="row"),

    html.Hr(),

    dcc.Graph(
        id='total_material_by_type_graph',
        style={
                'rect': {
                    'width': '1px',
                    'color': 'red',
                    'background': 'blue'
                }
            }
    ),

    html.Div([  
        html.Div([
            dcc.Slider(
            id='material_year_slider',
            min=value_range[0],
            max=2014,
            step=1,
            value=value_range[0],
            marks={i: '{}'.format(i) for i in range(value_range[0],2015)}
            ),
        ],
        style={'width': '100%', 'display': 'block'}),
    ]),

    html.Hr()
])

# Taxes layout
taxes_layout = html.Div([
    html.Hr(),

    dcc.Graph(
        id='taxes_stacked_graph',
        style={
                'rect': {
                    'width': '1px',
                    'color': 'red',
                    'background': 'blue'
                }
            }
    ),

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='some_toggle',
                options=[{'label': i, 'value': i} for i in beer_taxed['type'].unique()],
                value='Production'
            )
        ], className="col-xs-6 col-md-4"),

        html.Div([
            dcc.Dropdown(
                id='some_toggle2',
                options=[{'label': i, 'value': i} for i in beer_taxed['type'].unique()],
                value='In barrels and kegs'
            )
        ], className="col-xs-6 col-md-4"),

        html.Div([
            dcc.Dropdown(
                id='type_toggle_22',
                options=[{'label': i, 'value': i} for i in ['Scatter', 'Line', 'Both']],
                value='Scatter'
            )
        ], className="col-xs-6 col-md-4")
    ], className="row"),

    html.Hr(),
])

# Taxes callbacks
@app.callback(
    Output('taxes_stacked_graph', 'figure'),
    [
        Input('some_toggle', 'value'),
        Input('some_toggle2', 'value'),
        Input('type_toggle_22', 'value')
    ]
)
def update_taxes_graph(value, value2, plot_type):

    pmap = {"Scatter":"markers", "Line":"lines", "Both":"lines+markers"}
    plot_type = pmap[plot_type]

    fig = go.Figure()

    data = beer_taxed[beer_taxed['tax_status'] == "Totals"]
    type_frame = data[data['type'] == value]

    fig.add_trace(
        go.Scatter(
            x=type_frame['Date'],
            y=type_frame['Month Current'],
            marker=dict(color="blue", size=5),
            mode=plot_type,
            name=value
        )
    )

    type_frame = beer_taxed[beer_taxed['type'] == value2]

    fig.add_trace(
        go.Scatter(
            x=type_frame['Date'],
            y=type_frame['Month Current'],
            marker=dict(color="red", size=5),
            mode=plot_type,
            name=value2
        )
    )

    fig.update_layout(
        title_text = 'Type Taxed Over Time',
        xaxis_title="Year",
        yaxis_title="Total",
    )

    return fig

not_found_layout = html.Div([
        html.H3('We can\'t find your pagie-wagie, uwu')
    ])

if __name__ == '__main__':
    app.run_server(debug=True)