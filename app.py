from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
from basecar import Auto
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

auto = Auto()

app.layout = html.Div