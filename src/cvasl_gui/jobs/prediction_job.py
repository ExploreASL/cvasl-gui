import sys
import os
import traceback
import zipfile
import json
import numpy as np
import pandas as pd

from cvasl.prediction import PredictBrainAge
from cvasl.dataset import MRIdataset, encode_cat_features

from sklearn.ensemble import ExtraTreesRegressor


# Argument is the job id (input and parameters(?) are inside the job folder)

WORKING_DIR = os.getenv("CVASL_WORKING_DIRECTORY", ".")
INPUT_DIR = os.path.join(WORKING_DIR, 'data')
JOBS_DIR = os.path.join(WORKING_DIR, 'jobs')


def write_job_status(job_id: str, status: str) -> None:
    """ Write the status of the job to a file (for use in the GUI)
    """
    status_path = os.path.join(JOBS_DIR, job_id, "job_status")
    with open(status_path, "w") as f:
        f.write(status)


def zip_job_output(job_id):
    """Create a ZIP file for job output if not already zipped"""
    output_folder = os.path.join(JOBS_DIR, job_id, 'output')
    zip_path = os.path.join(JOBS_DIR, job_id, 'output.zip')

    if not os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(output_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, arcname=os.path.relpath(file_path, output_folder))


def run_prediction() -> None:
    """Run the prediction process"""

    # Load job arguments
    job_arguments_path = os.path.join(JOBS_DIR, job_id, "job_arguments.json")
    with open(job_arguments_path) as f:
        job_arguments = json.load(f)
    train_paths = job_arguments["train_paths"]
    train_names = [ os.path.splitext(os.path.basename(path))[0] for path in train_paths ]
    train_sites = job_arguments["train_sites"]
    validation_paths = job_arguments["validation_paths"]
    validation_names = [ os.path.splitext(os.path.basename(path))[0] for path in validation_paths ]
    validation_sites = job_arguments["validation_sites"]
    model = job_arguments["model"] # TODO: actually use it
    prediction_features = job_arguments["prediction_features"]
    prediction_features = list(map(lambda x: x.lower(), prediction_features))
    label = job_arguments["label"]
    if label is None or label == "":
        label = "predicted"

    # Load the training datasets into pandas dataframes and concatenate them
    train_dfs = [pd.read_csv(path) for path in train_paths]
    train_dfs = pd.concat(train_dfs, ignore_index=True)
    validation_dfs = [pd.read_csv(path) for path in validation_paths]
    validation_dfs = pd.concat(validation_dfs, ignore_index=True)

    print("Running prediction")
    print("Train paths:", train_paths)
    print("Validation paths:", validation_paths)
    print("prediction features:", prediction_features)

    # Prepare train datasets
    mri_datasets_train = [MRIdataset(input_path, input_site, "participant_id", features_to_drop=[])
                          for input_site, input_path in zip(train_sites, train_paths) ]
    for mri_dataset in mri_datasets_train:
        mri_dataset.preprocess()
    features_to_map = ['sex']
    encode_cat_features(mri_datasets_train, features_to_map)

    # Prepare test datasets
    mri_datasets_validation = [MRIdataset(input_path, input_site, "participant_id", features_to_drop=[])
                               for input_site, input_path in zip(validation_sites, validation_paths) ]
    for mri_dataset in mri_datasets_validation:
        mri_dataset.preprocess()
    features_to_map = ['sex']
    encode_cat_features(mri_datasets_validation, features_to_map)

    # Create model & predictor
    model = ExtraTreesRegressor(n_estimators=100,random_state=np.random.randint(0,100000), criterion='absolute_error', min_samples_split=2,
                                min_samples_leaf=1, max_features='log2',bootstrap=False, n_jobs=-1, warm_start=True)
    predicter = PredictBrainAge(model_name='extratree', model_file_name='extratree', model=model,
                                datasets=mri_datasets_train, datasets_validation=mri_datasets_validation, features=prediction_features,
                                target='age', cat_category='sex', cont_category='age', n_bins=2, splits=1, test_size_p=0.05, random_state=42)

    # Perform training and prediction
    metrics_df, metrics_df_val, predictions_df, predictions_df_val, models = predicter.train_and_evaluate()
    mri_datasets_train = [predicter.predict(dataset) for dataset in mri_datasets_train]
    mri_datasets_validation = [predicter.predict(dataset) for dataset in mri_datasets_validation]

    # Some final processing & Write output
    output_folder = os.path.join(JOBS_DIR, job_id, 'output')
    os.makedirs(output_folder, exist_ok=True)
    for i, dataset in enumerate(mri_datasets_train):
        df = dataset.data
        df['age_gap'] = get_column_case_insensitive(df, 'age_predicted') - get_column_case_insensitive(df, 'age')
        df['label'] = label
        df.to_csv(os.path.join(output_folder, f"{train_names[i]}_{label}.csv"), index=False)
    for i, dataset in enumerate(mri_datasets_validation):
        df = dataset.data
        df['age_gap'] = get_column_case_insensitive(df, 'age_predicted') - get_column_case_insensitive(df, 'age')
        df['label'] = label
        df.to_csv(os.path.join(output_folder, f"{validation_names[i]}_{label}.csv"), index=False)


def get_column_case_insensitive(df, colname):
    match = [c for c in df.columns if c.lower() == colname.lower()]
    if not match:
        raise KeyError(f"Column '{colname}' not found.")
    return df[match[0]]


def process(job_id: str) -> None:
    write_job_status(job_id, "running")
    print("Processing job", job_id)

    try:
        run_prediction()

        # Zip the output
        zip_job_output(job_id)

    except Exception as e:
        write_job_status(job_id, "failed")
        with open(os.path.join(JOBS_DIR, job_id, "error.log"), "w") as f:
            f.write(traceback.format_exc())
        return
    
    write_job_status(job_id, "completed")


if __name__ == '__main__':
    job_id = sys.argv[1]
    process(job_id)
