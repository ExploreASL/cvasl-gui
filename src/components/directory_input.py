import os
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
import data_store

def create_directory_input():
    return html.Div([
        html.Label("Enter Directory Path:"),
        dcc.Input(
            id='directory-path-input',
            type='text',
            placeholder="Enter directory path",
            style={'width': '60%'}
        ),
        html.Button('Scan Directory', id='scan-button'),
        html.Div(id='file-list-container')  # Display files in directory
    ])


# Callback to initialize the directory input with the global variable's value
@app.callback(
    Output('directory-path-input', 'value'),
    Input('scan-button', 'n_clicks')  # Triggered on load or initial interaction
)
def initialize_directory_input(n_clicks):
    # Set the directory input field to the current value of data_store.selected_directory
    return data_store.selected_directory


@app.callback(
    Output('file-list-container', 'children'),
    Input('scan-button', 'n_clicks'),
    State('directory-path-input', 'value')
)
def scan_directory(n_clicks, directory_path):
    if not n_clicks or not directory_path:
        raise PreventUpdate
    
    data_store.selected_directory = directory_path

    # Check if the directory exists
    if not os.path.isdir(directory_path):
        return html.Div(["Directory not found. Please enter a valid path."], style={'color': 'red'})

    # List files in the directory
    files = os.listdir(directory_path)
    file_list = html.Ul([html.Li(file) for file in files])

    return html.Div([
        html.H5(f"Files in {directory_path}:"),
        file_list
    ])
