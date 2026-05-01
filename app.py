import streamlit as st
import joblib
import numpy as np

model = joblib.load("model.pkl")

st.title("🇸🇩 نظام ذكاء السوبرماركت - الإصدار 2")
st.write("Dashboard + توقع + توصيات ذكية")

# =====================
# 📥 Inputs
# =====================
quantity = st.number_input("الكمية", 1, 200)
discount = st.number_input("الخصم", 0.0, 1.0)
profit = st.number_input("الربح")

# Features مشتقة
profit_ratio = profit / (quantity + 1)
discount_impact = discount * quantity

# =====================
# 🔘 Predict
# =====================
if st.button("تحليل النظام"):

    input_data = np.array([[
        quantity,
        discount,
        profit,
        profit_ratio,
        discount_impact,
        5, 2, 0,
        0, 1, 0,
        1, 0, 0,
        1, 0, 0, 0,
        0, 0, 0, 1
    ]])

    prediction = model.predict(input_data)[0]

    # =====================
    # 📊 DASHBOARD
    # =====================
    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 المبيعات", round(prediction, 2))
    col2.metric("📦 الكمية", quantity)
    col3.metric("💵 الربح", profit)

    # =====================
    # 🧠 Business Logic
    # =====================
    st.subheader("🧠 تحليل ذكي")

    # Demand level
    if prediction > 500:
        st.success("🟢 طلب عالي → زوّد المخزون فوراً")
    elif prediction > 200:
        st.warning("🟡 طلب متوسط → راقب المخزون")
    else:
        st.error("🔴 طلب ضعيف → قلل الكمية أو غيّر المنتج")

    # Profit analysis
    if profit_ratio < 5:
        st.info("💡 الربحية ضعيفة → راجع التسعير")

    # Discount insight
    if discount > 0.5:
        st.warning("⚠️ خصم عالي قد يقلل الأرباح")

    # =====================
    # 📦 Inventory Advice
    # =====================
    st.subheader("📦 توصيات المخزون")

    if quantity > 80 and prediction > 300:
        st.success("📦 هذا المنتج Hot → لازم مخزون أعلى")
    elif quantity < 20:
        st.info("📉 حركة ضعيفة → لا تكدّس مخزون")