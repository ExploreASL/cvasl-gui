import os
import dash
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dependencies import ALL
import pandas as pd
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
        html.Div(id='file-list-container'),  # Display files in directory
        html.Div(id='file-contents-container')  # Display contents of file
    ])

@app.callback(
    Output('file-list-container', 'children'),
    Input('scan-button', 'n_clicks'),
    State('directory-path-input', 'value')
)
def scan_directory(n_clicks, directory_path):
    if not n_clicks or not directory_path:
        raise PreventUpdate

    # Check if the directory exists
    if not os.path.isdir(directory_path):
        return html.Div(["Directory not found. Please enter a valid path."], style={'color': 'red'})

    # List files in the directory
    files = os.listdir(directory_path)

    file_list = html.Ul([
        html.Li([
            html.Div(file),
            html.Button('Open', id={'type': 'open-button', 'index': index})  # Pattern-matching ID
        ]) for index, file in enumerate(files)
    ])

    return html.Div([
        html.H5(f"Files in {directory_path}:"),
        file_list
    ])


# Callback to open a file
@app.callback(
    Output('file-contents-container', 'children'),
    Input({'type': 'open-button', 'index': ALL}, 'n_clicks'),
    State('directory-path-input', 'value')
)
def open_file(n_clicks, directory_path):
    # Use callback_context to determine which button triggered the callback
    ctx = dash.callback_context
    if not ctx.triggered or not any(n_clicks):
        raise PreventUpdate

    # Identify the button clicked by extracting its index from ctx
    clicked_button = ctx.triggered[0]['prop_id']
    print(clicked_button)
    index = int(eval(clicked_button.split('.')[0])['index'])

    # Retrieve the list of files and select the file based on the index
    files = os.listdir(directory_path)
    file_name = files[index]

    # Open and read the file contents
    file_path = os.path.join(directory_path, file_name)
    data_store.all_data = pd.read_csv(file_path)

    return html.Div([
        html.H5(f"Loaded {file_name}")
    ])
