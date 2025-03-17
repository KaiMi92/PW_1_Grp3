from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Hallo Phase2"), 
    html.P("Test", id="test-output"),
    dcc.RangeSlider(id="range-slider-1", min=0, max=180, value=[40,90]),
    dcc.RangeSlider(id="range-slider-2", min=0, max=180, value=[40,90])
    ])

# callback hat immer einen Output und einen Input
# beim Starten des Autos muss hier etwas getrckst werden
@app.callback(
    # Was soll beim Output verändert werden
    Output("test-output", "children"),
    # Was soll vom Input verwendet werden?
    Input("range-slider-1", "value"),
    # State: Nur Werte von SLider2 verwendet
    State("range-slider-2", "value") 
)
# was soll passieren
def update_paragraph(range_slider_1):
    print(range_slider_1)
    erster, zweiter = range_slider_1
    erster2, zweiter2 = range_slider_2
    return f"Hier der RS-Wert {range_slider_1}: {erster} - {zweiter}, Hier der RS-Wert {range_slider_2}: {erster2} - {zweiter2}"


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
