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


def create_tab_estimation():
    return html.Div([
        html.H3("Estimation"),
        
    ])

