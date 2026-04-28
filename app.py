import streamlit as st
import pandas as pd
import joblib

# تحميل الموديل
model = joblib.load("sales_model.pkl")

st.title("📊 AI Sales Prediction App")
st.write("Predict sales based on product details")

# Inputs
quantity = st.number_input("Quantity", min_value=1, value=5)
discount = st.number_input("Discount", min_value=0.0, max_value=1.0, value=0.2)
profit = st.number_input("Profit", value=30.0)

category = st.selectbox("Category", ["Furniture", "Office Supplies", "Technology"])
segment = st.selectbox("Segment", ["Consumer", "Corporate", "Home Office"])

if st.button("Predict Sales"):

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

    st.success(f"Predicted Sales: {prediction:.2f}")