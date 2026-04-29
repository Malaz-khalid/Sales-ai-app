from sklearn.metrics import r2_score, mean_absolute_error
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales AI Pro", layout="wide")

# ---------------- LOAD MODEL ----------------
model = joblib.load("sales_model.pkl")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

df_model = df[[
    "Sales","Quantity","Discount","Profit","Category","Segment"
]]

df_model = pd.get_dummies(df_model)

X = df_model.drop("Sales", axis=1)
y = df_model["Sales"]

# ---------------- TITLE ----------------
st.title("📊 Sales AI Intelligence Platform (Pro)")

# ---------------- UPLOAD DATA ----------------
st.sidebar.header("📁 Upload Dataset")
file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if file:
    df_uploaded = pd.read_csv(file)
    st.subheader("📄 Data Preview")
    st.write(df_uploaded.head())

    st.subheader("📊 Basic KPIs")
    st.metric("Total Sales", round(df_uploaded["Sales"].sum(), 2))
    st.metric("Average Sales", round(df_uploaded["Sales"].mean(), 2))

# ---------------- INPUT ----------------
st.subheader("📥 Single Prediction")

quantity = st.number_input("Quantity", 1, 100, 5)
discount = st.number_input("Discount", 0.0, 1.0, 0.2)
profit = st.number_input("Profit", value=30.0)

category = st.selectbox("Category", ["Furniture", "Office Supplies", "Technology"])
segment = st.selectbox("Segment", ["Consumer", "Corporate", "Home Office"])

# ---------------- PREDICT ----------------
if st.button("🚀 Predict"):

    input_data = pd.DataFrame({
        "Quantity": [quantity],
        "Discount": [discount],
        "Profit": [profit],
        "Category_Furniture": [0],
        "Category_Office Supplies": [0],
        "Category_Technology": [0],
        "Segment_Consumer": [0],
        "Segment_Corporate": [0],
        "Segment_Home Office": [0]
    })

    input_data[f"Category_{category}"] = 1
    input_data[f"Segment_{segment}"] = 1

    prediction = model.predict(input_data)[0]

    st.success(f"💰 Predicted Sales: {prediction:.2f}")

    # ---------------- SMART RECOMMENDATIONS ----------------
    st.subheader("💡 Smart Recommendations")

    recommendations = []

    if discount > 0.5:
        recommendations.append("⚠️ Reduce discount to improve profit margins")
    elif discount < 0.1:
        recommendations.append("💡 Increase discount slightly to boost sales")

    if quantity < 10:
        recommendations.append("📦 Increase quantity or offer bundle deals")
    elif quantity > 50:
        recommendations.append("📊 High demand detected — ensure stock availability")

    if category == "Technology":
        recommendations.append("💻 Technology has high revenue potential")
    elif category == "Furniture":
        recommendations.append("🪑 Furniture needs promotions")
    else:
        recommendations.append("📎 Office Supplies are stable")

    if segment == "Corporate":
        recommendations.append("🏢 Corporate customers = bulk orders")
    elif segment == "Consumer":
        recommendations.append("🧑 Focus on consumer marketing")
    else:
        recommendations.append("🏠 Home Office is seasonal")

    for rec in recommendations:
        st.info(rec)

    if len(recommendations) == 0:
        st.success("✅ Optimal settings detected")

    # ---------------- DASHBOARD ----------------
    st.subheader("📊 Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        ax.bar(["Prediction"], [prediction])
        st.pyplot(fig)

    with col2:
        st.metric("Predicted Sales", f"{prediction:.2f}")
        st.metric("Discount", f"{discount}")

    # ---------------- AI EXPLANATION ----------------
    st.subheader("🧠 AI Explanation")

    if discount > 0.5:
        st.warning("High discount may reduce profit")
    elif quantity > 50:
        st.info("High quantity increases demand")
    else:
        st.success("Normal business pattern detected")

# ---------------- MODEL PERFORMANCE (FIXED) ----------------
st.subheader("📊 Model Performance")

if st.button("📊 Evaluate Model"):

    y_pred = model.predict(X)

    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)

    st.write(f"R² Score: {r2:.3f}")
    st.write(f"MAE: {mae:.2f}")

    st.success(f"Estimated Accuracy: {r2*100:.1f}%")