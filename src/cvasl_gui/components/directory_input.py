import json
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
        html.Div(id='harmonized-file-list-container', children=[dcc.Checklist(
            id='harmonized-file-list',
            options=[],  # populated via callback
            labelStyle={'display': 'block'},
            inputStyle={'marginRight': '5px'},
            inline=True
        )]),
        html.Div(id='file-contents-container'),
    ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '10px'})


FIXED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data'))
JOBS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'jobs'))

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
    Output('harmonized-file-list', 'options'),
    Input('harmonized-file-list', 'id')  # dummy trigger on page load
)
def populate_harmonized_file_list(_):
    if not os.path.isdir(JOBS_DIR):
        return [{'label': 'Directory not found', 'value': '', 'disabled': True}]
    
    job_dirs = sorted(os.listdir(JOBS_DIR), reverse=True)
    all_files = []
    for job_dir in job_dirs:
        job_details_file = os.path.join(JOBS_DIR, job_dir, "job_details.json")
        job_arguments_file = os.path.join(JOBS_DIR, job_dir, "job_arguments.json")
        output_dir = os.path.join(JOBS_DIR, job_dir, 'output')
        if os.path.exists(output_dir):
            output_files = [ os.path.join(job_dir, f) for f in os.listdir(output_dir)
                            if os.path.isfile(os.path.join(output_dir, f)) and f.endswith('.csv') ]
            all_files.extend(output_files)

    return [{'label': f, 'value': f} for f in all_files]
    
        # if os.path.exists(job_details_file):
        #     # Load the job details
        #     with open(job_details_file) as f:
        #         details = json.load(f)

        #     # Load current status
        #     status_file = os.path.join(JOBS_DIR, job_dir, "job_status")
        #     if os.path.exists(status_file):
        #         with open(status_file) as f:
        #             details["status"] = f.read()

        #     # Check if process is still running
        #     process_id = details.get("process")
        #     details["running"] = is_process_running(process_id)

        #     # Load job arguments
        #     if os.path.exists(job_arguments_file):
        #         with open(job_arguments_file) as f:
        #             job_arguments = json.load(f)
        #             details["arguments"] = job_arguments

        #     job_data.append(details)


@app.callback(
    Output('file-contents-container', 'children'),
    Input('file-list', 'value'),
    Input('harmonized-file-list', 'value')
)
def load_all_selected_files(normal_files, harmonized_files):
    if not normal_files and not harmonized_files:
        raise PreventUpdate

    normal_dfs = []
    harmonized_dfs = []
    normal_file_rows = []
    harmonized_file_rows = []
    errors = []

    # Load normal files
    input_files = []
    input_sites = []
    if normal_files:
        for fname in normal_files:
            file_path = os.path.join(FIXED_DIR, fname)
            input_files.append(file_path)
            try:
                df = pd.read_csv(file_path)
                # Get the site from the dataframe
                site_col = [col for col in df.columns if col.lower() == 'site']
                if site_col:
                    input_sites.append(int(df[site_col[0]].iloc[0]))
                else:
                    input_sites.append(0) #TODO: how to make sure this is sensible?
                df['harmonized'] = False
                normal_dfs.append(df)
                normal_file_rows.append(f"{fname} ({len(df)})")
            except Exception as e:
                errors.append(f"Error loading {fname}: {e}")
        data_store.input_files = input_files
        data_store.input_sites = input_sites
        data_store.input_data = pd.concat(normal_dfs, ignore_index=True) if normal_dfs else pd.DataFrame()

    # Load harmonized files
    if harmonized_files:
        for fname in harmonized_files:
            split = fname.split(os.sep)
            file_path = os.path.join(JOBS_DIR, split[0], 'output', split[1])
            try:
                df = pd.read_csv(file_path)
                df['harmonized'] = True
                harmonized_dfs.append(df)
                harmonized_file_rows.append(f"{fname} ({len(df)})")
            except Exception as e:
                errors.append(f"Error loading {fname}: {e}")
        data_store.harmonized_data = pd.concat(harmonized_dfs, ignore_index=True) if harmonized_dfs else pd.DataFrame()

    # Combine all
    combined_dfs = normal_dfs + harmonized_dfs
    data_store.all_data = pd.concat(combined_dfs, ignore_index=True) if combined_dfs else pd.DataFrame()

    return html.Div([
        html.Div(f"Loaded normal files: {', '.join(normal_file_rows) if normal_file_rows else 'None'}"),
        html.Div(f"Loaded harmonized files: {', '.join(harmonized_file_rows) if harmonized_file_rows else 'None'}"),
        html.Div(f"{len(data_store.all_data)} total rows loaded"),
        *([html.Div(e, style={'color': 'red'}) for e in errors] if errors else [])
    ])
