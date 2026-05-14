from flask import Flask, render_template, request, jsonify
import joblib
import json
import pandas as pd
import numpy as np
from pathlib import Path

app = Flask(__name__)

models_path = Path('models')

# Load features on startup
with open(models_path / 'features.json', 'r') as f:
    feature_names = json.load(f)

@app.route('/')
def index():
    try:
        with open(models_path / 'metrics.json', 'r') as f:
            metrics = json.load(f)
        with open(models_path / 'stats.json', 'r') as f:
            stats = json.load(f)
        with open(models_path / 'examples.json', 'r') as f:
            examples = json.load(f)
    except FileNotFoundError:
        metrics = {}
        stats = {}
        examples = []
        
    return render_template('index.html', metrics=metrics, features=feature_names, stats=stats, examples=examples)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        selected_model = data.get('model', 'knn')
        features_data = data.get('features')
        
        input_data = pd.DataFrame([features_data], columns=feature_names)
        
        model = joblib.load(models_path / f'{selected_model}_model.joblib')
        
        pred = int(model.predict(input_data)[0])
        
        results = {
            'model': selected_model,
            'prediction': 'High' if pred == 1 else 'Low'
        }
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/train', methods=['POST'])
def train():
    try:
        data = request.json
        model_name = data.get('model')
        params = data.get('params', {})
        
        from train_models import load_and_process_data, train_single_model
        X, y, _ = load_and_process_data()
        
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        metrics = train_single_model(model_name, params, X_train, y_train, X_test, y_test)
        
        return jsonify({'success': True, 'metrics': metrics})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
