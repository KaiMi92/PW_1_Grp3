from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from flask import Flask, Response
from software.basisklassen_cam import Camera
import cv2
import numpy as np
from processor import Processor

external_stylesheets = [dbc.themes.BOOTSTRAP]
server = Flask(__name__)

print("Start Init...")
app = Dash(__name__, external_stylesheets=external_stylesheets, server=server)
cam = Camera() # (height=200, width=320)
proc = Processor()
print("End Init")


def generate_stream(camera_instance):
    while True:
        frame = camera_instance.get_frame()
        filtered = proc.filter_color(frame)
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # canny = cv2.Canny(gray, 100, 200)
        stacked = np.hstack([frame, filtered]) # canny, filtered])
        _, x = cv2.imencode(".jpeg", stacked)
        x_bytes = x.tobytes()

        x_string = (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + x_bytes + b'\r\n\r\n')
        
        yield x_string
        

@server.route("/video_feed")
def video_feed():
   return Response(generate_stream(cam), mimetype='multipart/x-mixed-replace; boundary=frame')


# Reine Optik
app.layout = html.Div(children=[
    html.H1("Livestream"),
    html.P("Status:", id="test-output"),
    html.P("Hue"),
    dcc.RangeSlider(id="range-slider-h1", min=0, max=180, value=[proc.lower_hue,proc.upper_hue]),
    html.P("Saturation"),
    dcc.RangeSlider(id="range-slider-s1", min=0, max=180, value=[proc.lower_saturation, proc.upper_saturation]),
    html.P("Value"),
    dcc.RangeSlider(id="range-slider-v1", min=0, max=180, value=[proc.lower_value, proc.upper_value]),
    dbc.Row([
        dbc.Col( html.Div([html.Img(src="/video_feed", id="videofeed", style={'height':'500px'})])),       
        ]),
    html.A("Help on HSV-Color-Modell", href='https://de.wikipedia.org/wiki/HSV-Farbraum', target="_blank")
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

    return f"Hier der RS-Werte ({hue1_lower} - {hue1_upper}), ({sat1_lower} - {sat1_upper}), ({val1_lower} - {val1_upper})"


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=False, port=8050)
