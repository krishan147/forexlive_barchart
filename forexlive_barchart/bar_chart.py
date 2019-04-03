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
        dcc.Interval(id='updateone',interval=1*2500),
    ]
)

@app.callback(Output('graphone', 'figure'),events=[Event('updateone', 'interval')])
def update_graph_scatter():
    traces = list()
    rate_list = []
    symbols_list = ['USDGBP','USDEUR','USDKWD','USDCHF','USDCAD','USDZAR']

    url = 'https://www.freeforexapi.com/api/live?pairs=USDGBP,USDEUR,USDKWD,USDJPY,USDCHF,USDCAD,USDZAR'
    request = requests.get(url)
    gbp_rate = request.json()['rates']["USDGBP"]["rate"]
    gbp_time = request.json()['rates']["USDGBP"]["timestamp"]
    eur_rate = request.json()['rates']["USDEUR"]["rate"]
    eur_time = request.json()['rates']["USDEUR"]["timestamp"]
    kwd_rate = request.json()['rates']["USDKWD"]["rate"]
    kwd_time = request.json()['rates']["USDKWD"]["timestamp"]

    chf_rate = request.json()['rates']["USDCHF"]["rate"]
    chf_time = request.json()['rates']["USDCHF"]["timestamp"]

    cad_rate = request.json()['rates']["USDCAD"]["rate"]
    cad_time = request.json()['rates']["USDCAD"]["timestamp"]

    zar_rate = request.json()['rates']["USDZAR"]["rate"]
    zar_time = request.json()['rates']["USDZAR"]["timestamp"]

    rate_list.append(gbp_rate)
    rate_list.append(eur_rate)
    rate_list.append(kwd_rate)
    rate_list.append(chf_rate)
    rate_list.append(cad_rate)
    rate_list.append(zar_rate)

    print (rate_list)

    traces.append(go.Bar(
            x=symbols_list,
            y=rate_list,
            text = rate_list,
            name='barchart',
            textposition='auto',
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5),
        ),
            ))


    return {'data': traces}


if __name__ == '__main__':
    app.run_server(debug=True)