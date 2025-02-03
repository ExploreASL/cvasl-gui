import sys

import cvasl
import cvasl.harmony

# Argument is the job id (input and parameters(?) are inside the job folder)

# Write the process id to a file in the job folder (so we can see whether it is still running)

# When finished and output has been written, set the status to "completed" by writing a flag file

def write_job_status(job_id: str, status: str) -> None:
    with open(f"job_output/{job_id}/job_status", "w") as f:
        f.write(status)


def process(job_id: str) -> None:
    write_job_status(job_id, "running")
    print("Processing job", job_id)

    #cvasl.harmony.harmonize()



if __name__ == '__main__':
    # Get the job id argument
    job_id = sys.argv[1]


