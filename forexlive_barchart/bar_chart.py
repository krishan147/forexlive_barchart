import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import random
import plotly.graph_objs as go
from collections import deque
import time
import requests
import datetime
rate_list = []

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='graphone', animate=False),
        dcc.Interval(id='updateone',interval=1*6000),
    ]
)

@app.callback(Output('graphone', 'figure'),events=[Event('updateone', 'interval')])
def update_graph_scatter():
    traces = list()
    rate_list = []

    symbols = ['USDGBP','USDEUR','USDKWD']

    url = 'https://www.freeforexapi.com/api/live?pairs=USDGBP,USDEUR,USDKWD'
    request = requests.get(url)
    gbp_rate = request.json()['rates']["USDGBP"]["rate"]
    gbp_time = request.json()['rates']["USDGBP"]["timestamp"]
    eur_rate = request.json()['rates']["USDEUR"]["rate"]
    eur_time = request.json()['rates']["USDEUR"]["timestamp"]
    kwd_rate = request.json()['rates']["USDKWD"]["rate"]
    kwd_time = request.json()['rates']["USDKWD"]["timestamp"]

    rate_list.append(gbp_rate)
    rate_list.append(eur_rate)
    rate_list.append(kwd_rate)

    print (symbols)

    traces.append(go.Bar(
            x=symbols,
            y=rate_list,
            name='barchart'
            ))

    print (traces)

    return {'data': traces}


if __name__ == '__main__':
    app.run_server(debug=True)