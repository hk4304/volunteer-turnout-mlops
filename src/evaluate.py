import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import yaml
import os
import joblib
import json


def evaluate_model(config_path):
    """
    Evaluates the trained model on the test set.
    - Loads the test data and the trained model.
    - Calculates MSE, MAE, and R2 score.
    - Saves the metrics to a JSON file.
    """
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    # Paths
    test_data_path = config['evaluate']['test_data_path']
    model_path = os.path.join(config['train']['model_dir'], config['train']['model_name'])
    metrics_path = config['evaluate']['metrics_path']
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
    
    # Load test data
    test_df = pd.read_csv(test_data_path)
    
    target = config['data_processing']['target_column']
    X_test = test_df.drop(columns=[target])
    y_test = test_df[target]
    
    # Load the model
    model = joblib.load(model_path)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model evaluation results:")
    print(f"  Mean Squared Error: {mse:.4f}")
    print(f"  Mean Absolute Error: {mae:.4f}")
    print(f"  R2 Score: {r2:.4f}")
    
    # Save metrics
    metrics = {
        'mse': float(mse),
        'mae': float(mae),
        'r2': float(r2)
    }
    
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
        
    print(f"Metrics saved to {metrics_path}")


if __name__ == '__main__':
    evaluate_model('params.yaml')
