from dash import Dash, html, dcc, Input, Output, ctx, callback
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from drivedata_KPI import *
from basecar import BaseCar
from driving_mode_4 import *
from driving_mode_5 import * 
import math

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        html.H1(["Drive Data Dashboard"], id="my-header"),
        dcc.Dropdown(["Time", "Direction", "Speed", "Steering", "Distance", "IR-v1", "IR-v2", "IR-v3", "IR-v4", "IR-v5"], value="Steering", id="my-dd"),
        dbc.Col(dcc.Graph(id="my-graph")),
        html.Button('Show KPIs', id='btn-1', n_clicks=0),
        html.Div(id='container-button-timestamp'),
        html.Button('Stop Car', id='b-stop', n_clicks=0),
        html.Button('Driving Mode 1', id='b-dm1', n_clicks=0),
        html.Button('Driving Mode 2', id='b-dm2', n_clicks=0),
        html.Button('Driving Mode 3', id='b-dm3', n_clicks=0),
        html.Button('Driving Mode 4', id='b-dm4', n_clicks=0),
        html.Button('Driving Mode 5', id='b-dm5', n_clicks=0),
        html.Div(id='mode-container'),
        html.H4('Simple stock plot'),
        html.P("Change figure width:"),
        dcc.Slider(id='slider', min=200, max=500, step=25, value=300,marks={x: str(x) for x in [200, 300, 400, 500]}),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(Output("my-graph", "figure"), Input("my-dd", "value"), prevent_initial_callbacks=True)
def update_line_plot(dd_value):
    try:
        csv_df = pd.read_csv('driving_data/driving_data.csv')
        fig = px.line(csv_df, x="Time", y=dd_value)
        return fig
    except pd.errors.EmptyDataError:
        print("CSV File empty")
    return fig

@app.callback(Output('container-button-timestamp', 'children'),Input('btn-1', 'n_clicks'), prevent_initial_callbacks=True)
def displayClick(btn1):
    msg = "Empty"
    if "btn-1" == ctx.triggered_id:
        msg = ("Max Speed :",round(max_speed, 2), ' | ' ,               # \n for new Row doesnt work...
               "Min Speed :",round(min_speed, 2), ' | ' ,
               "Average Speed :", round(average_speed, 2), ' | ' ,
               "Distance Traveled :",round(distance_traveled, 2), ' | ' ,
               "Total Time :", round(sum_time,2)
               )                 
    return msg

@app.callback(Output("mode-container", "children"), Input("b-stop", "n_clicks"), Input("b-dm1", "n_clicks"), Input("b-dm2", "n_clicks"), Input("b-dm3", "n_clicks"), Input("b-dm4", "n_clicks"), Input("b-dm5", "n_clicks"), prevent_initial_callbacks=True)
def run_drive_modes(btnstop, bdm1, bdm2, bdm3, bdm4, bdm5):
    msg_dm = "Please select a Driving Mode"
    if "b-stop" == ctx.triggered_id:
        msg_dm = "Car Stops"
        BaseCar.finished = True
    elif "b-dm1" == ctx.triggered_id:
        msg_dm = "Ran Driving Mode 1" 
        BaseCar.finished = False
        script_path = 'driving_mode_1.py'
        exec(open(script_path).read())  
    elif "b-dm2" == ctx.triggered_id:
        msg_dm = "Ran Driving Mode 2"
        BaseCar.finished = False
        script_path = 'driving_mode_2.py'
        exec(open(script_path).read())
    elif "b-dm3" == ctx.triggered_id:
        msg_dm = "Ran Driving Mode 3"
        BaseCar.finished = False
        script_path = 'driving_mode_3.py'
        exec(open(script_path).read())
    elif "b-dm4" == ctx.triggered_id:
        msg_dm = "Ran Driving Mode 4"
        BaseCar.finished = False
        script_path = 'driving_mode_4.py'
        exec(open(script_path).read())
    elif "b-dm5" == ctx.triggered_id:
        msg_dm = "Ran Driving Mode 5"
        BaseCar.finished = False
        script_path = 'driving_mode_5.py'
        exec(open(script_path).read())
    return msg_dm

@app.callback(Output("graph", "figure"),Input('slider', 'value'), prevent_initial_callbacks=True)
def resize_figure(width):
    df = read_data()
    fig = px.line(df, x='x', y='y')  
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",)
    fig.update_layout(width=int(width))
 
    return fig

def read_data():
    path = "driving_data/driving_data.csv"
    drive_data = pd.read_csv(path)
    data_speed = drive_data["Speed"]
    data_time = drive_data['Time']
    data_steering = drive_data['Steering']
 
    x = 0.0
    y = 0.0
 
    df = pd.DataFrame(columns=["x", "y"])
    df.loc[0] = [x, y]
 
    for i in range(1, len(drive_data)):

        t = data_time[i] - data_time[i-1]
        v = data_speed[i-1]
        s = v * t
 
        x = x + s * math.cos(math.radians(data_steering[i-1]))
        y = y + s * math.sin(math.radians(data_steering[i-1]))
        df.loc[i] = [x, y]
 
    return df

if __name__ == "__main__":
    app.run_server(debug=True, host="localhost", port=1234)