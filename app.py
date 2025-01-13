from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
#from basecar import Auto
import dash_bootstrap_components as dbc
import csv

csv_df = pd.read_csv('driving_data/driving_data.csv')
#print(csv_df)

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(["Drive Data Dashboard"], id="my-header"),
        dcc.Dropdown(["Distance", "Direction", "Speed", "Steering"], value="Distance", id="my-dd"),
        dbc.Col(dcc.Graph(id="my-graph")),
        #dcc.Textarea(id='textarea',value='Max Speed : {100}\nMin Speed : {1}\nAverage Speed : {50}\nDistance Traveled : {1111}cm\nTotal Time Driven : {1000}s',style={'width': '10%', 'height': 100},),
        #html.Div(id='textarea-output', style={'whiteSpace': 'pre-line'}),
        html.H1(["This are the KPIs:"], id="h2"),
        html.H2(["Max Speed : {100}"], id="h3"),
        html.H2(["Min Speed : {1}"], id="h4"),
        html.H2(["Average Speed : {50}"], id="h5"),
        html.H2(["Distance Traveled : {1111}cm"], id="h6"),
        html.H2(["Total Time Driven : {1000}s"], id="h7")
    ]
)

@app.callback(Output("my-graph", "figure"), Input("my-dd", "value"))
def update_line_plot(dd_value):
    fig = px.line(csv_df, x="Time", y=dd_value)
    return fig

#@app.callback(Output('textarea-output', 'children'),Input('textarea', 'value'))
#def update_output(value):
#    return 'This are the KPIs: \n{}'.format(value)

if __name__ == "__main__":
    app.run_server(debug=True, host="localhost", port=1234)