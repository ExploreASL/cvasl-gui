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


def create_harmonization_parameters():
    return [
        # Row for algorithm selection
        dbc.Row([
            dbc.Col(html.Label("Algorithm:", style={"marginTop": "6px"}), width=3),
            dbc.Col(
                dcc.Dropdown(
                    id="algorithm-dropdown",
                    options=[
                        {"label": "NeuroCombat", "value": "neurocombat"},
                    ],
                    value="neurocombat",
                    clearable=False,
                ),
            ),
        ], className="mb-3"),

        # Row for main feature selection
        dbc.Row([
            dbc.Col(html.Label("Features:", style={"marginTop": "6px"}), width=3),
            dbc.Col(
                dcc.Dropdown(
                    id="feature-dropdown",
                    options=[{"label": col, "value": col} for col in get_dataframe_columns()],
                    multi=True,
                    placeholder="Select features...",
                ),
            ),
        ], className="mb-3"),

        # Row for discrete covariate features
        dbc.Row([
            dbc.Col(html.Label("Discrete covariate features:", style={"marginTop": "6px"}), width=3),
            dbc.Col(
                dcc.Dropdown(
                    id="discrete-covariate-dropdown",
                    options=[{"label": col, "value": col} for col in get_dataframe_columns()],
                    multi=True,
                    placeholder="Select discrete covariates...",
                ),
            ),
        ], className="mb-3"),

        # Row for continuous covariate features
        dbc.Row([
            dbc.Col(html.Label("Continuous covariate features:", style={"marginTop": "6px"}), width=3),
            dbc.Col(
                dcc.Dropdown(
                    id="continuous-covariate-dropdown",
                    options=[{"label": col, "value": col} for col in get_dataframe_columns()],
                    multi=True,
                    placeholder="Select continuous covariates...",
                ),
            ),
        ], className="mb-3"),

        # Row for site indicator
        dbc.Row([
            dbc.Col(html.Label("Site indicator:", style={"marginTop": "6px"}), width=3),
            dbc.Col(
                dcc.Dropdown(
                    id="site-indicator-dropdown",
                    options=[{"label": col, "value": col} for col in get_dataframe_columns()],
                    multi=False,
                    placeholder="Select site indicator...",
                ),
            ),
        ], className="mb-3"),

        html.Button("Start Job", id="start-button", n_clicks=0)
    ]


def create_tab_harmonization():
    return html.Div([
        dbc.Accordion([
            dbc.AccordionItem([create_directory_input()],
                title="Select new input data"),
            dbc.AccordionItem([create_data_table()],
                title="Inspect data"),
            dbc.AccordionItem([create_feature_compare()],
                title="Feature comparison"),
            dbc.AccordionItem(create_harmonization_parameters(),
                title="Harmonization"),
            dbc.AccordionItem([create_job_list()],
                title="Runs")
        ], always_open=True)
    ])


# Populate dropdown with columns from the data table
@app.callback(
    Output("feature-dropdown", "options"),
    Input("data-table", "data"),
    prevent_initial_call=True
)
def update_feature_dropdown(data):
    return [{"label": col, "value": col} for col in data[0].keys()]


# Populate dropdown with columns from the data table
@app.callback(
    Output("discrete-covariate-dropdown", "options"),
    Output("discrete-covariate-dropdown", "value"),
    Input("data-table", "data"),
    prevent_initial_call=True
)
def update_discrete_covariate_dropdown(data):
    if not data:
        return [], None
    options = [{"label": col, "value": col} for col in data[0].keys()]
    default_value = ["Sex"] if "Sex" in data[0].keys() else None
    return options, default_value


# Populate dropdown with columns from the data table
@app.callback(
    Output("continuous-covariate-dropdown", "options"),
    Output("continuous-covariate-dropdown", "value"),
    Input("data-table", "data"),
    prevent_initial_call=True
)
def update_continuous_covariate_dropdown(data):
    if not data:
        return [], None
    options = [{"label": col, "value": col} for col in data[0].keys()]
    default_value = ["Age"] if "Age" in data[0].keys() else None
    return options, default_value


# Populate dropdown with columns from the data table
@app.callback(
    Output("site-indicator-dropdown", "options"),
    Output("site-indicator-dropdown", "value"),
    Input("data-table", "data"),
    prevent_initial_call=True
)
def update_site_indicator_dropdown(data):
    if not data:
        return [], None
    options = [{"label": col, "value": col} for col in data[0].keys()]
    default_value = "Site" if "Site" in data[0].keys() else None
    return options, default_value


@app.callback(
    Input("start-button", "n_clicks"),
    State("feature-dropdown", "value"),
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
        "harmonization_features": selected_features,
        "discrete_covariate_features": discrete_covariate_features,
        "continuous_covariate_features": continuous_covariate_features,
        "site_indicator": site_indicator
    }

    # Start job in a separate thread
    threading.Thread(target=run_job, args=(job_arguments,), daemon=True).start()

    return dash.no_update
