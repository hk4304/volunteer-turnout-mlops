import pandas as pd
from sklearn.model_selection import train_test_split
import yaml
import os
import joblib


def preprocess_data(config_path):
    """
    Loads, preprocesses, and splits the dataset.
    - No encoding needed - all features are already numeric
    - Splits data into training and testing sets.
    """
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    # Paths
    raw_data_path = config['data_processing']['raw_data_path']
    processed_dir = config['data_processing']['processed_dir']
    train_path = os.path.join(processed_dir, 'train.csv')
    test_path = os.path.join(processed_dir, 'test.csv')
    model_dir = config['train']['model_dir']
    
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)

    # Load data
    df = pd.read_csv(raw_data_path)
    print(f"Loaded dataset with columns: {df.columns.tolist()}")
    print(f"Dataset shape: {df.shape}")

    # Define target
    target = config['data_processing']['target_column']
    
    # Features are all columns except target
    features = [col for col in df.columns if col != target]
    
    X = df[features]
    y = df[target]
    
    print(f"Features: {features}")
    print(f"Target: {target}")

    # Save feature names for inference
    feature_names_path = os.path.join(model_dir, 'feature_names.joblib')
    joblib.dump(features, feature_names_path)
    print(f"Feature names saved: {features}")

    # Split data
    test_size = config['data_processing']['test_size']
    random_state = config['base']['random_state']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Save processed data
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f"\n✓ Data processing complete!")
    print(f"  Training set: {train_df.shape}")
    print(f"  Test set: {test_df.shape}")


if __name__ == '__main__':
    preprocess_data('params.yaml')
