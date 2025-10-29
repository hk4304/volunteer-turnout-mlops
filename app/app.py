from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import json
import os
from datetime import datetime

app = Flask(__name__)

# Load model and metadata at startup
print("="*60)
print("Loading Model & Metadata...")
print("="*60)

try:
    # Load model
    model = joblib.load('models/model.joblib')
    feature_names = joblib.load('models/feature_names.joblib')
    
    # Load metrics
    with open('metrics/metrics.json', 'r') as f:
        metrics = json.load(f)
    
    # Load baseline metrics
    try:
        with open('metrics/baseline_metrics.json', 'r') as f:
            baseline_metrics = json.load(f)
    except:
        baseline_metrics = None
    
    # Get version info from environment variables
    git_commit = os.environ.get('GIT_COMMIT', 'unknown')
    build_time = os.environ.get('BUILD_TIME', 'unknown')
    model_version = os.environ.get('MODEL_VERSION', 'unknown')
    
    # Print startup info
    print(f"✓ Model loaded successfully")
    print(f"✓ Git Commit: {git_commit[:12]}")
    print(f"✓ Build Time: {build_time}")
    print(f"✓ Model Version: {model_version}")
    print(f"✓ Model R² Score: {metrics['r2']:.4f}")
    print(f"✓ Model MAE: {metrics['mae']:.2f}")
    print(f"✓ Features: {feature_names}")
    print("="*60)
    
except Exception as e:
    print(f"✗ Error loading model: {str(e)}")
    raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extract features in correct order
        features = np.array([[
            data['month'],
            data['day_of_week'],
            data['time_of_day'],
            data['is_holiday'],
            data['beach_id'],
            data['registered_volunteers']
        ]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        return jsonify({
            'prediction': round(prediction, 2),
            'model_info': {
                'version': git_commit[:7],
                'r2_score': round(metrics['r2'], 4),
                'mae': round(metrics['mae'], 2)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/version')
def version():
    """Version information endpoint"""
    return jsonify({
        'git_commit': git_commit,
        'git_commit_short': git_commit[:12] if len(git_commit) > 12 else git_commit,
        'build_time': build_time,
        'model_version': model_version,
        'python_version': os.sys.version,
        'container_id': os.environ.get('HOSTNAME', 'unknown')
    }), 200

@app.route('/model-info')
def model_info():
    """Detailed model information"""
    return jsonify({
        'model_type': 'Random Forest Regressor',
        'version_info': {
            'git_commit': git_commit,
            'git_commit_short': git_commit[:12] if len(git_commit) > 12 else git_commit,
            'build_time': build_time,
            'model_version': model_version
        },
        'current_metrics': {
            'r2': round(metrics['r2'], 4),
            'mse': round(metrics['mse'], 2),
            'mae': round(metrics['mae'], 2)
        },
        'baseline_metrics': baseline_metrics if baseline_metrics else 'No baseline available',
        'features': feature_names,
        'n_features': len(feature_names),
        'status': 'production' if baseline_metrics and metrics['r2'] >= baseline_metrics['r2'] else 'under validation'
    }), 200

@app.route('/metrics')
def get_metrics():
    """Raw metrics endpoint"""
    return jsonify(metrics), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
