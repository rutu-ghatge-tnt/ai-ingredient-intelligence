# test/test_analysis.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_analyze_inci():
    payload = {
        "inci_list": [
            "Aqua",
            "Glycerin",
            "Xylitylglucoside",
            "Anhydroxylitol",
            "Xylitol",
            "Sodium Hyaluronate Crosspolymer",
            "Dipalmitoyl Hydroxyproline",
            "Tocopheryl Acetate",
            "Phenoxyethanol",
            "Carbomer",
            "Triethanolamine"
        ]
    }

    response = client.post("/api/analyze-inci", json=payload)
    
    print("\n🔍 Response JSON:\n", response.json())  # Optional for debugging

    assert response.status_code == 200
    assert "branded_ingredients" in response.json()
    assert "unmatched_inci" in response.json()
    assert "conflicts" in response.json()
    assert "overall_confidence" in response.json()
    assert "processing_time" in response.json()
