import os
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from cvasl_gui.app import app
from cvasl_gui import data_store


def create_directory_input():
    return html.Div([
        html.Div(id='file-list-container', children=[dcc.Checklist(
            id='file-list',
            options=[],  # populated via callback
            labelStyle={'display': 'block'},
            inputStyle={'marginRight': '5px'},
            inline=True
        )]),
        html.Div(id='file-contents-container')
    ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '10px'})


FIXED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data'))  # adjust as needed

@app.callback(
    Output('file-list', 'options'),
    Input('file-list', 'id')  # dummy trigger on page load
)
def populate_file_list(_):
    if not os.path.isdir(FIXED_DIR):
        return [{'label': 'Directory not found', 'value': '', 'disabled': True}]
    
    files = sorted([
        f for f in os.listdir(FIXED_DIR)
        if os.path.isfile(os.path.join(FIXED_DIR, f)) and f.endswith('.csv')
    ])
    return [{'label': f, 'value': f} for f in files]



@app.callback(
    Output('file-contents-container', 'children'),
    Input('file-list', 'value')  # triggered on checklist change
)
def load_selected_files(selected_files):
    if not selected_files:
        raise PreventUpdate

    dfs = []
    input_files = []
    errors = []
    for fname in selected_files:
        file_path = os.path.join(FIXED_DIR, fname)
        input_files.append(file_path)
        try:
            df = pd.read_csv(file_path)
            dfs.append(df)
        except Exception as e:
            errors.append(f"Error loading {fname}: {e}")

    data_store.input_files = input_files
    if dfs:
        data_store.all_data = pd.concat(dfs, ignore_index=True)
    else:
        data_store.all_data = pd.DataFrame()  # empty fallback

    return html.Div([
        html.Div(f"Loaded files: {', '.join(selected_files)}"),
        html.Div(f"{len(data_store.all_data)} rows loaded"),
        *([html.Div(e, style={'color': 'red'}) for e in errors] if errors else [])
    ])