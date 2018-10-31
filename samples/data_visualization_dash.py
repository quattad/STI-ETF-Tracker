"""
BOOKMARK: Video 5 https://www.youtube.com/watch?v=luixWRpp6Jo&list=PLQVvvaa0QuDfsGImWNt1eUEveHOepkjqt&index=5
install necessary pip modules
pip install dash dash-renderer dash-html-components dash-core-components plotly
Dash is built with Flask. can embed with flask applications, etc. possible to do down the road. possibility for project extension
Callback function: function to be executed after another function has executed
"""

"""
dash_core_components: divs etc
dash_html_components: html etc
deque: container that allows you to specify size of list. e.g. if 20 element size, if try to insert 21 elements it pops 0th element.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event
import pandas_datareader.data as web
import datetime
import plotly
import random
import plotly.graph_objs as go
from collections import deque

app = dash.Dash(__name__)

""" INTRODUCTION TO APP LAYOUT"""
"""
app.layout: html of entire project. serves as HTML of project. div tag that contains graph.
children: actual contents of web page. can be single element or list. see children = ['Dash tutorials']
apply header tag to children : html.H1(children=['Dash tutorials'])
dcc.Graph() : creates graph
"""
# app.layout = html.Div(children=
# [
#     html.H1('Dash Tutorials'),
#     dcc.Graph(id='example',
#               figure={
#                   'data': [
#                       {'x': [1, 2, 3, 4, 5], 'y': [5, 6, 6, 4, 2], 'type':['line'], 'type': 'line', 'name':'boats'},
#                       {'x': [2, 3, 4, 5, 6], 'y': [5, 5, 5, 2, 2], 'type': ['line'], 'name': 'bar', 'name':'cars'}
#                           ],
#                   'layout':
#                       {'title': 'Basic Dash Example'}
#                       }
#               )
# ])


"""DYNAMICALLY UPDATE HTML ELEMENTS WITHOUT PAGE REFRESH"""
# app.layout = html.Div(children=[
#     dcc.Input(id='input', value='Enter something', type='text'),
#     html.Div(id='output')
# ])

# @app.callback(
#     Output(component_id='output', component_property='children'),
#     [Input(component_id='input', component_property='value')])
# def update_value(input_data):
#     return "Input: {}".format(input_data)
""" could modify more properties besides children"""


""" BRINGS GRAPH INTO DASH AND GETS USER INPUT TO UPDATE GRAPH"""
# start = datetime.datetime(2015, 1, 1)
# end = datetime.datetime.now()
#
# stock = 'TSLA'
# df = web.DataReader(stock, 'yahoo', start, end)

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),
#     html.Div(children='''Symbol to graph:'''),
#     dcc.Input(id='input', value='TSLA', type='text'),  # obtain input from the user
#     html.Div(children='Web framework for Python'),
#     # Commented out to test auto graph updating
#     #           figure={'data': [{'x': df.index,
#     #                            'y': df['Close'],
#     #                            'type': 'line',
#     #                            'name': stock}],
#     #                   'layout':{
#     #                       'title':stock
#     #                   }}),
#     html.Div(id='output-graph')
# ])
#
# @app.callback(
#     Output(component_id='output-graph', component_property='children'),
#     [Input(component_id='input', component_property='value')]
# )
# def update_graph(input_data):
#     start = datetime.datetime(2015, 1, 1)
#     end = datetime.datetime.now()
#     df = web.DataReader(input_data, 'yahoo', start, end)
#
#     return dcc.Graph(id='example-graph',
#               figure={
#                   'data': [{
#                       'x': df.index,
#                       'y': df.Close,
#                       'type':'line',
#                       'name':input_data
#                   }],
#                   'layout':{
#                       'title':input_data
#                   }
#               })

""" AUTOMATED UPDATING OF GRAPH"""

# create deques for x and y axes
X = deque(maxlen=50)
Y = deque(maxlen=50)
X.append(1)
Y.append(1)

# create dropdown for people to choose which field to plot
data_dict = {"Parameter 1": X,
             "Parameter 2": Y}

# main html
app.layout = html.Div([
        dcc.Graph(id='live-graph',
               animate=True),
        dcc.Interval(id='graph-update',
                     interval=2000)
    ],
    className="container",
    style={'width': '100%',
             'margin-left': 10,
             'margin-right': 10
           }
)


@app.callback(Output('live-graph', 'figure'), # update figure. figure is a dictionary that contains graph fields as keys and graph attributes as values
              events=[Event('graph-update', 'interval')])  # Event() takes in id of event. Interval class calls ID every 1 second, could use many other types of events.
def update_graph():
    X.append(X[-1] + 1)  # X is the x-axis. X[-1] calls the last element and adds 1 to the x element
    Y.append(Y[-1] + (Y[-1]*random.uniform(-0.1, 0.1)))  # add some randomness, not sure of its effect

    data = go.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'  # plotly only has scatter graphs with lines drawn in-between
    )

    return {'data':[data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                               yaxis=dict(range=[min(Y), max(Y)]))}


if __name__ == '__main__':
    app.run_server(debug=True)