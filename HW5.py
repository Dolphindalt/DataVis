#!/usr/bin/env python
# coding: utf-8

# In[15]:


from pylab import *
import h5py
f = h5py.File("data/GreenlandInBedCoord.h5")
H  = array(f["thickness"],dtype=float32) # Ice thickness (m)
ux = array(f["VX"],dtype=float32)        # x component of velocity (m/year)
uy = array(f["VY"],dtype=float32)        # y component of velocity (m/year)
S  = array(f["surface"],dtype=float32)   # Surface elevation (m above sea level)
B  = array(f["bed"],dtype=float32)       # Elevation of material under ice (m above sea level)
T  = array(f["t2m"],dtype=float32)      # Mean annual temperature at 2 m above surface (C)
A  = array(f["smb"],dtype=float32)       # Rate of ice accumulation (m/year)
X  = array(f["x"])                       # x coordinate of data
Y  = array(f["y"])                       # y coordinate of data

#dimension of data
print(len(X))
print(len(Y))

#Can reduce size of data if renders too slow
S.shape
reduce=100
s= S[::reduce,::reduce]
s.shape

reduce=100
x,y = np.meshgrid(X[::reduce], Y[::reduce])
u = ux[::reduce,::reduce]
v = uy[::reduce,::reduce]

reduce=10
B = B[::reduce, ::reduce]

reduce=100
T = T[::reduce, ::reduce]

H = H[::-1]


# In[16]:


# Standard plotly imports
import plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot
import plotly.figure_factory as ff

# Data science imports
import numpy as np

import cufflinks
cufflinks.go_offline()

import cmocean
import json


# At this point, I do not know what to do so let's start with some heightmaps and a quiver plot.

# In[17]:


def cmocean_to_plotly(cmap, pl_entries=100):
    h = 1.0/(pl_entries-1)
    pl_colorscale = []
    
    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])
        
    return pl_colorscale


# In[18]:


#Create the arrows, use scale to increase arrow size
#A figure is returned, with a scattered data component
fig = ff.create_quiver(x, y, u, v,
                       scale=1000,
                       arrow_scale=.3,
                       name='quiver',
                       line=dict(width=2,color='red'))

#Add the figure layout
layout = go.Layout(
    width=800,
    height=800,
    autosize=False,
    margin=dict(t=50, b=50, l=50, r=50),
    scene=dict(
        xaxis=dict(
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=True,
            backgroundcolor='rgb(230, 230,230)'
        ),
        yaxis=dict(
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=True,
            backgroundcolor='rgb(230, 230, 230)'
        ),
        zaxis=dict(
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=True,
            backgroundcolor='rgb(230, 230,230)'
        ),
        aspectratio = dict(x=1, y=1, z=0.7),
        aspectmode = 'manual'
    )
)

button_layer_1_height = 1.12

updatemenus=list([
    dict(
        buttons=list([   
            dict(
                args=[{"visible": [True, False, False, False]}],
                label='Glacier Movement',
                method='restyle'
            ),
            dict(
                args=[{"visible": [False, True, False, False]}],
                label='Glacier Height',
                method='restyle'
            ),
            dict(
                args=[{"visible": [False, False, True, False]}],
                label='Elevation Under Ice',
                method='restyle'
            ),
            dict(
                args=[{"visible": [False, False, False, True]}],
                label='Ice Thickness',
                method='restyle'
            )
        ]),
        #button properties
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        x = 0.1,
        xanchor = 'left',
        y = button_layer_1_height,
        yanchor = 'top' 
    ),
    dict(
        buttons=list([
            dict(
                args=['colorscale', json.dumps(cmocean_to_plotly(cmocean.cm.haline)) ],
                label='Haline',
                method='restyle'
            ),
            dict(
                args=['colorscale', json.dumps(cmocean_to_plotly(cmocean.cm.turbid))],
                label='Turbid',
                method='restyle'
            ),
            dict(
                args=['colorscale', json.dumps(cmocean_to_plotly(cmocean.cm.deep))],
                label='Deep',
                method='restyle'
            ),
        ]),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        x = 0.75,
        xanchor = 'left',
        y = button_layer_1_height,
        yanchor = 'top'            
    ),
])

#Text annotations placed to left of dropdown buttons
# I can't get these lads to show up in the right place
#annotations = list([
    #dict(text='Data', x=0, y=1.11, yref="paper", showarrow=False),
    #dict(text='Color Scheme', x=0.5, y=1.11, yref="paper", showarrow=False, align='left')
#])

#Add buttons and annotation to the layout
layout['updatemenus'] = updatemenus
#layout['annotations'] = annotations

# the heatmap was upside down so I reversed the array
trace2 = go.Heatmap(z=S[::-1], visible=False, name="Surface Elevation")

# heatmap for elevation under the ice
trace3 = go.Heatmap(z=B[::-1], name="Surface Elevation Under Ice", visible=False)

# heatmap for ice thickness
trace4 = go.Heatmap(z=H[::-1], visible=False, name="Ice Thickness")

data = [fig['data'][0], trace2, trace3, trace4]

fig = go.Figure(data=data, layout=layout)

iplot(fig, filename='greenland_quiver')


# In[19]:


# Now for three visuals that support the hypothesis.
# Hypothesis:
# Areas of Greenland with more ice layered upon the surface will have lower elevations 
# due to the principle of isostasy.


# In[20]:


def plot_3d_surface_and_heatmap(z):
    
    sh_0, sh_1 = z.shape
    x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
    data = [go.Surface(x=x, y=y, z=z, colorscale='Haline')]

    layout = go.Layout(
        width=800,
        height=800,
        autosize=False,
        margin=dict(t=0, b=0, l=0, r=0),
        scene=dict(
            xaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            yaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230, 230)'
            ),
            zaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            aspectratio = dict(x=1, y=1, z=0.7),
            aspectmode = 'manual'
        )
    )

    #Create a dropdown buttons that modify how data is displayed
    updatemenus=list([
        dict(
            buttons=list([   
                dict(
                    args=['type', 'surface'],
                    label='3D Surface',
                    method='restyle'
                ),
                dict(
                    args=['type', 'heatmap'],
                    label='Heatmap',
                    method='restyle'
                )             
            ]),
            #button properties
            direction = 'down',
            pad = {'r': 10, 't': 10},
            showactive = True,
            x = 0.1,
            xanchor = 'left',
            y = 1.1,
            yanchor = 'top' 
        ),
    ])

    #Text annotation for button
    annotations = list([
        dict(text='Trace type:', x=0, y=1.085, yref='paper', align='left', showarrow=False)
    ])

    #Add buttons and annotation to the layout
    layout['updatemenus'] = updatemenus
    layout['annotations'] = annotations

    fig = dict(data=data, layout=layout)
    iplot(fig)


# In[21]:


plot_3d_surface_and_heatmap(H[::2])


# In[ ]:




