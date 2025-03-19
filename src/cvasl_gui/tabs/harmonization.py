import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import os
import json
import threading

from cvasl_gui.app import app
from cvasl_gui.components.job_list import run_job
from cvasl_gui import data_store
from cvasl_gui.components.directory_input import create_directory_input
from cvasl_gui.components.data_table import create_data_table
from cvasl_gui.components.feature_compare import create_feature_compare
from cvasl_gui.components.job_list import create_job_list

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
        dbc.Accordion([
            dbc.AccordionItem([create_directory_input()],
                title="Select new input data"),
            dbc.AccordionItem([create_data_table()],
                title="Inspect data"),
            dbc.AccordionItem([create_feature_compare()],
                title="Feature comparison"),
            dbc.AccordionItem([
                html.H3("Features to Harmonize"),
        
                # Feature selection dropdown
                dcc.Dropdown(
                    id="feature-dropdown",
                    options=[{"label": col, "value": col} for col in get_dataframe_columns()],
                    multi=True,
                    placeholder="Select features...",
                ),

                html.Button("Start Job", id="start-button", n_clicks=0),
            ], title="Harmonization"),
            dbc.AccordionItem([create_job_list()],
                title="Runs")
        ], always_open=True)
    ])

@app.callback(
    Output("feature-dropdown", "options"),
    Input("data-table", "data"),
    prevent_initial_call=True
)
def update_feature_dropdown(data):
    return [{"label": col, "value": col} for col in data[0].keys()]


@app.callback(
    Input("start-button", "n_clicks"),
    State("feature-dropdown", "value"),
    prevent_initial_call=True
)
def start_job(n_clicks, selected_features):
    if not selected_features:
        return dash.no_update

    # # Start job in a separate thread
    # threading.Thread(target=run_job, daemon=True).start()

    job_arguments = {
        "input_paths": ["/Users/peter/repos/brainage/data-workshop/TestingData_Site1_fake.csv"],
        "harmonization_features": selected_features,
        "covariate_features": ["Age","Sex","Site"]
    }
    run_job(job_arguments)

    return dash.no_update
