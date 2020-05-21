import dash
import dash_core_components as dcc
import dash_html_components as html
from pathlib import Path
import pandas as pd
idx=pd.IndexSlice
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots


df = pd.read_csv(Path.cwd() / 'captures/play_harp.csv', header=None, usecols=[0,1,2,3,4],
                 names=['loc','b', 'g', 'r', 'time'])


df2 = df.melt(id_vars=['time','loc'], value_vars=['b','g','r'],var_name='channel')
df2 = df2.astype({'channel':'str', 'value':'int64'})
df2 = df2.set_index(keys=['time','loc','channel'])
df2= df2.sort_index()


#%%
app = dash.Dash(__name__)

fig = px.line(df2.loc[idx[-5:,:,:],:], x=df2.index.get_level_values('time'),
              y='value',
              color=df2.index.get_level_values('channel'),
              animation_frame=df2.index.get_level_values('loc'))

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
