import pandas as pd
import joblib
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

def train():
    # Carga de datos
    csv_path = Path('data/russia_losses_equipment.csv')
    df = pd.read_csv(csv_path)

    # Limpieza básica
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.sort_values('day').reset_index(drop=True)

    # Convertimos columnas numéricas
    ignore_cols = ['date', 'greatest losses direction']
    feature_candidates = [col for col in df.columns if col not in ignore_cols]
    for col in feature_candidates:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df[feature_candidates] = df[feature_candidates].fillna(0)

    # Cálculo de variación diaria
    daily = df[feature_candidates].diff().fillna(0)
    daily['day'] = df['day']

    # Variable objetivo binaria: drone
    target_col = 'drone'
    threshold = daily[target_col].median()
    y = (daily[target_col] > threshold).astype(int)

    # Features: todas menos la variable objetivo
    X = daily.drop(columns=[target_col])
    
    # Save feature names for the web form
    feature_names = X.columns.tolist()
    with open('models/features.json', 'w') as f:
        json.dump(feature_names, f)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    metrics = {}

    # 1) KNN
    knn_model = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=7))
    ])
    knn_model.fit(X_train, y_train)
    knn_acc = accuracy_score(y_test, knn_model.predict(X_test))
    joblib.dump(knn_model, 'models/knn_model.joblib')
    metrics['knn'] = {'accuracy': round(knn_acc, 4)}

    # 2) Perceptron
    perceptron_model = Pipeline([
        ('scaler', StandardScaler()),
        ('perceptron', Perceptron(random_state=42, max_iter=2000, tol=1e-3))
    ])
    perceptron_model.fit(X_train, y_train)
    perceptron_acc = accuracy_score(y_test, perceptron_model.predict(X_test))
    joblib.dump(perceptron_model, 'models/perceptron_model.joblib')
    metrics['perceptron'] = {'accuracy': round(perceptron_acc, 4)}

    # 3) Naive Bayes
    # Note: GaussianNB doesn't strictly need scaling but the notebook didn't use a pipeline for it.
    # However, for consistency in the app, I'll keep it as is.
    nb_model = GaussianNB()
    nb_model.fit(X_train, y_train)
    nb_acc = accuracy_score(y_test, nb_model.predict(X_test))
    joblib.dump(nb_model, 'models/nb_model.joblib')
    metrics['nb'] = {'accuracy': round(nb_acc, 4)}

    # Save metrics
    with open('models/metrics.json', 'w') as f:
        json.dump(metrics, f)

    print("Training complete. Models and metrics saved in 'models/'.")

if __name__ == "__main__":
    train()
