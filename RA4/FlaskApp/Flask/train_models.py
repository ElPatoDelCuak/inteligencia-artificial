import pandas as pd
import joblib
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import io

def load_and_process_data():
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
    
    return X, y, daily

def generate_plots(daily):
    Path('static/images').mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="darkgrid")
    
    # 1. Distribution of Target
    plt.figure(figsize=(10, 6))
    sns.histplot(daily['drone'], bins=20, kde=True, color='skyblue')
    plt.title('Distribution of Daily Drone Losses Variation', fontsize=14)
    plt.xlabel('Daily Variation')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('static/images/dist_drone.png', dpi=100)
    plt.close()

    # 2. Correlation Heatmap
    plt.figure(figsize=(12, 10))
    corr = daily.corr()
    top_corr_features = corr['drone'].abs().sort_values(ascending=False).head(10).index
    sns.heatmap(daily[top_corr_features].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap (Top 10 Features with Drone)', fontsize=14)
    plt.tight_layout()
    plt.savefig('static/images/heatmap.png', dpi=100)
    plt.close()

    # 3. Boxplot
    plt.figure(figsize=(10, 6))
    threshold = daily['drone'].median()
    is_high = (daily['drone'] > threshold).astype(int)
    top_feature = top_corr_features[1] if len(top_corr_features) > 1 else daily.columns[0]
    
    sns.boxplot(x=is_high, y=daily[top_feature], palette='Set2')
    plt.title(f'{top_feature} vs High Drone Activity', fontsize=14)
    plt.xlabel('High Drone Activity (1=Yes, 0=No)')
    plt.ylabel(top_feature)
    plt.tight_layout()
    plt.savefig('static/images/boxplot.png', dpi=100)
    plt.close()

    print("Plots saved in 'static/images/'.")

def train_and_save_models(X_train, X_test, y_train, y_test):
    metrics = {}
    Path('models').mkdir(parents=True, exist_ok=True)

    def evaluate_and_save(model, name, X_t, y_t, X_v, y_v):
        model.fit(X_t, y_t)
        y_pred = model.predict(X_v)
        acc = accuracy_score(y_v, y_pred)
        prec = precision_score(y_v, y_pred, zero_division=0)
        rec = recall_score(y_v, y_pred, zero_division=0)
        f1 = f1_score(y_v, y_pred, zero_division=0)
        
        joblib.dump(model, f'models/{name}_model.joblib')
        
        return {
            'accuracy': round(float(acc), 4),
            'precision': round(float(prec), 4),
            'recall': round(float(rec), 4),
            'f1': round(float(f1), 4)
        }

    # Models
    knn_model = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=7))
    ])
    metrics['knn'] = evaluate_and_save(knn_model, 'knn', X_train, y_train, X_test, y_test)

    perceptron_model = Pipeline([
        ('scaler', StandardScaler()),
        ('perceptron', Perceptron(random_state=42, max_iter=2000, tol=1e-3))
    ])
    metrics['perceptron'] = evaluate_and_save(perceptron_model, 'perceptron', X_train, y_train, X_test, y_test)

    nb_model = GaussianNB()
    metrics['nb'] = evaluate_and_save(nb_model, 'nb', X_train, y_train, X_test, y_test)

    tree_model = DecisionTreeClassifier(random_state=42, max_depth=5)
    metrics['tree'] = evaluate_and_save(tree_model, 'tree', X_train, y_train, X_test, y_test)

    nn_model = Pipeline([
        ('scaler', StandardScaler()),
        ('mlp', MLPClassifier(hidden_layer_sizes=(10, 5), max_iter=1000, random_state=42))
    ])
    metrics['nn'] = evaluate_and_save(nn_model, 'nn', X_train, y_train, X_test, y_test)

    with open('models/metrics.json', 'w') as f:
        json.dump(metrics, f)

    return metrics

def train_single_model(model_name, params, X_train, y_train, X_test, y_test):
    # (Kept for interactive training)
    if model_name == 'knn':
        model = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=int(params.get('n_neighbors', 7))))
        ])
    elif model_name == 'tree':
        model = DecisionTreeClassifier(
            random_state=42, 
            max_depth=int(params.get('max_depth', 5)) if params.get('max_depth') else None
        )
    elif model_name == 'nn':
        model = Pipeline([
            ('scaler', StandardScaler()),
            ('mlp', MLPClassifier(
                hidden_layer_sizes=eval(params.get('hidden_layer_sizes', '(10, 5)')),
                max_iter=int(params.get('max_iter', 1000)),
                random_state=42
            ))
        ])
    elif model_name == 'perceptron':
        model = Pipeline([
            ('scaler', StandardScaler()),
            ('perceptron', Perceptron(
                random_state=42, 
                max_iter=int(params.get('max_iter', 2000)),
                tol=float(params.get('tol', 1e-3))
            ))
        ])
    elif model_name == 'nb':
        model = GaussianNB()
    else:
        raise ValueError(f"Unknown model: {model_name}")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': round(float(accuracy_score(y_test, y_pred)), 4),
        'precision': round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        'recall': round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        'f1': round(float(f1_score(y_test, y_pred, zero_division=0)), 4)
    }
    
    joblib.dump(model, f'models/{model_name}_model.joblib')
    
    try:
        with open('models/metrics.json', 'r') as f:
            current_metrics = json.load(f)
    except FileNotFoundError:
        current_metrics = {}
        
    current_metrics[model_name] = metrics
    with open('models/metrics.json', 'w') as f:
        json.dump(current_metrics, f)
        
    return metrics

def main():
    X, y, daily = load_and_process_data()
    
    feature_names = X.columns.tolist()
    Path('models').mkdir(parents=True, exist_ok=True)
    with open('models/features.json', 'w') as f:
        json.dump(feature_names, f)

    # Generate plots
    generate_plots(daily)

    # Save Stats (describe)
    stats = daily.describe().to_dict()
    with open('models/stats.json', 'w') as f:
        json.dump(stats, f)

    # Save Examples (first 5 rows)
    examples = daily.head(5).to_dict(orient='records')
    with open('models/examples.json', 'w') as f:
        json.dump(examples, f)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    train_and_save_models(X_train, X_test, y_train, y_test)
    print("Stats and examples saved.")

if __name__ == "__main__":
    main()
