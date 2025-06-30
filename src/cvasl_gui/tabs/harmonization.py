import time
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import os
import threading

from cvasl_gui.app import app
from cvasl_gui.components.job_list import run_job
from cvasl_gui import data_store
from cvasl_gui.components.directory_input import create_directory_input
from cvasl_gui.components.data_table import create_data_table
from cvasl_gui.components.feature_compare import create_feature_compare
from cvasl_gui.components.job_list import create_job_list, get_job_status

# Folder where job output files are stored
WORKING_DIR = os.getenv("CVASL_WORKING_DIRECTORY", ".")
INPUT_DIR = os.path.join(WORKING_DIR, 'data')
JOBS_DIR = os.path.join(WORKING_DIR, 'jobs')

ALGORITHM_PARAMS = {
        "neuroharmonize": ["features-to-harmonize", "covariates", "smooth-terms", "site-indicator", "empirical-bayes"],
        "covbat": ["features-to-harmonize", "covariates", "site-indicator", "patient-identifier", "numerical-covariates", "empirical-bayes"],
        "neurocombat": ["features-to-harmonize", "discrete-covariates", "continuous-covariates", "site-indicator", "patient-identifier", "empirical-bayes", "mean-only", "parametric"],
}    
# neuroharmonize
# covbat
# neurocombat
# nestedcombat
# comscanneuroharmonize
# autocombat
# relief
# combat++


def get_dataframe_columns():
    df = data_store.all_data['harmonization']
    if df is None:
        return []
    return df.columns


def create_tab_harmonization():
    return html.Div([
        dbc.Accordion([
            dbc.AccordionItem([create_directory_input('harmonization')],
                title="Select new input data"),
            dbc.AccordionItem([create_data_table('harmonization')],
                title="Inspect data"),
            dbc.AccordionItem([create_feature_compare()],
                title="Feature comparison"),
            dbc.AccordionItem(create_harmonization_parameters(),
                title="Harmonization"),
            dbc.AccordionItem([create_job_list()],
                title="Runs"),
            dcc.Store(id="harmonization-job-id", data=None),
        ], always_open=True)
    ])


def LabelWithInfoCol(label_text, tooltip_id, tooltip_text, width=3):
    return dbc.Col(
        dbc.Row(
            [
                html.Label(
                    label_text,
                    style={"marginTop": "6px", "marginRight": "5px"}
                ),
                html.I(
                    className="bi bi-info-circle-fill",
                    id=f"{tooltip_id}-target",
                    style={"cursor": "pointer", "color": "#0d6efd"}
                ),
                dbc.Tooltip(
                    tooltip_text,
                    target=f"{tooltip_id}-target",
                    placement="right",
                    trigger="hover"
                )
            ],
            align="center"
        ),
        width=width
    )


# All possible parameters for the different harmonization methods

# data_subset
# features_to_harmonize
# batch_list_harmonisations
# covariates
# discrete_covariates
# continuous_covariates
# numerical_covariates
# discrete_covariates_to_remove
# continuous_covariates_to_remove
# smooth_terms
# discrete_cluster_features
# continuous_cluster_features

# metric: str
# features_reduction: str
# feature_reduction_dimensions: int

# flags:
# emperical_bayes: bool
# mean_only: bool
# parametric: bool
# return_extended: bool
# use_gmm: bool

# site_indicator
# patient_identifier
# intermediate_results_path?


