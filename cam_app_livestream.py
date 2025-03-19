from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from flask import Flask, Response
from software.basisklassen_cam import Camera
import cv2
import numpy as np
from processor import Processor
import math
import time
import calc_steering_angle_1
import calc_steering_angle_2
import calc_steering_angle_3
import calc_steering_angle_4
import calc_steering_angle_5

methodDictionary = {1: calc_steering_angle_1.calculate_steering_angle, 
                    2: calc_steering_angle_2.calculate_steering_angle,
                    3: calc_steering_angle_3.calculate_steering_angle,
                    4: calc_steering_angle_4.calculate_steering_angle,
                    5: calc_steering_angle_5.calculate_steering_angle}
external_stylesheets = [dbc.themes.BOOTSTRAP]
server = Flask(__name__)

print("Start Init...")
app = Dash(__name__, external_stylesheets=external_stylesheets, server=server)
cam = Camera() # (height=200, width=320)
proc = Processor()
print("End Init")

prev_frame_time = time.time()
new_frame_time = time.time()

def draw_fps(image):
    global prev_frame_time
    global new_frame_time

	# Calculating True FPS
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    text = str(round(fps,1)) + " fps"
    position  =(10,40)
    font = cv2.FONT_HERSHEY_SIMPLEX 
    fontscale = 0.5
    color = (0,0,255) # Hier im BGR-Modus + Werte vom Type 'unit8'
    thickness = 2
    linestyle = 1
    img_text = cv2.putText(image, text, position,font, fontscale, color, thickness, linestyle)

def draw_steering_angle(image, steering_angle):
    height, width, channels = image.shape
    angle = steering_angle - 90

    x = height * math.tan(math.radians(angle))
    x45 = height * math.tan(math.radians(45))
    x135 = height * math.tan(math.radians(135))

    middle = int((width - 1) / 2)
    x1 = middle
    y1 = height - 1
    x2 = middle + int(x)
    y2 = 0
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 3)
    cv2.line(image, (x1, y1), (middle + int(x45), y2), (255, 255, 255), 2)
    cv2.line(image, (x1, y1), (middle + int(x135), y2), (255, 255, 255), 2)
    # print(f'steering_angle = {steering_angle}, angle = {angle}, x = {x}, P1({x1}|{y1}), P2({x2}|{y2}) ')


def generate_stream(camera_instance):
    while True:
        print("============================================")
        frame = camera_instance.get_frame()
        line_filter, lines = proc.line_filter(frame)
        # steering_angle = calc_steering_angle.calculate_steering_angle(line_filter, lines)   # einzeichnen im bild?

        print(f"Verwende Methode {proc.calc_angle_method}")
        method = methodDictionary[proc.calc_angle_method]
        steering_angle = method(line_filter, lines)   # einzeichnen im bild?

        # print (f"{line_filter.shape}: Draw angle {steering_angle} to ({x1}|{y1}), ({x2}|{y2})")

        draw_steering_angle(line_filter, steering_angle)
        draw_fps(line_filter)

        # filtered = proc.filter_color(frame)
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # canny = cv2.Canny(gray, 100, 200)
        stacked = np.hstack([line_filter]) # canny, filtered])
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
    html.P("Calculation Method:", id="test-output2"),
    html.P("Simulation:", id="output-simulation"),
    html.P("Hue"),
    dcc.RangeSlider(id="range-slider-h1", min=0, max=180, value=[proc.lower_hue,proc.upper_hue]),
    html.P("Saturation"),
    dcc.RangeSlider(id="range-slider-s1", min=0, max=255, value=[proc.lower_saturation, proc.upper_saturation]),
    html.P("Value"),
    dcc.RangeSlider(id="range-slider-v1", min=0, max=255, value=[proc.lower_value, proc.upper_value]),
    html.P("Steering angle calcualtion method"),
    dcc.Slider(min=1, max=5, step=1, value = proc.calc_angle_method, id='calc-angle-slider'),
    html.P("Simulation"),
    dcc.Slider(min=0, max=1, step=1, value = proc.simulation, id='simulation-slider'),
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



# callback hat immer einen Output und einen Input
# beim Starten des Autos muss hier etwas getrickst werden
@app.callback(
    Output("test-output2", "children"),
    Input("calc-angle-slider", "value"),
)
def update_method(method_slider):
    proc.calc_angle_method = method_slider
    return f"Verwende Methode {proc.calc_angle_method}"

# callback hat immer einen Output und einen Input
# beim Starten des Autos muss hier etwas getrickst werden
@app.callback(
    Output("output-simulation", "children"),
    Input("simulation-slider", "value"),
)
def update_method(sim_slider):
    if sim_slider:
        proc.simulation = True
        return "YES"
    else:
        proc.simulation = False
        return "NO"


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=False, port=8050)
