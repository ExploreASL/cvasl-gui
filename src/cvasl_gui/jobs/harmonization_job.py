import sys
import os
import traceback
import zipfile
import time
import json

from cvasl.harmonizers import NeuroHarmonize
from cvasl.dataset import MRIdataset


# Argument is the job id (input and parameters(?) are inside the job folder)

JOBS_FOLDER = "jobs"

def write_job_status(job_id: str, status: str) -> None:
    """ Write the status of the job to a file (for use in the GUI)
    """
    status_path = os.path.join(JOBS_FOLDER, job_id, "job_status")
    with open(status_path, "w") as f:
        f.write(status)


def zip_job_output(job_id):
    """Create a ZIP file for job output if not already zipped"""
    output_folder = os.path.join(JOBS_FOLDER, job_id, 'output')
    zip_path = os.path.join(JOBS_FOLDER, job_id, 'output.zip')

    if not os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(output_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, arcname=os.path.relpath(file_path, output_folder))


def run_harmonization() -> None:
    """Run the harmonization process"""

    # Load job arguments
    job_arguments_path = os.path.join(JOBS_FOLDER, job_id, "job_arguments.json")
    with open(job_arguments_path) as f:
        job_arguments = json.load(f)

    input_paths = job_arguments["input_paths"]
    harmonization_features = job_arguments["harmonization_features"]
    covariate_features = job_arguments["covariate_features"]
    site_indicator = job_arguments["site_indicator"]

    print("Running harmonization")
    print("Input paths:", input_paths)
    print("Harmonization features:", harmonization_features)
    print("Covariate features:", covariate_features)

    # Perform harmonization
    mri_datasets = [MRIdataset(input_path, "1", "participant_id") for input_path in input_paths]
    harmonizer = NeuroHarmonize(harmonization_features, covariate_features, [], "Site", True)
    output = harmonizer.harmonize(mri_datasets)

    # Write output
    for i, mri_dataset in enumerate(output):
        output_folder = os.path.join(JOBS_FOLDER, job_id, 'output')
        os.makedirs(output_folder, exist_ok=True)
        df = mri_dataset.data
        df.to_csv(os.path.join(output_folder, f"output_{i}.csv"))
    # output_folder = os.path.join(JOBS_FOLDER, job_id, 'output')
    # df_out.to_csv("output.csv")


def process(job_id: str) -> None:
    write_job_status(job_id, "running")
    print("Processing job", job_id)

    try:
        run_harmonization()
        # # Sleep (dummy)
        # time.sleep(30)

        # # Write some dummy output
        # output_path = os.path.join(JOBS_FOLDER, job_id, "output", "output.txt")
        # os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # with open(output_path, "w") as f:
        #     f.write(f"This is the output of job {job_id}")

        # Zip the output
        zip_job_output(job_id)

    except Exception as e:
        write_job_status(job_id, "failed")
        with open(os.path.join(JOBS_FOLDER, job_id, "error.log"), "w") as f:
            f.write(traceback.format_exc())
        return
    
    write_job_status(job_id, "completed")


if __name__ == '__main__':
    job_id = sys.argv[1]
    process(job_id)
