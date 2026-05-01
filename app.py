import streamlit as st
import joblib
import pandas as pd

model = joblib.load("model.pkl")

st.title("🇸🇩 نظام ذكاء المبيعات")

# إدخالات أساسية
quantity = st.number_input("Quantity", 1, 100)
discount = st.number_input("Discount", 0.0, 1.0)
profit = st.number_input("Profit")

# Features مشتقة
profit_ratio = profit / (quantity + 1)
discount_impact = discount * quantity

# ثابتة (ممكن نخليها اختيار أو قيم افتراضية)
month = 5
dayofweek = 2
is_weekend = 0

# القيم الفئوية (اختياري نخلي default واحد)
data = pd.DataFrame([{
    "Quantity": quantity,
    "Discount": discount,
    "Profit": profit,
    "ProfitRatio": profit_ratio,
    "DiscountImpact": discount_impact,
    "Month": month,
    "DayOfWeek": dayofweek,
    "IsWeekend": is_weekend,

    "Category_Furniture": 0,
    "Category_Office Supplies": 1,
    "Category_Technology": 0,

    "Segment_Consumer": 1,
    "Segment_Corporate": 0,
    "Segment_Home Office": 0,

    "Region_Central": 1,
    "Region_East": 0,
    "Region_South": 0,
    "Region_West": 0,

    "Ship Mode_First Class": 0,
    "Ship Mode_Same Day": 0,
    "Ship Mode_Second Class": 0,
    "Ship Mode_Standard Class": 1
}])

if st.button("Predict"):
    prediction = model.predict(data)
    st.success(f"📊 Sales Prediction: {prediction[0]:.2f}")