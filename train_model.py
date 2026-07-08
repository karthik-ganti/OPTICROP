"""
OptiCrop — one-shot training pipeline.

Loads dataset/Crop_recommendation.csv, preprocesses, trains and compares four
classifiers (KNN, Logistic Regression, Decision Tree, Random Forest), runs a
K-Means elbow analysis, then saves the best model + scaler with pickle:

    models/model.pkl     (best classifier)
    models/scaler.pkl    (StandardScaler)
    models/metrics.txt   (algorithm + accuracy, read by app.py to seed MLModel)

Feature order (must match app.py FEATURE_ORDER):
    N, P, K, temperature, humidity, ph, rainfall
Target: label (22 crops, multi-class).

Note on outliers: the IQR analysis below is reported for insight, and the
notebook demonstrates a log-transform of Potassium (per the spec). The DEPLOYED
model is trained on the raw features + StandardScaler so that training and the
app's inference path stay identical (no train/serve skew).
"""

import os
import pickle
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ── Paths & column config ─────────────────────────────────────────────────────
CSV_CANDIDATES = [
    os.path.join('dataset', 'Crop_recommendation.csv'),
    'Crop_recommendation.csv',
]
FEATURE_COLS = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
TARGET_COL = 'label'

# Accepts common header variants (case-insensitive) -> canonical name
COLUMN_ALIASES = {
    'n': 'N', 'nitrogen': 'N',
    'p': 'P', 'phosphorus': 'P', 'phosphorous': 'P',
    'k': 'K', 'potassium': 'K',
    'temperature': 'temperature', 'temp': 'temperature',
    'humidity': 'humidity',
    'ph': 'ph',
    'rainfall': 'rainfall', 'rain': 'rainfall',
    'label': 'label', 'crop': 'label', 'crops': 'label',
}


def find_dataset():
    for path in CSV_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        'Crop_recommendation.csv not found. Place it in dataset/ and re-run.'
    )


def canonicalize_columns(df):
    renamed = {}
    for col in df.columns:
        key = col.strip().lower()
        if key in COLUMN_ALIASES:
            renamed[col] = COLUMN_ALIASES[key]
    return df.rename(columns=renamed)


