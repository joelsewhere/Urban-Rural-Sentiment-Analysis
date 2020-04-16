import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from gensim.models import Word2Vec
from dash.dependencies import Input, Output, State

df = pd.read_csv('predicted_sentiment_data.csv')
df = df[df.text.notnull()]
chi = df[df.target > 0]
il_x = df[df.target < 1]

chi_vectors = Word2Vec.load('chicago_vectors.bin')
il_x_vectors = Word2Vec.load('il_x_vectors.bin')


app = dash.Dash()

app.layout = html.Div(children = [
    html.H1('Chicago Vs. Illinois Sentiment'),
    dcc.Input(id='input', value='Enter a topic', type='text'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-graph')])
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input('submit-button', 'n_clicks')],
    [State(component_id='input', component_property='value')])   
def update_graph(n_clicks, input_data):
    lower = input_data.lower()
    tokens = lower.split()
    
    try:
        chi_lst = chi_vectors.wv.most_similar(positive = tokens)
    except:
        chi_lst = False
    try:
        il_x_lst = il_x_vectors.wv.most_similar(positive = tokens)
    except:
        il_x_lst = False

    if chi_lst:
        if il_x_lst:

            chi_words = [x[0] for x in chi_lst]
            il_words = [x[0] for x in il_x_lst]
            chi_words += tokens
            il_words += tokens

            chi_mentions = [len(chi[chi.text.str.contains(x)]) for x in chi_words]
            il_mentions = [len(il_x[il_x.text.str.contains(x)]) for x in il_words]

            chi_sent = [chi[chi.text.str.contains(x)].sentiment.mean() for x in chi_words]
            il_sent = [il_x[il_x.text.str.contains(x)].sentiment.mean() for x in il_words]

            return dcc.Graph(id = 'example',
            figure = {
            'data': [
                go.Scatter(x= chi_mentions, y = chi_sent, mode =  'markers', marker = {'color': 'blue',
                                                                                        'size': 40,
                                                                                        'opacity': 0.5,},
                                                                                        hovertext = chi_words,
                                                                                        name = 'Chicago' ),
                go.Scatter(x = il_mentions, y = il_sent, mode = 'markers', marker = {'color': 'green',
                                                                                'size': 40,
                                                                                'opacity': 0.5},
                                                                                hovertext = il_words,
                                                                                name = 'Illinois')
            ],

            'layout' : go.Layout(
                title = 'Chicago vs. Illinois Sentiment',
                xaxis={'type': 'log', 'title': 'Number of mentions'},
                yaxis={'title': 'Sentiment (Negative to Positive)'}
                    )
                }
            )
        else:
            chi_words = [x[0] for x in chi_lst]
            chi_words += tokens
            chi_mentions = [len(chi[chi.text.str.contains(x)]) for x in chi_words]
            chi_sent = [chi[chi.text.str.contains(x)].sentiment.mean() for x in chi_words]
            return dcc.Graph(id = 'example',
            figure = {
            'data': [
                go.Scatter(x= chi_mentions, y = chi_sent, mode =  'markers', marker = {'color': 'blue',
                                                                                        'size': 40,
                                                                                        'opacity': 0.5,},
                                                                                        hovertext = chi_words,
                                                                                        name = 'Chicago' )
            ],
            'layout' : go.Layout(
                title = 'Chicago Sentiment –– Word not mentioned outside of Chicago.',
                xaxis={'type': 'log', 'title': 'Number of mentions'},
                yaxis={'title': 'Sentiment (Negative to Positive)'}
                    )
                }
            )
    elif il_x_lst:
        il_words = [x[0] for x in il_x_lst]
        il_words += tokens
        il_mentions = [len(il_x[il_x.text.str.contains(x)]) for x in il_words]
        il_sent = [il_x[il_x.text.str.contains(x)].sentiment.mean() for x in il_words]
        return dcc.Graph(id = 'example',
            figure = {
            'data': [
                go.Scatter(x = il_mentions, y = il_sent, mode = 'markers', marker = {'color': 'green',
                                                                                'size': 40,
                                                                                'opacity': 0.5},
                                                                                hovertext = il_words,
                                                                                name = 'Illinois')
            ],

            'layout' : go.Layout(
                title = 'Illinois Sentiment –– Word not mentioned in Chicago',
                xaxis={'type': 'log', 'title': 'Number of mentions'},
                yaxis={'title': 'Sentiment (Negative to Positive)'}
                    )
                }
            )

if __name__ == '__main__':
    app.run_server(debug=True)




