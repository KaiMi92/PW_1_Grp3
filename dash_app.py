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



# Reine Optik
app.layout = html.Div(style={'backgroundColor': '#000000'}, children=[
    dbc.Container([
        dbc.Row(dbc.Col(html.H1("Livestream", className="text-center mt-4", style={'color': 'white'}))),
        dbc.Row(dbc.Col(html.P("Status:", id="test-output", className="text-center", style={'color': 'white'}))),
        dbc.Row(dbc.Col(html.P("Calculation Method:", id="test-output2", className="text-center", style={'color': 'white'}))),
        dbc.Row(dbc.Col(html.P("Simulation:", id="output-simulation", className="text-center", style={'color': 'white'}))),
        dbc.Row([
            dbc.Col([
                html.P("Hue", style={'color': 'white'}),
                dcc.RangeSlider(id="range-slider-h1", min=0, max=180, value=[proc.lower_hue, proc.upper_hue], marks={i: str(i) for i in range(0, 181, 20)}, step=1, updatemode='drag', tooltip={"placement": "bottom", "always_visible": True}),
                html.P("Saturation", style={'color': 'white'}),
                dcc.RangeSlider(id="range-slider-s1", min=0, max=255, value=[proc.lower_saturation, proc.upper_saturation], marks={i: str(i) for i in range(0, 256, 25)}, step=1, updatemode='drag', tooltip={"placement": "bottom", "always_visible": True}),
                html.P("Value", style={'color': 'white'}),
                dcc.RangeSlider(id="range-slider-v1", min=0, max=255, value=[proc.lower_value, proc.upper_value], marks={i: str(i) for i in range(0, 256, 25)}, step=1, updatemode='drag', tooltip={"placement": "bottom", "always_visible": True}),
                html.Hr(style={'borderColor': 'white'}),
                html.P("Steering angle calculation method", style={'color': 'white'}),
                dcc.Slider(min=1, max=3, step=1, value=proc.calc_angle_method, id='calc-angle-slider', marks={i: str(i) for i in range(1, 4)}, tooltip={"placement": "bottom", "always_visible": True}),
                html.Hr(style={'borderColor': 'white'}),
                html.P("Use Average", style={'color': 'white'}),
                dcc.Slider(min=0, max=1, step=1, value=proc.use_average, id='simulation-slider', marks={0: 'No', 1: 'Yes'}, tooltip={"placement": "bottom", "always_visible": True}),
                html.Hr(style={'borderColor': 'white'}),
                dbc.Button('Start Car', id='b-start', n_clicks=0, color="success", className="me-2", style={'fontSize': '20px'}),
                dbc.Button('Stop Car', id='b-stop', n_clicks=0, color="danger", style={'fontSize': '20px'}),
                html.Div(id='mode-container', style={'color': 'white', 'fontSize': '20px'})
            ], width=6),
            dbc.Col(html.Div([html.Img(src="/video_feed", id="videofeed", style={'width':'800px'})]), width=6)
        ]),
        dbc.Row(dbc.Col(html.A("Help on HSV-Color-Modell", href='https://de.wikipedia.org/wiki/HSV-Farbraum', target="_blank", className="text-center mt-4", style={'color': 'white'})))
    ])
])
# callback hat immer einen Output und einen Input
# beim Starten des Autos muss hier etwas getrickst werden
@app.callback(
    # Was soll beim Output verändert werden
    Output("test-output", "children"),
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

    return f"Used HSV-Ranges: HUE({hue1_lower} - {hue1_upper}), SAT({sat1_lower} - {sat1_upper}), VAL({val1_lower} - {val1_upper})"



# callback hat immer einen Output und einen Input
# beim Starten des Autos muss hier etwas getrickst werden
@app.callback(
    Output("test-output2", "children"),
    Input("calc-angle-slider", "value"),
)
def update_method(method_slider):
    proc.calc_angle_method = method_slider
    return f"Used steering-angle-calculation-method: {proc.calc_angle_method}"

# callback hat immer einen Output und einen Input
# beim Starten des Autos muss hier etwas getrickst werden
@app.callback(
    Output("output-simulation", "children"),
    Input("simulation-slider", "value"),
)
def update_method(sim_slider):
    if sim_slider:
        proc.use_average = True
        return "Simulation: YES"
    else:
        proc.use_average = False
        return "Simulation: NO"
    
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
        #script_path = 'driving_mode_1.py'
        #exec(open(script_path).read())  
    return msg_dm

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=False, port=8050)
