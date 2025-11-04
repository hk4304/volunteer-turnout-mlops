import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import yaml
import os
import joblib
import mlflow
import mlflow.sklearn


def train_model(config_path):
    """
    Trains a Random Forest Regressor model.
    """
    print("🔄 Starting training...")  # ← ADD THIS
    
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    # Paths
    train_data_path = config['train']['train_data_path']
    model_dir = config['train']['model_dir']
    model_path = os.path.join(model_dir, config['train']['model_name'])
    os.makedirs(model_dir, exist_ok=True)

    # Load training data
    print(f"📂 Loading data from {train_data_path}...")  # ← ADD THIS
    train_df = pd.read_csv(train_data_path)
    print(f"   Loaded {len(train_df)} samples")  # ← ADD THIS
    
    target = config['data_processing']['target_column']
    X_train = train_df.drop(columns=[target])
    y_train = train_df[target]
    
    # Model Hyperparameters
    params = config['train']['model_params']
    random_state = config['base']['random_state']

    # ═══════════════════════════════════════════════════════
    # START MLflow EXPERIMENT
    # ═══════════════════════════════════════════════════════
    print("🔬 Starting MLflow experiment...")  # ← ADD THIS
    mlflow.set_experiment("volunteer-turnout")
    
    with mlflow.start_run(run_name=f"RF_n_estimators_{params['n_estimators']}"):
        print("📝 Logging parameters...")  # ← ADD THIS
        
        # Log hyperparameters
        mlflow.log_params({
            "n_estimators": params['n_estimators'],
            "max_depth": params['max_depth'],
            "min_samples_split": params['min_samples_split'],
            "min_samples_leaf": params['min_samples_leaf'],
            "max_features": params['max_features'],
            "random_state": random_state
        })
        
        # Initialize and train the model
        print("🚀 Training Random Forest...")  # ← ADD THIS
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
        print("✅ Model training complete!")
        
        # Calculate training metrics (for logging)
        print("📊 Calculating metrics...")  # ← ADD THIS
        y_train_pred = model.predict(X_train)
        train_r2 = r2_score(y_train, y_train_pred)
        train_mae = mean_absolute_error(y_train, y_train_pred)
        train_mse = mean_squared_error(y_train, y_train_pred)
        
        # Log metrics to MLflow
        print("📝 Logging metrics...")  # ← ADD THIS
        mlflow.log_metrics({
            "train_r2": train_r2,
            "train_mae": train_mae,
            "train_mse": train_mse
        })
        
        # Log the model to MLflow
        print("💾 Logging model...")  # ← ADD THIS
        mlflow.sklearn.log_model(model, "model")
        
        print(f"\n📊 Training Metrics:")
        print(f"   R² Score: {train_r2:.4f}")
        print(f"   MAE: {train_mae:.2f}")
        print(f"   MSE: {train_mse:.2f}")
        
        # Save the model locally
        joblib.dump(model, model_path)
        print(f"\n✅ Model saved to {model_path}")
    
    print("\n🎉 Training completed and logged to MLflow!")
    print("   Run 'mlflow ui' to view results\n")


if __name__ == '__main__':
    train_model('params.yaml')
