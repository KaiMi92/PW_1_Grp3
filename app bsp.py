from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
from basecar import Auto
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

auto = Auto()

x = list(range(30))

df = pd.DataFrame({"x": x, "y": [i**2 for i in x], "z": [i**0.5 for i in x]})

# App Layout
app.layout = html.Div(
    [
        dbc.Row(
            [
                html.H1(["Hallo Dash-Welt"], id="my-header"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="my-graph"), width=5),
                dbc.Col(
                    [
                        dcc.Dropdown(["x", "y", "z"], value="x", id="my-dd"),
                        dcc.Slider(min=1, max=10, step=1, value=5, id="my-slider"),
                        dbc.Card(dbc.CardBody(dbc.Button("Stop", id="stop-button", color="error"))),
                    ],
                    width=5,
                ),
            ]
        ),
    ]
)


# Verknüpfungen bzw. Funktionen
@app.callback(Output("my-header", "children"), Input("my-dd", "value"), prevent_initial_call=True)
def change_header(selected_value):
    return f"Meine Auswahl war: {selected_value}"


@app.callback(
    Output("my-header", "children", allow_duplicate=True),
    Input("my-slider", "value"),
    State("my-dd", "value"),
    prevent_initial_call=True,
)
def change_header_2(slide_value, dd_value):
    return f"Der zweite Callback: {dd_value*int(slide_value)}"


@app.callback(Output("my-graph", "figure"), Input("my-dd", "value"))
def update_line_plot(dd_value):
    fig = px.line(df, x="x", y=dd_value)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8051)