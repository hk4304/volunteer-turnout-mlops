import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import yaml
import os
import joblib


def train_model(config_path):
    """
    Trains a Random Forest Regressor model.
    - Loads training data.
    - Uses hyperparameters from the params.yaml file.
    - Saves the trained model.
    """
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    # Paths
    train_data_path = config['train']['train_data_path']
    model_dir = config['train']['model_dir']
    model_path = os.path.join(model_dir, config['train']['model_name'])
    os.makedirs(model_dir, exist_ok=True)

    # Load training data
    train_df = pd.read_csv(train_data_path)
    
    target = config['data_processing']['target_column']
    X_train = train_df.drop(columns=[target])
    y_train = train_df[target]
    
    # Model Hyperparameters
    params = config['train']['model_params']
    random_state = config['base']['random_state']

    # Initialize and train the model
    model = RandomForestRegressor(
        n_estimators=params['n_estimators'],
        max_depth=params['max_depth'],
        min_samples_split=params['min_samples_split'],
        min_samples_leaf=params['min_samples_leaf'],
        max_features=params['max_features'],
        bootstrap=params['bootstrap'],
        oob_score=params['oob_score'],
        n_jobs=params['n_jobs'],
        max_samples=params['max_samples'],
        min_weight_fraction_leaf=params['min_weight_fraction_leaf'],
        min_impurity_decrease=params['min_impurity_decrease'],
        random_state=random_state
    )
    
    model.fit(X_train, y_train)

    # Save the model
    joblib.dump(model, model_path)
    
    print(f"Model trained and saved to {model_path}")


if __name__ == '__main__':
    train_model('params.yaml')