def create_harmonization_parameters():

    return [
        dbc.Row([
            dbc.Col(html.Label("Algorithm:", style={"marginTop": "6px"}), width=3),
            dbc.Col(
                dcc.Dropdown(
                    id="algorithm-dropdown",
                    options=[
                        {"label": "NeuroCombat", "value": "neurocombat"},
                        {"label": "NeuroHarmonize", "value": "neuroharmonize"},
                        {"label": "Covbat", "value": "covbat"},
                        {"label": "NestedCombat", "value": "nestedcombat"},
                        {"label": "ComscanNeuroHarmonize", "value": "comscanneuroharmonize"},
                        {"label": "AutoCombat", "value": "autocombat"},
                        {"label": "Relief", "value": "relief"},
                        {"label": "Combat++", "value": "combat++"},
                    ],
                    value="neurocombat",
                    clearable=False,
                ),
            ),
        ], className="mb-3", id="row-algorithm"),

        dbc.Row([
            LabelWithInfoCol("Data subset:", "data-subset-tooltip",
                "Select a subset of the data to harmonize"),
            dbc.Col(
                dcc.Dropdown(id="data-subset-dropdown", options=[], multi=True,
                    placeholder="Select data subset...",
                ),
            ),
        ], className="mb-3", id="row-data-subset"),

        dbc.Row([
            dbc.Col(html.Label("Features to harmonize:", style={"marginTop": "6px"}), width=3),
            dbc.Col(
                dcc.Dropdown(id="feature-dropdown", options=[], multi=True,
                    placeholder="Select features...",
                ),
            ),
        ], className="mb-3", id="row-features-to-harmonize"),

        dbc.Row([
            LabelWithInfoCol("Batch list harmonizations:", "batch-list-harmonizations-tooltip",
                ""),
            dbc.Col(
                dcc.Dropdown(id="batch-list-harmonizations-dropdown", options=[],
                    multi=True, placeholder="Select batch list harmonizations...",
                ),
            ),
        ], className="mb-3", id="row-batch-list-harmonizations"),

        dbc.Row([
            LabelWithInfoCol("Covariates:", "covariates-tooltip",
                ""),
            dbc.Col(
                dcc.Dropdown(id="covariates-dropdown", options=[],
                    multi=True, placeholder="Select covariates...",
                ),
            ),
        ], className="mb-3", id="row-covariates"),

        dbc.Row([
            LabelWithInfoCol("Discrete covariates:", "discrete-covariates-tooltip",
                "Discreate covariates to control for"),
            dbc.Col(
                dcc.Dropdown(id="discrete-covariate-dropdown", options=[], multi=True,
                    placeholder="Select discrete covariates...",
                ),
            ),
        ], className="mb-3", id="row-discrete-covariates"),

        dbc.Row([
            LabelWithInfoCol("Continuous covariates:", "continuous-covariates-tooltip",
                "Continuous covariates to control for"),
            dbc.Col(
                dcc.Dropdown(id="continuous-covariate-dropdown", options=[], multi=True,
                    placeholder="Select continuous covariates...",
                ),
            ),
        ], className="mb-3", id="row-continuous-covariates"),

        dbc.Row([
            LabelWithInfoCol("Site indicator:", "site-indicator-tooltip",
                "Column name indicating the site or batch"),
            dbc.Col(
                dcc.Dropdown(id="site-indicator-dropdown", options=[], multi=False,
                    placeholder="Select site indicator...",
                ),
            ),
        ], className="mb-3", id="row-site-indicator"),

        dbc.Row([
            dbc.Col(html.Label("Label:", style={"marginTop": "6px"}), width=3),
            dbc.Col(dbc.Input(id="label-input", type="text",
                placeholder="Enter label...", value="harmonized"),
            ),
        ], className="mb-3", id="row-label-input"),

        # Row for button and status
        dbc.Row([
            dbc.Col(html.Label("", style={"marginTop": "6px"}), width=3),
            dbc.Col(
                html.Div([
                    html.Button("Start harmonization", id="start-button", n_clicks=0),
                    html.Span("Status: ", style={"marginLeft": "10px"}),
                    html.Span(id="harmonization-job-status", children="Idle"),
                    dcc.Interval(id="harmonization-status-interval", interval=1000, n_intervals=0, disabled=True)
                ]),
            ),
        ], className="mb-3"),
    ]


@app.callback(
    [
        Output("row-data-subset", "style"),
        Output("row-features-to-harmonize", "style"),
        Output("row-continuous-covariates", "style"),
        Output("row-discrete-covariates", "style"),
        Output("row-site-indicator", "style"),
    ],
    Input("algorithm-dropdown", "value"),
)
def toggle_rows(algorithm):
    visible = ALGORITHM_PARAMS.get(algorithm, [])

    return [
        {"display": "flex"} if "data-subset" in visible else {"display": "none"},
        {"display": "flex"} if "features-to-harmonize" in visible else {"display": "none"},
        {"display": "flex"} if "continuous-covariates" in visible else {"display": "none"},
        {"display": "flex"} if "discrete-covariates" in visible else {"display": "none"},
        {"display": "flex"} if "site-indicator" in visible else {"display": "none"},
    ]


