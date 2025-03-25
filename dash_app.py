from dash import Dash, html, dcc, Input, Output, ctx
import dash_bootstrap_components as dbc
from flask import Flask, Response
from opencvcar import OpenCvCar
import os

external_stylesheets = [dbc.themes.BOOTSTRAP]
server = Flask(__name__)

app = Dash(__name__, external_stylesheets=external_stylesheets, server=server)
open_cv_car = OpenCvCar()
proc = open_cv_car.proc        

cmd = "v4l2-ctl -d 0 --set-ctrl=saturation=50"
res = os.system(cmd)
print(f'{cmd} -> ', res)

@server.route("/video_feed")
def video_feed():
   return Response(open_cv_car.generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.layout = html.Div(style={'backgroundColor': '#292929'}, children=[
    dbc.Container([
        # dbc.Row(dbc.Col(html.H1("Livestream", className="text-center mt-4", style={'color': 'white'}))),
        # dbc.Row(dbc.Col(html.P("Status:", id="output_status", className="text-center", style={'color': 'white'}))),
        # dbc.Row(dbc.Col(html.P("Calculation Method:", id="output_status2", className="text-center", style={'color': 'white'}))),
        dbc.Row([
            dbc.Col([
                html.H1("", className="text-start", style={'color': 'white'}),
                dbc.Button('Start Car', id='b-start', n_clicks=0, color="success", className="me-2", style={'fontSize': '20px'}),
                dbc.Button('Stop Car', id='b-stop', n_clicks=0, color="danger", style={'fontSize': '20px'}),
                html.Div(id='mode-container', style={'color': 'white', 'fontSize': '20px'})
            ], width=3),
            dbc.Col([
               html.H1("Livestream", className="text-start", style={'color': 'white'}),
               html.P("Status:", id="output_status", className="text-start", style={'color': 'white'}),
               html.P("Calculation Method:", id="output_calc_method", className="text-start", style={'color': 'white'})
            ], width=6),
        ]),
        dbc.Row([
            dbc.Col([
                html.Hr(style={'color':'white', 'border-style':'solid'}),
                html.P("Hue", style={'color': 'white'}),
                dcc.RangeSlider(id="range-slider-h1", min=0, max=180, value=[proc.lower_hue, proc.upper_hue], marks={i: str(i) for i in range(0, 181, 20)}, step=1, updatemode='drag', tooltip={"placement": "bottom", "always_visible": True}),
                html.P("Saturation", style={'color': 'white'}),
                dcc.RangeSlider(id="range-slider-s1", min=0, max=255, value=[proc.lower_saturation, proc.upper_saturation], marks={i: str(i) for i in range(0, 256, 25)}, step=1, updatemode='drag', tooltip={"placement": "bottom", "always_visible": True}),
                html.P("Value", style={'color': 'white'}),
                dcc.RangeSlider(id="range-slider-v1", min=0, max=255, value=[proc.lower_value, proc.upper_value], marks={i: str(i) for i in range(0, 256, 25)}, step=1, updatemode='drag', tooltip={"placement": "bottom", "always_visible": True}),
                html.Hr(style={'color':'white', 'border-style':'solid'}),
                html.P("Steering angle calculation method", style={'color': 'white'}),
                # dcc.Slider(min=1, max=4, step=1, value=proc.calc_angle_method, id='calc-angle-slider', marks={i: str(i) for i in range(1, 4)}, tooltip={"placement": "bottom", "always_visible": True}),
                dcc.RadioItems(
                    id="radioitems_calc_method",
                    # style={'color': 'white', "padding": "10px", "max-width": "800px", "margin": "auto"},
                    labelStyle={"display": "flex", "align-items": "center"},
                    options=[
                        {"label": html.Div([' Method 1'], style={'color': 'LightBlue'}), "value": 1},
                        {"label": html.Div([' Method 2'], style={'color': 'LightBlue'}), "value": 2},
                        {"label": html.Div([' Method 3'], style={'color': 'LightBlue'}), "value": 3},
                        {"label": html.Div([' Average'], style={'color': 'LightGreen'}), "value": 4},
                        {"label": html.Div([' Neural Network 1'], style={'color': 'Gold'}), "value": 5},
                        {"label": html.Div([' Neural Network 2'], style={'color': 'Gold'}), "value": 6},
                        {"label": html.Div([' Neural Network 3'], style={'color': 'Gold'}), "value": 7},
                    ],
                    value = proc.calc_angle_method,
                ),
                html.Hr(style={'color':'white', 'border-style':'solid'}),
            ], width=3),
            dbc.Col(html.Div([html.Img(src="/video_feed", id="videofeed", style={'width':'800px'})]), width=6)
        ]),
        dbc.Row(dbc.Col(html.A("Help on HSV-Color-Modell", href='https://de.wikipedia.org/wiki/HSV-Farbraum', target="_blank", className="text-center mt-4", style={'color': 'white'}))),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
    ])
])


# callback hat immer einen Output und einen Input
# beim Starten des Autos muss hier etwas getrickst werden
@app.callback(
    # Was soll beim Output verändert werden
    Output("output_status", "children"),
    # Was soll vom Input verwendet werden?
    Input("range-slider-h1", "value"),
    Input("range-slider-s1", "value"),
    Input("range-slider-v1", "value"),
    # State: Nur Werte von SLider2 verwendet
    # State("range-slider-2", "value") 
)
# was soll passieren
def update_paragraph(range_slider_h1, range_slider_s1, range_slider_v1):
    hue1_lower, hue1_upper = range_slider_h1
    sat1_lower, sat1_upper = range_slider_s1
    val1_lower, val1_upper = range_slider_v1
    proc.lower_hue = hue1_lower
    proc.upper_hue = hue1_upper
    proc.lower_saturation = sat1_lower
    proc.upper_saturation = sat1_upper
    proc.lower_value = val1_lower
    proc.upper_value = val1_upper

    return f"Use HSV-Ranges: HUE({hue1_lower} - {hue1_upper}), SAT({sat1_lower} - {sat1_upper}), VAL({val1_lower} - {val1_upper})"


# callback hat immer einen Output und einen Input
# beim Starten des Autos muss hier etwas getrickst werden
@app.callback(
    Output("output_calc_method", "children"),
    Input("radioitems_calc_method", "value"),
)
def update_method(radioitems_calc_method):
    proc.calc_angle_method = radioitems_calc_method
    return f"Use steering angle calculation method: {proc.calc_angle_method}"
    
@app.callback(
    Output("mode-container", "children"), 
    Input("b-stop", "n_clicks"), 
    Input("b-start", "n_clicks"), 
    prevent_initial_callbacks=True
)
def run_drive_modes(btnstop, bdm1):
    msg_dm = "Car not started yet"
    if "b-stop" == ctx.triggered_id:
        msg_dm = "Car Stops"
        open_cv_car.finished = True
        open_cv_car.stop_driving()
    elif "b-start" == ctx.triggered_id:
        msg_dm = "Car Starts"
        open_cv_car.finished = False
        open_cv_car.start_driving()
    return msg_dm

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=False, port=8050)
