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
indicators = [{'label': n, 'value': n} for n in backend.get_indicator_list()]


app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='pair',
                options=pairs,
                value=pairs[0]['value'],
            ),
            dcc.Graph(id='graph')

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
                                             dd.Input('indicator', 'value'),
                                             dd.Input('indicator_params', 'rows')])
def update_graph(pair, indicator_name, param_rows):
     indicator = backend.get_indicator(indicator_name)
     params = {}
     for r in param_rows:
         params[r['Parameter']]=r['Value']
     indicator.set_params(params)
     df = bf.get_candles(pair, '1M').sort_index()
     data = [go.Scatter(x=pd.to_datetime(df.index, unit='ms'), y=df['CLOSE'], mode='lines', name=pair)]
     df_i = indicator.calculate(df['CLOSE'])
     for column in df_i.columns:
         data.append(go.Scatter(x=pd.to_datetime(df_i.index, unit='ms'), y=df_i[column], name = column))
     return dict(data=data)


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

