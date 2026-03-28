# 📡 Telecom Customer Churn Prediction — Real-Time ML App

## 📌 Overview

This project implements a real-time customer churn prediction system for the telecommunications sector.

The application allows users to input customer characteristics through a web form and receive:

- 🔢 **Predicted churn probability**
- 🚦 **Risk classification** (Low / Medium / High)
- 💾 **Automatic storage** of prediction logs in PostgreSQL

The system is fully containerized using Docker and follows a clean production-style architecture.

---

## 🏗 Architecture

```
User (Browser)
        ↓
Streamlit App (Frontend + Inference)
        ↓
Serialized ML Pipeline (churn_pipeline.pkl)
        ↓
PostgreSQL (Prediction Logs Storage)
```

### Components

| Component | Role |
|---|---|
| **Streamlit** | User interface + model inference |
| **Scikit-learn Pipeline** | Preprocessing + Gradient Boosting classifier |
| **PostgreSQL** | Stores prediction history |
| **Docker & Docker Compose** | Containerized deployment |

---

## 🧠 Machine Learning Model

The predictive system uses a scikit-learn `Pipeline` containing:

- `StandardScaler` (numerical features)
- `OneHotEncoder` (categorical features)
- `GradientBoostingClassifier`

The entire preprocessing and model logic is serialized into:

```
model/churn_pipeline.pkl
```

---

## 📂 Project Structure

```bash
├── app
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── data
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.csv
│   └── customer_churn_telecom_analysis.ipynb
├── db
│   └── init.sql
├── docker-compose.yml
└── model
    └── churn_pipeline.pkl
```

---

## 🚀 How to Run the Project

### 1. Configure Environment Variables

Copy the example file and fill the following values:

```bash
cp .env.example .env
```

The `.env` should look like this:

```env
# PostgreSQL
DB_NAME=your_db_name
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
```

> ⚠️ Never commit `.env` file. It is already listed in `.gitignore`.

### 2. Build and Run

From the root directory:

```bash
docker compose up --build
```

### 3. Access the Application

Open in your browser:

```
http://localhost:8501
```

---

## 📊 Risk Classification Logic

| Probability | Risk Level |
|---|---|
| ≥ 70% | 🔴 High Risk |
| 40% – 69% | 🟠 Medium Risk |
| < 40% | 🟢 Low Risk |


---

## 💾 Database Logging

Each prediction is stored in PostgreSQL with:

- Input customer attributes
- Predicted probability
- Risk level
- Timestamp

**Table:** `predictions`

This enables:

- Audit trail
- Business analytics
- Model monitoring
- Future retraining datasets

### Inspect Stored Predictions

```bash
docker exec -it churn_db psql -U postgres -d churn_db -c "SELECT id, churn_probability, risk_level, created_at FROM predictions ORDER BY id DESC LIMIT 10;"
```

---

### Stop Docker Services

When finished, stop all containers:

```bash
docker compose down
```

## 📚 Technologies Used

| Technology | Version |
|---|---|
| Python | 3.12 |
| Scikit-learn | 1.6.1 |
| Joblib | 1.5.3 |
| Streamlit | latest |
| PostgreSQL | 16 |
| Docker | latest |

---

## 👨‍💻 Author

**Telecom Customer Churn Prediction System**  
Samuel
