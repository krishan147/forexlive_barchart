import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import requests
import datetime
from flask_caching import Cache
from flask_restful import Resource, Api
rate_list = []
import flask
date_now = datetime.datetime.now().replace(microsecond=0)

application = server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
cache = Cache(application, config={'CACHE_TYPE': 'simple'})
api = Api(application)

app.layout = html.Div(
    [
        html.Div(id='live-update-text'),
            dcc.Interval(
            id='interval-component',
            interval=1 * 2500,  # in milliseconds
            n_intervals=0,
            # typeface = "Arial"
        ),

        dcc.Graph(id='graphone', animate=False),
        dcc.Interval(id='updateone', interval=1 * 2500)


    ]
)

@app.callback(Output('graphone', 'figure'),events=[Event('updateone', 'interval')])
def update_graph_scatter():
    traces = list()
    date_now = datetime.datetime.now().replace(microsecond=0)

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

    traces.append(go.Bar(
            x=symbols_list,
            y=rate_list,
            text = rate_list,
            name='barchart',
            textposition='auto',
            marker=dict(
                color='rgb(120,120,120)',
                line=dict(
                    color='rgb(1,32,96)',
                    width=1.5),
            ),
    )
)
    return {'data': traces}

@app.callback(Output('live-update-text', 'children'),[Input('interval-component', 'n_intervals')])
def update_metrics(n):
    return "Last updated: "+str(datetime.datetime.now().replace(microsecond=0))

if __name__ == '__main__':
    app.run_server(debug=True)