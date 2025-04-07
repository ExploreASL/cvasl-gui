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
WORKING_DIR = os.getenv("CVASL_WORKING_DIRECTORY", ".")
INPUT_DIR = os.path.join(WORKING_DIR, 'data')
JOBS_DIR = os.path.join(WORKING_DIR, 'jobs')


def get_dataframe_columns():
    df = data_store.all_data
    if df is None:
        return []
    return df.columns


def create_prediction_parameters():
    return [
        # Row for algorithm selection
        dbc.Row([
            dbc.Col(html.Label("Model:", style={"marginTop": "6px"}), width=3),
            dbc.Col(
                dcc.Dropdown(
                    id="model-dropdown",
                    options=[
                        {"label": "ExtraTrees", "value": "extratrees"},
                    ],
                    value="extratrees",
                    clearable=False,
                ),
            ),
        ], className="mb-3"),

        # Row for main feature selection
        dbc.Row([
            dbc.Col(html.Label("Features:", style={"marginTop": "6px"}), width=3),
            dbc.Col(
                dcc.Dropdown(
                    id="prediction-features-dropdown",
                    options=[{"label": col, "value": col} for col in get_dataframe_columns()],
                    multi=True,
                    placeholder="Select features...",
                ),
            ),
        ], className="mb-3"),

        html.Button("Estimate", id="prediction-start-button", n_clicks=0)
    ]


def create_tab_prediction():
    return html.Div([
        dbc.Accordion([
            dbc.AccordionItem([create_directory_input('prediction')],
                title="Select new input data"),
            dbc.AccordionItem([create_data_table('prediction')],
                title="Inspect data"),
            # dbc.AccordionItem([create_feature_compare()],
            #     title="Feature comparison"),
            dbc.AccordionItem(create_prediction_parameters(),
                title="Prediction"),
            # dbc.AccordionItem([create_job_list()],
            #     title="Runs")
        ], always_open=True)
    ])


# Populate dropdown with columns from the data table
@app.callback(
    Output("prediction-features-dropdown", "options"),
    Input({'type': 'data-table', 'index': 'prediction'}, "data"),
    prevent_initial_call=True
)
def update_feature_dropdown(data):
    return [{"label": col, "value": col} for col in data[0].keys()]


@app.callback(
    Input("prediction-start-button", "n_clicks"),
    State("prediction-features-dropdown", "value"),
    State("discrete-covariate-dropdown", "value"),
    State("continuous-covariate-dropdown", "value"),
    State("site-indicator-dropdown", "value"),
    prevent_initial_call=True
)
def start_job(n_clicks, selected_features, discrete_covariate_features, continuous_covariate_features, site_indicator):
    if not selected_features:
        return dash.no_update

    job_arguments = {
        "input_paths": data_store.input_files,
        "input_sites": data_store.input_sites,
        "harmonization_features": selected_features,
        "discrete_covariate_features": discrete_covariate_features,
        "continuous_covariate_features": continuous_covariate_features,
        "site_indicator": site_indicator
    }

    # Start job in a separate thread
    threading.Thread(target=run_job, args=(job_arguments,), daemon=True).start()

    return dash.no_update
