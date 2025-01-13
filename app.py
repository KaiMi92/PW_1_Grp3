from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
#from basecar import Auto
import dash_bootstrap_components as dbc
import csv

csv_df = pd.read_csv('drivedata.csv')
print(csv_df)

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(["Drive Data Dashboard"], id="my-header"),
        dcc.Dropdown(["Distance", "Direction", "Speed", "Steering"], value="Distance", id="my-dd"),
        dbc.Col(dcc.Graph(id="my-graph")),
    ]
)

@app.callback(Output("my-graph", "figure"), Input("my-dd", "value"))
def update_line_plot(dd_value):
    fig = px.line(csv_df, x="Time", y=dd_value)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True, host="localhost", port=1234)