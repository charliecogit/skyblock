import dash
import dash_core_components as dcc
import dash_html_components as html
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(Path.cwd() / 'captures/play_harp.csv', header=None, usecols=[0,1,2,3,4,5,6],
                 names=['loc', 'filled', 'b', 'g', 'r', 'change', 'time'])

df2 = df.melt(id_vars=['time','loc'], value_vars=['b','g','r', 'change'],var_name='channel')

app = dash.Dash(__name__)

fig = px.line(df2, x='time', y='value', color='channel',
              animation_frame='loc')

#%%


#%%
app.layout = html.Div(children=[
    html.H1(children="Melodie's Harp"),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure= fig

    )
])

app.run_server(debug=True)
