import dash
from dash import dcc, html, Input, Output, State, ctx

import os
import time
import threading
import subprocess
import json

from cvasl_gui.app import app

# Folder where job output files are expected
OUTPUT_FOLDER = "job_output"

def create_tab_harmonization():
    return html.Div([
        html.Button("Start Job", id="start-button", n_clicks=0),
        html.Div(id="job-status"),
        dcc.Interval(id="interval-check", interval=3000, n_intervals=0)
    ])

def run_job():
    """Function to start the harmonization job"""

    # Create a unique folder for the job
    job_id = str(int(time.time()))
    job_folder = os.path.join(OUTPUT_FOLDER, job_id)
    os.makedirs(job_folder, exist_ok=True)

    # Write the job input

    # Start the job
    print("Starting job", job_id)
    # Get the path to the harmonization script, relative to this module
    script_path = os.path.join(os.path.dirname(__file__), "..", "jobs", "harmonization_job.py")
    process = subprocess.Popen(["python", script_path, job_id])

    job_details = {
        "id": job_id,
        "process": process.pid,
        "start_time": time.isoformat(),
        # input dir? input file? parameters?
    }
    json.dump(job_details, open(os.path.join(job_folder, "job_details.json"), "w"))


def check_job_status():
    """Check if expected output files exist"""
    status_list = {}
    job_dirs = os.listdir(OUTPUT_FOLDER)
    for job_dir in job_dirs:
        job_details_file = os.path.join(OUTPUT_FOLDER, job_dir, "job_details.json")
        if os.path.exists(job_details_file):
            details = json.load(open(job_details_file))
            process_id = details["process"]
            if not os.path.exists(f"/proc/{process_id}"):
                # Process is not running
                status_list[job_dir] = "completed"
                # TODO: distinguish between success and failure
            else:
                # Process is still running
                status_list[job_dir] = "running"
            # with open(job_status_file, "r") as f:
            #     status = f.read().strip()
            #     status_list[job_dir] = status
    return status_list


@app.callback(
    Output("job-status", "children"),
    Input("start-button", "n_clicks"),
    Input("interval-check", "n_intervals"),
    prevent_initial_call=True
)
def start_or_monitor_job(n_clicks, n_intervals):
    """Starts the job or monitors its status"""

    triggered_id = triggered_id = ctx.triggered_id

    if triggered_id == "start-button":
        # Start the job
        threading.Thread(target=run_job, daemon=True).start()
        return "Job started, waiting for output..."

    elif triggered_id == "interval-check":
        # Monitor job output
        status_list = check_job_status()

        return html.Ul([html.Li(f"Job {job_id}: {status}") for job_id, status in status_list.items()])

    return dash.no_update
