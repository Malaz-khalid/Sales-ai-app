import streamlit as st
import joblib
import numpy as np

model = joblib.load("model.pkl")

st.title("نظام ذكاء المبيعات")

quantity = st.number_input("الكمية", 1, 100)
discount = st.number_input("الخصم", 0.0, 1.0)
profit = st.number_input("الربح")

# ميزات مشتقة (لازم تكون موجودة زي التدريب)
profit_ratio = profit / (quantity + 1)
discount_impact = discount * quantity

if st.button("توقع"):
    input_data = np.array([[
        quantity,
        discount,
        profit,
        profit_ratio,
        discount_impact
    ]])

    prediction = model.predict(input_data)
    st.success(f"المبيعات المتوقعة: {prediction[0]:.2f}")