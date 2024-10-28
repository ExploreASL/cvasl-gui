from dash import html
from components.directory_input import create_directory_input

def create_tab_input_selection():
    return html.Div([
        html.H3("Select Input:"),
        create_directory_input(),
    ])
