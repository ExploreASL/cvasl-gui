import dash
from dash import dcc, html, Input, Output, State, ctx, MATCH, ALL
import os
import time
import threading
import subprocess
import json
import signal

from cvasl_gui.app import app

# Folder where job output files are stored
OUTPUT_FOLDER = "jobs"

def create_tab_harmonization():
    return html.Div([
        html.Button("Start Job", id="start-button", n_clicks=0),
        html.Div(id="job-status"),
        dcc.Interval(id="interval-check", interval=3000, n_intervals=0),
        dcc.Download(id="download-data")
    ])

def run_job():
    """Function to start the harmonization job"""

    # Create a unique folder for the job
    job_id = str(int(time.time()))
    job_folder = os.path.join(OUTPUT_FOLDER, job_id)
    os.makedirs(job_folder, exist_ok=True)

    # Save job arguments
    job_arguments = {
        "input_paths": ["/Users/peter/repos/brainage/data-workshop/TestingData_Site1_fake.csv"],
        "harmonization_features": ["GM_vol", "WM_vol"],
        "covariate_features": ["Age","Sex","Site"]
    }
    with open(os.path.join(job_folder, "job_arguments.json"), "w") as f:
        json.dump(job_arguments, f)

    # Start the job
    print("Starting job", job_id)
    script_path = os.path.join(os.path.dirname(__file__), "..", "jobs", "harmonization_job.py")
    process = subprocess.Popen(["python", script_path, job_id])

    # Save job details (so it can be monitored)
    job_details = {
        "id": job_id,
        "process": process.pid,
        "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(os.path.join(job_folder, "job_details.json"), "w") as f:
        json.dump(job_details, f)

def check_job_status():
    """Check if jobs are still running and return their details"""
    job_data = []
    job_dirs = sorted(os.listdir(OUTPUT_FOLDER), reverse=True)

    for job_dir in job_dirs:
        job_details_file = os.path.join(OUTPUT_FOLDER, job_dir, "job_details.json")
        if os.path.exists(job_details_file):
            # Load the job details
            with open(job_details_file) as f:
                details = json.load(f)

            # Load current status
            status_file = os.path.join(OUTPUT_FOLDER, job_dir, "job_status")
            if os.path.exists(status_file):
                with open(status_file) as f:
                    details["status"] = f.read()

            # Check if process is still running
            process_id = details.get("process")
            details["running"] = is_process_running(process_id)

            job_data.append(details)

    return job_data

def cancel_job(job_id):
    """Terminate a running job"""
    job_details_file = os.path.join(OUTPUT_FOLDER, job_id, "job_details.json")
    if os.path.exists(job_details_file):
        with open(job_details_file) as f:
            details = json.load(f)

        process_id = details.get("process")
        if os.path.exists(f"/proc/{process_id}"):
            os.kill(process_id, signal.SIGTERM)  # Send termination signal
            details["status"] = "cancelled"
            with open(job_details_file, "w") as f:
                json.dump(details, f)

def remove_job(job_id):
    """Delete job folder"""
    job_folder = os.path.join(OUTPUT_FOLDER, job_id)
    if os.path.exists(job_folder):
        for root, dirs, files in os.walk(job_folder, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(job_folder)

def is_process_running(pid):
    """Check if a process is running"""
    try:
        result = subprocess.run(["ps", "-p", str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0  # Return True if process is found
    except Exception as e:
        print(f"Error checking process: {e}")
        return False

@app.callback(
    Output("job-status", "children"),
    Input("start-button", "n_clicks"),
    Input("interval-check", "n_intervals"),
    Input({"type": "cancel-job", "index": ALL}, "n_clicks"),
    Input({"type": "remove-job", "index": ALL}, "n_clicks"),
    State({"type": "cancel-job", "index": ALL}, "id"),
    State({"type": "remove-job", "index": ALL}, "id"),
    prevent_initial_call=True
)
def start_or_monitor_job(n_clicks, n_intervals, cancel_clicks, remove_clicks, cancel_ids, remove_ids):
    """Starts a new job, updates job status table, handles job cancellations and removals"""

    triggered_id = ctx.triggered_id

    # Handle job cancellation
    if triggered_id and isinstance(triggered_id, dict) and triggered_id["type"] == "cancel-job":
        cancel_job(triggered_id["index"])

    # Handle job removal
    if triggered_id and isinstance(triggered_id, dict) and triggered_id["type"] == "remove-job":
        remove_job(triggered_id["index"])

    # Start new job
    if triggered_id == "start-button":
        threading.Thread(target=run_job, daemon=True).start()
        return "Job started, waiting for output..."

    # Monitor job output
    job_data = check_job_status()

    table_header = html.Tr([
        html.Th("Job ID"),
        html.Th("Running?"),
        html.Th("Status"),
        html.Th("Start Time"),
        html.Th("Download"),
        html.Th("Cancel"),
        html.Th("Remove")
    ])

    table_rows = [
        html.Tr([
            html.Td(job.get("id", "")),
            html.Td("Yes" if job.get("running", False) else "No"),
            html.Td(job.get("status", "")),
            html.Td(job.get("start_time", "")),
            html.Td(html.Button("Download", id={"type": "download-output", "index": job["id"]}, n_clicks=0) if job.get("status", "") == "completed" else ""),
            html.Td(html.Button("Cancel", id={"type": "cancel-job", "index": job["id"]}, n_clicks=0) if job.get("running", False) else ""),
            html.Td(html.Button("Remove", id={"type": "remove-job", "index": job["id"]}, n_clicks=0) if not job.get("running", False) else "")
        ]) for job in job_data
    ]

    return html.Table([table_header] + table_rows, style={"width": "100%", "border": "1px solid black"})

@app.callback(
    Output("download-data", "data"),
    Input({"type": "download-output", "index": ALL}, "n_clicks"),
    State({"type": "download-output", "index": ALL}, "id"),
    prevent_initial_call=True,
)
def func(n_clicks, ids):
    if not ctx.triggered_id or not isinstance(ctx.triggered_id, dict):
        return dash.no_update  # Prevent unnecessary execution

    triggered_id = ctx.triggered_id
    if triggered_id["type"] == "download-output":

        # Ensure the button was actually clicked this time
        job_id = triggered_id["index"]
        index = [id["index"] for id in ids].index(job_id)
        if n_clicks[index] > 0:
            path = os.path.join(OUTPUT_FOLDER, job_id, "output.zip")
            return dcc.send_file(path)

    return dash.no_update  # Avoid unwanted triggers
