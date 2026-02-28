import streamlit as st
import pandas as pd
import joblib
import psycopg2
from datetime import datetime
import os


PIPELINE_PATH = os.getenv("PIPELINE_PATH", "/models/churn_pipeline.pkl")
pipeline = joblib.load(PIPELINE_PATH)

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "churn_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

def save_prediction(row: dict):
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO predictions (
            tenure, monthlycharges, totalcharges,
            contract, internetservice, paymentmethod,
            techsupport, onlinesecurity, onlinebackup,
            deviceprotection, streamingtv, streamingmovies,
            paperlessbilling, partner, dependents, gender,
            churn_probability, risk_level, created_at
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            row["tenure"], row["MonthlyCharges"], row["TotalCharges"],
            row["Contract"], row["InternetService"], row["PaymentMethod"],
            row["TechSupport"], row["OnlineSecurity"], row["OnlineBackup"],
            row["DeviceProtection"], row["StreamingTV"], row["StreamingMovies"],
            row["PaperlessBilling"], row["Partner"], row["Dependents"], row["gender"],
            row["churn_probability"], row["risk_level"], row["created_at"]
        )
    )
    conn.commit()
    cur.close()
    conn.close()

st.title("Telecom Churn Prediction")

with st.form("form"):
    tenure = st.slider("Tenure (months)", 1, 72, 12)
    monthly = st.number_input("Monthly Charges", 18.0, 200.0, 70.0)
    total = st.number_input("Total Charges", 0.0, 20000.0, 1400.0)

    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    payment = st.selectbox(
        "Payment Method",
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    )
    techsupport = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    onlinesec = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    onlinebackup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
    deviceprot = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
    streamtv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    streammovies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
    paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    gender = st.selectbox("Gender", ["Male", "Female"])

    submitted = st.form_submit_button("Predict")

    if submitted:
        X_input = pd.DataFrame([{
            "tenure": tenure,
            "MonthlyCharges": monthly,
            "TotalCharges": total,
            "Contract": contract,
            "InternetService": internet,
            "PaymentMethod": payment,
            "TechSupport": techsupport,
            "OnlineSecurity": onlinesec,
            "OnlineBackup": onlinebackup,
            "DeviceProtection": deviceprot,
            "StreamingTV": streamtv,
            "StreamingMovies": streammovies,
            "PaperlessBilling": paperless,
            "Partner": partner,
            "Dependents": dependents,
            "gender": gender
        }])

        prob = float(pipeline.predict_proba(X_input)[0][1])

        st.metric("Churn probability", f"{prob*100:.2f}%")

        # Risk categorization
        if prob >= 0.70:
            risk = "High"
            st.error("🔴 High Churn Risk — Immediate retention action recommended")
        elif prob >= 0.40:
            risk = "Medium"
            st.warning("🟠 Medium Churn Risk — Monitor customer")
        else:
            risk = "Low"
            st.success("🟢 Low Churn Risk — Stable customer")

        # Save to DB
        row = X_input.iloc[0].to_dict()
        row["churn_probability"] = prob
        row["risk_level"] = risk
        row["created_at"] = datetime.utcnow()

        try:
            save_prediction(row)
            st.caption("✅ Saved to database.")
        except Exception as e:
            st.caption(f"⚠️ Not saved to DB: {e}")
