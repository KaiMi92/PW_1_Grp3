from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
#from basecar import Auto
import dash_bootstrap_components as dbc
import csv

csvdf = pd.read_csv('drivedata.csv')
print(csvdf)

app = Dash(__name__)

x = list(range(30))

df = pd.DataFrame({"x": x, "y": [i**2 for i in x], "z": [i**0.5 for i in x]})

app.layout = html.Div(
    [
        html.H1(["Drive Data Dashboard"], id="my-header"),
        dcc.Dropdown(["x", "y", "z"], value="x", id="my-dd"),
        dbc.Col(dcc.Graph(id="my-graph")),
    ]
)

@app.callback(Output("my-graph", "figure"), Input("my-dd", "value"))
def update_line_plot(dd_value):
    fig = px.line(df, x="x", y=dd_value)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True, host="localhost", port=1234)