from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from flask import Flask, Response
from software.basisklassen_cam import Camera
import cv2
import numpy as np

external_stylesheets = [dbc.themes.BOOTSTRAP]
server = Flask(__name__)

app = Dash(__name__, external_stylesheets=external_stylesheets, server=server)

cam = Camera()


def generate_stream(camera_instance):
    while True:
        frame = camera_instance.get_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 100, 200)
        stacked = np.hstack([gray, canny])
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
    dbc.Row([
        dbc.Col( html.Div([html.Img(src="/video_feed", id="videofeed", style={'height':'500px'})])),
       
        ])
    ])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=False, port=8050)
