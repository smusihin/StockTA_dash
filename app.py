import dash
import dash.dependencies as dd
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dte
import json
import requests_cache
import pandas as pd
import backend
from bitfinex import *
import plotly.graph_objs as go
from indicators.MovingAverage import *

app = dash.Dash(__name__)
app.title = 'Stock'
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
bf = bitfinex()
pairs = [{'label': str(n).upper(), 'value': str(n).upper()} for n in bf.getPairs()]
timeframes = [{'label': n, 'value': n} for n in ['1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '7D', '14D', '1M']]
indicators = [{'label': n, 'value': n} for n in backend.get_indicator_list()]


app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
  #              html.Div([
                    dcc.Dropdown(
                        id='pair',
                        options=pairs,
                        value=pairs[0]['value'],
                        className='nine columns'
                    ),
                    dcc.Dropdown(
                        id='timeframe',
                        options=timeframes,
                        value=timeframes[0]['value'],
                        className='offset-by-one two columns'
                    )],className='row'),
                html.Div([
                    dcc.Graph(id='graph',className='twelve columns')
                ],className = 'row'),
 #           ],className='container'),
        ],className = 'nine columns'),
        html.Div([
                dcc.Dropdown(
                     id='indicator',
                     options=indicators,
                     value=indicators[0]['value'],
                     ),
                html.Br(),
                dte.DataTable(
                    rows=[],
                    # optional - sets the order of columns
                    columns=['Parameter', 'Value'],
                    editable=True,
                    id='indicator_params'
                ),

        ],className= 'three columns')
    ],className='row'),
    html.Div(id='indicator_description', className='row')
], className='container')


@app.callback(dd.Output('graph', 'figure'), [dd.Input('pair', 'value'),
                                             dd.Input('timeframe', 'value'),
                                             dd.Input('indicator', 'value'),
                                             dd.Input('indicator_params', 'rows')])
def update_graph(pair,timeframe, indicator_name, param_rows):
     indicator = backend.get_indicator(indicator_name)
     params = {}
     for r in param_rows:
         params[r['Parameter']]=r['Value']
     indicator.set_params(params)
     df = bf.get_candles(pair, timeframe).sort_index()
     data = [go.Scatter(x=pd.to_datetime(df.index, unit='ms'), y=df['CLOSE'], mode='lines', name=pair, yaxis='y')]
     df_i = indicator.calculate(df['CLOSE'])
     for column in df_i.columns:
         data.append(go.Scatter(x=pd.to_datetime(df_i.index, unit='ms'), y=df_i[column], name = column, yaxis=indicator.yaxis))
     if indicator.yaxis == 'y2':
         layout_graph =  go.Layout(
         yaxis2=dict(domain=[0, 0.45]),
         yaxis=dict(domain=[0.55, 1]))
     else:
         layout_graph=[]
     return dict(data=data, layout=layout_graph)


@app.callback(dd.Output('indicator_description', 'children'), [dd.Input('indicator', 'value')],)
def update_description(indicator_name):
     indicator = backend.get_indicator(indicator_name)
     return indicator.description()

@app.callback(dd.Output('indicator_params', 'rows'), [dd.Input('indicator', 'value')],)
def update_params(indicator_name):
     indicator = backend.get_indicator(indicator_name)
     return [{'Parameter':key, 'Value':value} for key, value in indicator.params.items()]


if __name__ == '__main__':
     app.run_server()

