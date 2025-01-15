from dash import Dash, html, dcc, Input, Output, State, ctx, callback
import pandas as pd
import plotly.express as px
#from basecar import Auto
import dash_bootstrap_components as dbc
import csv
from drivedata_KPI import *
from driving_mode_1 import *
from driving_mode_2 import *
from driving_mode_3 import *
from driving_mode_4 import *
from driving_mode_5 import dm5
from basecar import BaseCar

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(["Drive Data Dashboard"], id="my-header"),
        dcc.Dropdown(["Distance", "Direction", "Speed", "Steering"], value="Distance", id="my-dd"),
        dbc.Col(dcc.Graph(id="my-graph")),
        html.Button('Show KPIs', id='btn-1', n_clicks=0),
        html.Div(id='container-button-timestamp'),
        html.Button('Stop Car', id='b-stop', n_clicks=0),
        html.Button('Driving Mode 1', id='b-dm1', n_clicks=0),
        html.Button('Driving Mode 2', id='b-dm2', n_clicks=0),
        html.Button('Driving Mode 3', id='b-dm3', n_clicks=0),
        html.Button('Driving Mode 4', id='b-dm4', n_clicks=0),
        html.Button('Driving Mode 5', id='b-dm5', n_clicks=0),
        html.Div(id='mode-container')
    ]
)


@app.callback(Output("my-graph", "figure"), Input("my-dd", "value"), prevent_initial_call=True)
def update_line_plot(dd_value):
    try:
        if False:
            csv_df = pd.read_csv('driving_data/driving_data.csv')
            fig = px.line(csv_df, x="Time", y=dd_value)
            return fig
    except pd.errors.EmptyDataError:
        print("CSV File empty")
    fig = px.line(csv_df, x="Time", y=dd_value)
    return fig

@app.callback(Output('container-button-timestamp', 'children'),Input('btn-1', 'n_clicks'), prevent_initial_call=False)
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

@app.callback(Output("mode-container", "children"), Input("b-stop", "n_clicks"), Input("b-dm1", "n_clicks"), Input("b-dm2", "n_clicks"), Input("b-dm3", "n_clicks"), Input("b-dm4", "n_clicks"), Input("b-dm5", "n_clicks"), prevent_initial_call=True)
def run_drive_modes(btnstop, bdm1, bdm2, bdm3, bdm4, bdm5):
    msg_dm = "Please select a Driving Mode"
    if "b-stop" == ctx.triggered_id:
        msg_dm = "Car Stops"
        BaseCar.finished = True
    elif "b-dm1" == ctx.triggered_id:
        msg_dm = "Ran Driving Mode 1" 
        BaseCar.finished = False
        dm1()  
    elif "b-dm2" == ctx.triggered_id:
        msg_dm = "Ran Driving Mode 2"
        BaseCar.finished = False
        dm2()
    elif "b-dm3" == ctx.triggered_id:
        msg_dm = "Ran Driving Mode 3"
        BaseCar.finished = False
        dm3()
    elif "b-dm4" == ctx.triggered_id:
        msg_dm = "Ran Driving Mode 4"
        BaseCar.finished = False
        dm4()
    elif "b-dm5" == ctx.triggered_id:
        msg_dm = "Ran Driving Mode 5"
        BaseCar.finished = False
        dm5()
        # script_path = 'driving_mode_5.py'
        # exec(open(script_path).read())
    return msg_dm


if __name__ == "__main__":
    app.run_server(debug=True, host="localhost", port=1234)