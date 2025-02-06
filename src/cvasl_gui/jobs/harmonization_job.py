import sys
import os
import zipfile

import cvasl
import cvasl.harmony
import time

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


def process(job_id: str) -> None:
    write_job_status(job_id, "running")
    print("Processing job", job_id)

    try:
        # Sleep (dummy)
        time.sleep(30)

        # Write some dummy output
        output_path = os.path.join(JOBS_FOLDER, job_id, "output", "output.txt")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(f"This is the output of job {job_id}")

        # Zip the output
        zip_job_output(job_id)

    except Exception as e:
        write_job_status(job_id, "failed")
        with open(os.path.join(JOBS_FOLDER, job_id, "error.log"), "w") as f:
            f.write(str(e))
        return
    
    write_job_status(job_id, "completed")


if __name__ == '__main__':
    job_id = sys.argv[1]
    process(job_id)
