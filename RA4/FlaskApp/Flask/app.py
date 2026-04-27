from flask import Flask, render_template, request, jsonify
import joblib
import json
import pandas as pd
import numpy as np
from pathlib import Path

app = Flask(__name__)

# Load models and metadata
models_path = Path('models')
knn_model = joblib.load(models_path / 'knn_model.joblib')
perceptron_model = joblib.load(models_path / 'perceptron_model.joblib')
nb_model = joblib.load(models_path / 'nb_model.joblib')
tree_model = joblib.load(models_path / 'tree_model.joblib')
nn_model = joblib.load(models_path / 'nn_model.joblib')

with open(models_path / 'metrics.json', 'r') as f:
    metrics = json.load(f)

with open(models_path / 'features.json', 'r') as f:
    feature_names = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', metrics=metrics, features=feature_names)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Create a DataFrame with the features in the correct order
        input_data = pd.DataFrame([data], columns=feature_names)
        
        # Predictions
        knn_pred = int(knn_model.predict(input_data)[0])
        perceptron_pred = int(perceptron_model.predict(input_data)[0])
        nb_pred = int(nb_model.predict(input_data)[0])
        tree_pred = int(tree_model.predict(input_data)[0])
        nn_pred = int(nn_model.predict(input_data)[0])
        
        results = {
            'knn': 'High' if knn_pred == 1 else 'Low',
            'perceptron': 'High' if perceptron_pred == 1 else 'Low',
            'nb': 'High' if nb_pred == 1 else 'Low',
            'tree': 'High' if tree_pred == 1 else 'Low',
            'nn': 'High' if nn_pred == 1 else 'Low'
        }
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