def main():
    # ── 1. Load ────────────────────────────────────────────────────────────────
    path = find_dataset()
    print(f'\n[1/7] Loading dataset: {path}')
    df = pd.read_csv(path)
    df = canonicalize_columns(df)
    print(f'      Shape: {df.shape}  |  Columns: {df.columns.tolist()}')

    missing = [c for c in FEATURE_COLS + [TARGET_COL] if c not in df.columns]
    if missing:
        raise ValueError(f'Dataset is missing required columns: {missing}')
    print(f'      Crops ({df[TARGET_COL].nunique()}): {sorted(df[TARGET_COL].unique())}')

    # ── 2. Missing values ──────────────────────────────────────────────────────
    print('\n[2/7] Handling missing values...')
    print('      Missing before:', int(df.isnull().sum().sum()))
    for col in df.columns:
        if df[col].isnull().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col].fillna(df[col].median(), inplace=True)
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)
    print('      Missing after: ', int(df.isnull().sum().sum()))

    # ── 3. Outlier analysis (IQR) — reported only, features kept raw ───────────
    print('\n[3/7] Outlier analysis (IQR, reported for insight)...')
    for col in FEATURE_COLS:
        Q1, Q3 = df[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        lo, hi = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        n = int(((df[col] < lo) | (df[col] > hi)).sum())
        if n:
            print(f'      {col:<12}: {n} potential outlier(s)')
    print('      (Deployed model uses raw features so train/serve stay identical.)')

    # ── 4. Split X / y ─────────────────────────────────────────────────────────
    print('\n[4/7] Splitting features and target...')
    X = df[FEATURE_COLS]
    y = df[TARGET_COL].astype(str)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f'      Train: {X_train.shape[0]}  Test: {X_test.shape[0]}')

    # ── 5. Scale ───────────────────────────────────────────────────────────────
    print('\n[5/7] Scaling features (StandardScaler)...')
    # Fit on .values (plain arrays) so the scaler stores no feature names —
    # this keeps app.py's array-based inference free of sklearn warnings.
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train.values)
    X_test_sc = scaler.transform(X_test.values)

    # ── K-Means elbow analysis (unsupervised; not the deployed predictor) ──────
    print('      Running K-Means elbow analysis...')
    wcss = []
    k_range = range(1, 11)
    for k in k_range:
        km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
        km.fit(X_train_sc)
        wcss.append(km.inertia_)
    try:
        os.makedirs(os.path.join('static', 'images'), exist_ok=True)
        plt.figure(figsize=(7, 4))
        plt.plot(list(k_range), wcss, marker='o', color='#2e7d32')
        plt.title('K-Means Elbow Method')
        plt.xlabel('Number of clusters (k)')
        plt.ylabel('WCSS')
        plt.tight_layout()
        plt.savefig(os.path.join('static', 'images', 'elbow_plot.png'), dpi=110)
        plt.close()
        print('      Saved static/images/elbow_plot.png')
    except Exception as e:
        print(f'      (Skipped elbow plot: {e})')

    # ── 6. Train & compare four classifiers ────────────────────────────────────
    print('\n[6/7] Training & evaluating classifiers...\n')

    def evaluate(name, clf):
        clf.fit(X_train_sc, y_train)
        pred = clf.predict(X_test_sc)
        acc = accuracy_score(y_test, pred)
        print(f'---- {name} {"-" * (40 - len(name))}')
        print(f'     Accuracy : {acc * 100:.2f}%')
        print('     Classification report (weighted avg):')
        rep = classification_report(y_test, pred, output_dict=True, zero_division=0)
        wa = rep['weighted avg']
        print(f'       precision={wa["precision"]:.3f}  recall={wa["recall"]:.3f}  f1={wa["f1-score"]:.3f}')
        return clf, acc

    models = {}
    models['KNN'], knn_acc = evaluate('KNN (k=5)', KNeighborsClassifier(n_neighbors=5))
    models['Logistic Regression'], lr_acc = evaluate(
        'Logistic Regression', LogisticRegression(max_iter=1000, random_state=42))
    models['Decision Tree'], dt_acc = evaluate(
        'Decision Tree', DecisionTreeClassifier(random_state=42))
    models['Random Forest'], rf_acc = evaluate(
        'Random Forest', RandomForestClassifier(n_estimators=100, random_state=42))

    results = {
        'KNN': knn_acc,
        'Logistic Regression': lr_acc,
        'Decision Tree': dt_acc,
        'Random Forest': rf_acc,
    }

    print('\n+----------------------------------------------------+')
    print('|          MODEL PERFORMANCE COMPARISON              |')
    print('+----------------------------------------------------+')
    for name, acc in results.items():
        bar = '#' * int(acc * 40)
        print(f'|  {name:<20} {acc * 100:>6.2f}%  {bar}')
    print('+----------------------------------------------------+')

    best_name = max(results, key=results.get)
    best_acc = results[best_name]
    best_model = models[best_name]
    print(f'\nBest model: {best_name} ({best_acc * 100:.2f}%) — selected for deployment.')

    # Optional: model comparison bar chart for the About page
    try:
        plt.figure(figsize=(7, 4))
        names = list(results.keys())
        accs = [results[n] * 100 for n in names]
        colors = ['#8bc34a', '#66bb6a', '#43a047', '#2e7d32']
        plt.barh(names, accs, color=colors)
        plt.xlim(0, 100)
        plt.xlabel('Accuracy (%)')
        plt.title('Classifier Accuracy Comparison')
        for i, v in enumerate(accs):
            plt.text(v - 8, i, f'{v:.1f}%', va='center', color='white', fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join('static', 'images', 'model_comparison.png'), dpi=110)
        plt.close()
        print('Saved static/images/model_comparison.png')
    except Exception as e:
        print(f'(Skipped comparison chart: {e})')

    # ── 7. Save best model + scaler (pickle) + metrics ─────────────────────────
    print('\n[7/7] Saving artifacts...')
    os.makedirs('models', exist_ok=True)
    with open(os.path.join('models', 'model.pkl'), 'wb') as f:
        pickle.dump(best_model, f)
    with open(os.path.join('models', 'scaler.pkl'), 'wb') as f:
        pickle.dump(scaler, f)
    with open(os.path.join('models', 'metrics.txt'), 'w') as f:
        f.write(f'algorithm={best_name}\naccuracy={round(best_acc * 100, 2)}\n')
    print('      models/model.pkl   OK')
    print('      models/scaler.pkl  OK')
    print('      models/metrics.txt OK')
    print(f'\nFeature order for app.py: {FEATURE_COLS}')
    print('Training complete. Run: python app.py')


if __name__ == '__main__':
    main()
