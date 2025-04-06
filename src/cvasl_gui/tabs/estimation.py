import dash
from dash import dcc, html, Input, Output, State
import os
import json
import threading

from cvasl_gui.app import app
from cvasl_gui.components.job_list import run_job
from cvasl_gui import data_store


# Folder where job output files are stored
WORKING_DIR = os.getenv("CVASL_WORKING_DIRECTORY", ".")
INPUT_DIR = os.path.join(WORKING_DIR, 'data')
JOBS_DIR = os.path.join(WORKING_DIR, 'jobs')


def get_dataframe_columns():
    df = data_store.all_data
    if df is None:
        return []
    return df.columns


def create_tab_estimation():
    return html.Div([
        html.H3("Estimation"),
        
    ])

