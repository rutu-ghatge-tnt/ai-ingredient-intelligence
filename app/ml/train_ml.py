# app/ml/train_ml.py

import os
import json
import joblib
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, f1_score

def load_data(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # INPUT TEXT = joined INCI names
    texts = [' '.join(item["inci_names"]) for item in data]

    # LABELS = product_name as a list
    labels = [[item["product_name"]] for item in data]

    return texts, labels

def train_model(X_train, Y_train, max_iter=3000):
    base_model = LogisticRegression(max_iter=max_iter)

    # Hyperparameter tuning
    param_grid = {
        "estimator__C": [0.1, 1, 5],
        "estimator__solver": ["lbfgs"]
    }

    ovr_model = OneVsRestClassifier(base_model)
    grid = GridSearchCV(ovr_model, param_grid, cv=3, scoring="f1_micro", verbose=1)
    grid.fit(X_train, Y_train)

    print(f"🏆 Best parameters: {grid.best_params_}")
    return grid.best_estimator_

def evaluate(model, X_test, Y_test, mlb):
    Y_pred = model.predict(X_test)

    print("\n📊 Classification Report:")
    print(classification_report(Y_test, Y_pred, target_names=mlb.classes_))

    acc = accuracy_score(Y_test, Y_pred)
    f1 = f1_score(Y_test, Y_pred, average='micro')

    print(f"✅ Accuracy: {acc:.4f}")
    print(f"✅ Micro F1 Score: {f1:.4f}")
    return acc, f1

def save_artifacts(model, vectorizer, mlb, output_dir="app/ml"):
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(model, os.path.join(output_dir, "model.joblib"))
    joblib.dump(vectorizer, os.path.join(output_dir, "vectorizer.joblib"))
    joblib.dump(mlb, os.path.join(output_dir, "mlb.joblib"))
    print("💾 Model, vectorizer, and label binarizer saved.")

def main(filepath: str):
    print("📦 Loading data...")
    texts, labels = load_data(filepath)

    print("🔤 Vectorizing...")
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    print("🏷️ Binarizing labels...")
    mlb = MultiLabelBinarizer()
    Y = mlb.fit_transform(labels)

    print("🧪 Train-test split...")
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    print("🧠 Training model...")
    model = train_model(X_train, Y_train)

    print("🔍 Evaluating model...")
    evaluate(model, X_test, Y_test, mlb)

    print("💾 Saving artifacts...")
    save_artifacts(model, vectorizer, mlb)

    print("✅ All done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train ML model for branded ingredient recognition.")
    parser.add_argument("--data", type=str, default="app/data/sample_data.json", help="Path to training data file.")
    args = parser.parse_args()
    main(args.data)
