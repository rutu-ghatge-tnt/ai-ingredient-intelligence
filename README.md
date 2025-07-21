# 🧠 AI-Powered Ingredient Intelligence
**Identifying Branded Complexes from INCI Lists using AI**

This is the backend for an AI-powered tool that analyzes skincare product ingredient lists (INCI) and intelligently detects branded ingredient complexes using rule-based, graph-based, and optionally machine-learning–based techniques.

Frontend is built in **React + TypeScript** using **Bolt AI**. This FastAPI backend is optimized for performance, modularity, and integration with MongoDB and future ML enhancements.

---

## 🚀 Features

- 🔎 Match branded ingredients based on INCI subsets
- ⚖️ Confidence scoring using rules, rarity, position, and graph intelligence
- 🧠 Optional AI model prediction using Scikit-learn or OpenAI
- 🔁 Detect ambiguous/conflicting INCI-to-brand mappings
- 📄 Return unmatched INCI info with common use & category
- 🌐 Full integration with Bolt AI frontend

---

## 🧱 Tech Stack

| Layer         | Technology                     |
|---------------|-------------------------------|
| Backend       | FastAPI (Python)              |
| Database      | MongoDB (Motor async driver)  |
| AI Logic      | Rule-based + Graph (NetworkX) |
| ML (Optional) | Scikit-learn / OpenAI GPT     |
| Frontend      | React + TypeScript (Bolt AI)  |

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-org/ingredient-intelligence.git
cd ingredient-intelligence
"# ai-ingredient-intelligence" 
