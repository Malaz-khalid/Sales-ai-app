import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales AI Pro", layout="wide")

model = joblib.load("sales_model.pkl")

st.title("📊 Sales AI Intelligence Platform (Pro)")

# ---------------- UPLOAD DATA ----------------
st.sidebar.header("📁 Upload Dataset")
file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.subheader("📄 Data Preview")
    st.write(df.head())

    st.subheader("📊 Basic KPIs")
    st.metric("Total Sales", round(df["Sales"].sum(), 2))
    st.metric("Average Sales", round(df["Sales"].mean(), 2))


# ---------------- INPUT ----------------
st.subheader("📥 Single Prediction")

quantity = st.number_input("Quantity", 1, 100, 5)
discount = st.number_input("Discount", 0.0, 1.0, 0.2)
profit = st.number_input("Profit", value=30.0)

category = st.selectbox("Category", ["Furniture", "Office Supplies", "Technology"])
segment = st.selectbox("Segment", ["Consumer", "Corporate", "Home Office"])


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

if st.button("📄 Download Report"):

    file_path = generate_report(
        prediction, quantity, discount, profit, category, segment
    )

    with open(file_path, "rb") as f:
        st.download_button(
            "⬇ Download PDF",
            f,
            file_name="AI_Report.pdf",
            mime="application/pdf"
        )

    # ---------------- EXPLANATION ----------------
    st.subheader("🧠 AI Explanation")

    if discount > 0.5:
        st.warning("High discount may reduce profit efficiency")
    if quantity > 50:
        st.info("High quantity increases sales probability")
    else:
        st.success("Normal business pattern detected")

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