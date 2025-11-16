import os
import joblib


def model_fn(model_dir):
    """Load model for inference"""
    # TODO: Load the model file named 'trained_model.joblib'
    model = joblib.load(os.path.join(model_dir, 'trained_model.joblib'))
    return model