#
#  Populate the dropdowns with columns from the data table
#

@app.callback(
    Output("data-subset-dropdown", "options"),
    Input({'type': 'data-table', 'index': 'harmonization'}, "data"),
    prevent_initial_call=True
)
def update_data_subset_dropdown(data):
    if not data:
        return []
    return [{"label": col, "value": col} for col in data[0].keys()]

@app.callback(
    Output("feature-dropdown", "options"),
    Input({'type': 'data-table', 'index': 'harmonization'}, "data"),
    prevent_initial_call=True
)
def update_feature_dropdown(data):
    if not data: # Check if data is empty
        return []
    return [{"label": col, "value": col} for col in data[0].keys()]

@app.callback(
    Output("discrete-covariate-dropdown", "options"),
    Output("discrete-covariate-dropdown", "value"),
    Input({'type': 'data-table', 'index': 'harmonization'}, "data"),
    prevent_initial_call=True
)
def update_discrete_covariate_dropdown(data):
    if not data:
        return [], None
    options = [{"label": col, "value": col} for col in data[0].keys()]
    default_value = ["Sex"] if "Sex" in data[0].keys() else None
    return options, default_value

@app.callback(
    Output("continuous-covariate-dropdown", "options"),
    Output("continuous-covariate-dropdown", "value"),
    Input({'type': 'data-table', 'index': 'harmonization'}, "data"),
    prevent_initial_call=True
)
def update_continuous_covariate_dropdown(data):
    if not data:
        return [], None
    options = [{"label": col, "value": col} for col in data[0].keys()]
    default_value = ["Age"] if "Age" in data[0].keys() else None
    return options, default_value

@app.callback(
    Output("site-indicator-dropdown", "options"),
    Output("site-indicator-dropdown", "value"),
    Input({'type': 'data-table', 'index': 'harmonization'}, "data"),
    prevent_initial_call=True
)
def update_site_indicator_dropdown(data):
    if not data:
        return [], None
    options = [{"label": col, "value": col} for col in data[0].keys()]
    default_value = "Site" if "Site" in data[0].keys() else None
    return options, default_value



@app.callback(
    Output("harmonization-job-id", "data"),
    Output("harmonization-status-interval", "disabled", allow_duplicate=True),
    Input("start-button", "n_clicks"),
    State("algorithm-dropdown", "value"),
    State("feature-dropdown", "value"),
    State("discrete-covariate-dropdown", "value"),
    State("continuous-covariate-dropdown", "value"),
    State("site-indicator-dropdown", "value"),
    State("label-input", "value"),
    prevent_initial_call=True
)
def start_job(n_clicks, algorithm, selected_features, discrete_covariate_features, continuous_covariate_features, 
              site_indicator, label):
    if not selected_features:
        return dash.no_update, True

    job_arguments = {
        "algorithm": algorithm,
        "input_paths": data_store.input_files['harmonization'],
        "input_sites": data_store.input_sites['harmonization'],
        "parameters": {
            "features_to_harmonize": selected_features,
            "discrete_covariates": discrete_covariate_features,
            "continuous_covariates": continuous_covariate_features,
            "site_indicator": site_indicator,
            "patient_identifier": 'participant_id'
        },
        "label": label,
    }

    # Generate job_id or receive from run_job
    job_id = str(int(time.time()))
    threading.Thread(target=run_job, args=(job_arguments, job_id, True), daemon=True).start()

    return job_id, False  # enable the interval


@app.callback(
    Output("harmonization-job-status", "children"),
    Output("harmonization-status-interval", "disabled", allow_duplicate=True),
    Input("harmonization-status-interval", "n_intervals"),
    State("harmonization-job-id", "data"),
    prevent_initial_call=True,
)
def update_job_status(n, job_id):
    if not job_id:
        return "", True

    status = get_job_status(job_id)

    if status.lower() in ("completed", "failed", "cancelled"):
        return status, True  # Stop interval
    return status, False
