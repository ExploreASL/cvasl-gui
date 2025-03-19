import dash
from dash import dcc, html, Input, Output, State
import os
import json
import threading

from cvasl_gui.app import app
from cvasl_gui.components.job_list import run_job
from cvasl_gui import data_store


# Folder where job output files are stored
OUTPUT_FOLDER = "jobs"
FEATURES_FILE = os.path.join(OUTPUT_FOLDER, "selected_features.json")


def get_dataframe_columns():
    df = data_store.all_data
    if df is None:
        return []
    return df.columns


def create_tab_harmonization():
    return html.Div([
        html.H3("Features to Harmonize"),
        
        # Feature selection dropdown
        dcc.Dropdown(
            id="feature-dropdown",
            options=[{"label": col, "value": col} for col in get_dataframe_columns()],
            multi=True,
            placeholder="Select features...",
        ),

        html.Button("Start Job", id="start-button", n_clicks=0),

        html.Div(id="job-status2"),
    ])

@app.callback(
    Output("job-status2", "children"),
    Input("start-button", "n_clicks"),
    State("feature-dropdown", "value"),
    prevent_initial_call=True
)
def start_job(n_clicks, selected_features):
    if not selected_features:
        return "No features selected. Please choose at least one feature."

    # # Start job in a separate thread
    # threading.Thread(target=run_job, daemon=True).start()

    job_arguments = {
        "input_paths": ["/Users/peter/repos/brainage/data-workshop/TestingData_Site1_fake.csv"],
        "harmonization_features": selected_features,
        "covariate_features": ["Age","Sex","Site"]
    }
    run_job(job_arguments)

    return f"Job started with features: {', '.join(selected_features)}"
