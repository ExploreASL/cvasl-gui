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

# Monkey patch to fix the DataFrame ambiguity bug
def _fixed_store_fold_predictions(self, fold_index, y_test, y_pred, y_val, y_pred_val, test_index):
    """Fixed version of _store_fold_predictions that handles DataFrame ambiguity properly."""
    import pandas as pd
    
    # Ensure arrays are properly flattened only if needed
    y_test_flat = y_test.flatten() if hasattr(y_test, 'flatten') else y_test
    y_pred_flat = y_pred.flatten() if hasattr(y_pred, 'flatten') else y_pred
    
    predictions_data = pd.DataFrame({'y_test': y_test_flat, 'y_pred': y_pred_flat})
    predictions_data[self.patient_identifier] = self.data[self.patient_identifier].values[test_index]
    predictions_data['site'] = self.data[self.site_indicator].values[test_index]
    predictions_data['fold'] = fold_index
    
    predictions_data_val = None
    if y_val is not None and y_pred_val is not None and self.data_validation is not None:
        y_val_flat = y_val.flatten() if hasattr(y_val, 'flatten') else y_val
        y_pred_val_flat = y_pred_val.flatten() if hasattr(y_pred_val, 'flatten') else y_pred_val
        
        predictions_data_val = pd.DataFrame({'y_test': y_val_flat, 'y_pred': y_pred_val_flat})
        predictions_data_val[self.patient_identifier] = self.data_validation[self.patient_identifier].values
        predictions_data_val['site'] = self.data_validation[self.site_indicator].values
        predictions_data_val['fold'] = fold_index
    
    return predictions_data, predictions_data_val

# Apply the monkey patch
PredictBrainAge._store_fold_predictions = _fixed_store_fold_predictions


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
    model_name = job_arguments["model_name"] # TODO: actually use it

    parameters = job_arguments["parameters"]
    prediction_features = parameters["prediction_features"]
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
    
    #TODO: not sure why this is necessary
    # Try to avoid the DataFrame ambiguity error by handling validation datasets carefully
    validation_datasets = mri_datasets_validation if mri_datasets_validation else None
    
    predicter = PredictBrainAge(model_name='extratree', model_file_name='extratree', model=model,
                                datasets=mri_datasets_train, datasets_validation=validation_datasets, features=prediction_features,
                                target='age', cat_category='sex', cont_category='age', n_bins=2, splits=1, test_size_p=0.05, random_state=42)

    # Perform training and prediction
    metrics_df, metrics_df_val, predictions_df, predictions_df_val, models = predicter.predict()

    # Some final processing & Write output
    output_folder = os.path.join(JOBS_DIR, job_id, 'output')
    os.makedirs(output_folder, exist_ok=True)
    
    # Save metrics
    if metrics_df is not None:
        metrics_df.to_csv(os.path.join(output_folder, f"metrics_train_{label}.csv"), index=False)
    if metrics_df_val is not None:
        metrics_df_val.to_csv(os.path.join(output_folder, f"metrics_validation_{label}.csv"), index=False)
    
    # Process and save predictions
    if predictions_df is not None:
        # Add age_gap calculation if both age columns exist
        df = predictions_df.copy()
        if 'y_pred' in df.columns and 'y_test' in df.columns:
            df['age_gap'] = df['y_pred'] - df['y_test']
            df['age_predicted'] = df['y_pred']
            df['age'] = df['y_test']
        df['label'] = label
        df.to_csv(os.path.join(output_folder, f"predictions_train_{label}.csv"), index=False)
    
    if predictions_df_val is not None:
        # Add age_gap calculation if both age columns exist
        df = predictions_df_val.copy()
        if 'y_pred' in df.columns and 'y_test' in df.columns:
            df['age_gap'] = df['y_pred'] - df['y_test']
            df['age_predicted'] = df['y_pred']
            df['age'] = df['y_test']
        df['label'] = label
        df.to_csv(os.path.join(output_folder, f"predictions_validation_{label}.csv"), index=False)


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
