# app/utils/ml_predict.py

import joblib
import os
from typing import List, Dict
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Paths
MODEL_PATH = "app/ml/model.joblib"
VECTORIZER_PATH = "app/ml/vectorizer.joblib"
MLB_PATH = "app/ml/mlb.joblib"

# Load model and tools
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
vectorizer = joblib.load(VECTORIZER_PATH) if os.path.exists(VECTORIZER_PATH) else None
mlb = joblib.load(MLB_PATH) if os.path.exists(MLB_PATH) else None

def predict_brands_from_ml(inci_list: List[str]) -> List[Dict]:
    """
    Predict branded ingredients using scikit-learn model.
    Returns list of predictions with confidence.
    """
    if not model or not vectorizer or not mlb:
        return []

    try:
        X = vectorizer.transform([' '.join(inci_list)])
        y_pred = model.predict_proba(X)
        top_indices = y_pred[0].argsort()[::-1][:3]  # Top 3 brands
        predicted_brands = []
        for idx in top_indices:
            brand = mlb.classes_[idx]
            confidence = round(y_pred[0][idx], 3)
            if confidence >= 0.5:
                predicted_brands.append({
                    "product_name": brand,
                    "supplier": "ML Model",
                    "inci_names": inci_list,
                    "confidence_score": confidence,
                    "documentation_url": None,
                    "description": "Predicted by ML model",
                    "functionality_category": None,
                    "chemical_class_category": None
                    })

        return predicted_brands
    except Exception as e:
        print(f"[ML] Prediction error: {str(e)}")
        return []
