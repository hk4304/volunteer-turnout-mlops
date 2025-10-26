from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import json
from pathlib import Path

app = Flask(__name__)

# Load model and preprocessing artifacts
MODEL_DIR = Path(__file__).parent.parent / 'models'
model = None
feature_names = None

def load_artifacts():
    global model, feature_names
    try:
        model_path = MODEL_DIR / 'model.joblib'
        feature_names_path = MODEL_DIR / 'feature_names.joblib'
        
        if model_path.exists():
            model = joblib.load(model_path)
            print("✓ Model loaded successfully")
        else:
            print("✗ Model not found")
        
        if feature_names_path.exists():
            feature_names = joblib.load(feature_names_path)
            print(f"✓ Feature names loaded: {feature_names}")
        else:
            print("✗ Feature names not found")
            
    except Exception as e:
        print(f"Error loading artifacts: {e}")

# Load artifacts on startup
load_artifacts()

@app.route('/')
def home():
    """Render the main page"""
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint
    Expected JSON format:
    {
        "month": 2,
        "day_of_week": 1,
        "time_of_day": 14,
        "is_holiday": 0,
        "beach_id": 2,
        "registered_volunteers": 110
    }
    """
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        if feature_names is None:
            return jsonify({'error': 'Feature names not loaded'}), 500
        
        data = request.get_json()
        print(f"\n[Prediction Request]")
        print(f"Received data: {data}")
        
        # Create DataFrame with features in correct order
        input_data = {feature: [data.get(feature, 0)] for feature in feature_names}
        input_df = pd.DataFrame(input_data)
        
        print(f"Input DataFrame:\n{input_df}")
        print(f"Data types:\n{input_df.dtypes}")
        
        # Make prediction
        prediction = model.predict(input_df)
        predicted_value = float(prediction[0])
        
        print(f"Prediction: {predicted_value:.2f}")
        
        return jsonify({
            'prediction': predicted_value,
            'input_features': data
        }), 200
        
    except Exception as e:
        print(f"\n[Error] {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Return current model metrics"""
    try:
        metrics_path = Path(__file__).parent.parent / 'metrics' / 'metrics.json'
        if metrics_path.exists():
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
            return jsonify(metrics), 200
        else:
            return jsonify({'error': 'Metrics not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """Return model information"""
    try:
        info = {
            'model_loaded': model is not None,
            'feature_count': len(feature_names) if feature_names else 0,
            'feature_names': feature_names if feature_names else []
        }
        return jsonify(info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
