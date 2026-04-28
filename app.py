import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="AI Sales System", layout="wide")

# تحميل الموديل
model = joblib.load("sales_model.pkl")

st.title("📊 AI Sales Intelligence System")

# ---------------- INPUT ----------------
st.header("📥 Input Data")

col1, col2, col3 = st.columns(3)

with col1:
    quantity = st.number_input("Quantity", 1, 100, 5)

with col2:
    discount = st.number_input("Discount", 0.0, 1.0, 0.2)

with col3:
    profit = st.number_input("Profit", value=30.0)

category = st.selectbox("Category", ["Furniture", "Office Supplies", "Technology"])
segment = st.selectbox("Segment", ["Consumer", "Corporate", "Home Office"])

# ---------------- PREDICTION ----------------
if st.button("🚀 Predict Sales"):

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

    # ---------------- RESULT ----------------
    st.success(f"💰 Predicted Sales: {prediction:.2f}")

    # ---------------- EXPLAINABLE AI ----------------
    st.subheader("🧠 AI Explanation")

    if discount > 0.5:
        st.warning("⚠ High discount may reduce profit stability")
    elif quantity > 50:
        st.info("📈 High quantity increases sales prediction")
    else:
        st.success("📊 Normal business pattern detected")

    # ---------------- DASHBOARD ----------------
    st.subheader("📊 Mini Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        ax.bar(["Prediction"], [prediction])
        ax.set_ylabel("Sales")
        st.pyplot(fig)

    with col2:
        st.metric("Estimated Sales", f"{prediction:.2f}")
        st.metric("Discount Level", f"{discount}")