import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff

import pickle
import pandas as pd
import os
import numpy as np


choropleth_data = pd.read_csv('choropleth_data.csv')
with open('map_topics.pickle', 'rb') as file:
    map_topics = pickle.load(file)

with open('decode.pickle', 'rb') as reverse:
    decode = pickle.load(reverse)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])


app.layout = html.Div([
    dbc.Row(
        dbc.Col(html.Div(html.H1("The Counties of Illinois"), style=dict(padding=10)))),
    dbc.Row(dbc.Col(html.Div(html.P(
        "Select a topic and explore the differences between each County."), style=dict(padding=17)))),

    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    dcc.Loading(
                        [
                            dcc.Graph(
                                id="choropleth-map",
                                style={'width': '100%',
                                       'height': '100%'})]),
                    style={'width': '49%',
                           'display': 'inline-block'})),

            dbc.Col(
                html.Div(
                    dcc.Dropdown(
                        id='map_topic_dropdown',
                        options=map_topics,
                        value='Median age: Total',
                        style=dict(width='100%')),
                    style={'width': '60%', 'display': 'inline-block'}))])])


@app.callback(
    Output(component_id='choropleth-map', component_property='figure'),
    [Input(component_id='map_topic_dropdown', component_property='value')])
def update_choropleth(value):
    datapoints = choropleth_data[value].astype('int').tolist()
    fig = ff.create_choropleth(
        fips=choropleth_data.GISJOIN.tolist(),
        values=datapoints, scope=['IL'],
        county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, round_legend_values=True,
        legend_title=value, title=decode[value]
    )

    fig.layout.template = "plotly"
    if value == 'Median age: Total':
        t = ()
        for i in range(len(fig.data[-2]['text'])):
            new_label1 = fig.data[-2]['text'][i].replace(
                "FIPS: %s<br>" % choropleth_data.GISJOIN.tolist()[i], "")
            new_label2 = new_label1.replace('Value', 'Median Age')
            new_label3 = new_label2.replace(
                "State: Illinois<br>", "")
            t += (new_label3,)
    elif value == 'total_population':
        t = ()
        for i in range(len(fig.data[-2]['text'])):
            new_label1 = fig.data[-2]['text'][i].replace(
                "FIPS: %s<br>" % choropleth_data.GISJOIN.tolist()[i], "")
            new_label2 = new_label1.replace('Value', 'Population')
            new_label3 = new_label2.replace(
                "State: Illinois<br>", "")
            t += (new_label3,)

    else:
        t = ()
        for i in range(len(fig.data[-2]['text'])):
            new_label1 = fig.data[-2]['text'][i].replace(
                "FIPS: %s<br>" % choropleth_data.GISJOIN.tolist()[i], "")
            new_label2 = new_label1.replace('Value', 'Percentage')
            new_label3 = new_label2.replace(
                "State: Illinois<br>", "")
            t += (new_label3,)
    fig.layout.update(dict(paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)'))
    fig.data[-2]['text'] = t
    return fig


server = app.server
if __name__ == '__main__':
    app.run_server(debug=True)
