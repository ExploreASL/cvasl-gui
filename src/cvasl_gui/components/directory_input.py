import os
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from cvasl_gui.app import app
from cvasl_gui import data_store


def create_directory_input():
    return html.Div([
        html.Div(id='file-list-container', children=[dcc.RadioItems(
            id='file-list',
            options=[],  # populated via callback
            labelStyle={'display': 'block'},
            style={'overflowY': 'scroll', 'height': '200px'}
        )]),
        html.Div([html.Button('Load Selected File', id='load-button', className='button button-primary', n_clicks=0)]),
        html.Div(id='file-contents-container')
    ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '10px'})


FIXED_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data')  # change to your actual folder name

@app.callback(
    Output('file-list', 'options'),
    Input('file-list', 'id')  # dummy input that fires once when layout is ready
)
def populate_file_list(_):
    if not os.path.isdir(FIXED_DIR):
        return [{'label': 'Directory not found', 'value': '', 'disabled': True}]
    
    files = os.listdir(FIXED_DIR)
    return [{'label': f, 'value': f} for f in files if os.path.isfile(os.path.join(FIXED_DIR, f))]


@app.callback(
    Output('file-contents-container', 'children'),
    Input('load-button', 'n_clicks'),
    State('file-list', 'value')
)
def load_file(n_clicks, selected_file):
    if n_clicks == 0 or not selected_file:
        raise PreventUpdate

    file_path = os.path.join(FIXED_DIR, selected_file)
    try:
        data_store.all_data = pd.read_csv(file_path)
    except Exception as e:
        return html.Div([f"Error loading file: {e}"], style={'color': 'red'})

    return html.Div([html.Span(f"Loaded {selected_file}")])
