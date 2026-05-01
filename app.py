import streamlit as st
import joblib
import numpy as np

# تحميل الموديل
model = joblib.load("model.pkl")

# =====================
# 🏷️ عنوان التطبيق
# =====================
st.title("نظام السوبر ماركت")
st.write("تحليل المبيعات + توصيات ذكية للمخزون")

# =====================
# 📥 Inputs
# =====================
quantity = st.number_input("الكمية", 1, 200)
discount = st.number_input("الخصم", 0.0, 1.0)
profit = st.number_input("الربح")

# =====================
# 🧠 Product Selection (Grocery)
# =====================
product = st.selectbox(
    "نوع المنتج (بقالة)",
    ["Rice", "Sugar", "Oil", "Flour", "Milk", "Tea", "Pasta"]
)

# تحويل المنتج إلى One-Hot Encoding
rice = 1 if product == "Rice" else 0
sugar = 1 if product == "Sugar" else 0
oil = 1 if product == "Oil" else 0
flour = 1 if product == "Flour" else 0
milk = 1 if product == "Milk" else 0
tea = 1 if product == "Tea" else 0
pasta = 1 if product == "Pasta" else 0

# =====================
# 🔧 Feature Engineering
# =====================
profit_ratio = profit / (quantity + 1)
discount_impact = discount * quantity

# =====================
# 🚀 Prediction
# =====================
if st.button("تحليل المبيعات"):

    input_data = np.array([[
        quantity,
        discount,
        profit,
        profit_ratio,
        discount_impact,
        5,   # Month (ثابت)
        2,   # DayOfWeek (ثابت)
        0,   # IsWeekend

        rice,
        sugar,
        oil,
        flour,
        milk,
        tea,
        pasta,

        1, 0, 0,   # Segment (ثابت)
        1, 0, 0, 0  # Region + Ship Mode (ثابت)
    ]])

    prediction = model.predict(input_data)[0]

    # =====================
    # 📊 Dashboard
    # =====================
    st.subheader("📊 النتائج")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 المبيعات المتوقعة", round(prediction, 2))
    col2.metric("📦 الكمية", quantity)
    col3.metric("💵 الربح", profit)

    # =====================
    # 🧠 تحليل ذكي
    # =====================
    st.subheader("🧠 تحليل ذكي")

    if prediction > 500:
        st.success("🟢 منتج عالي الطلب → زوّد المخزون")
    elif prediction > 200:
        st.warning("🟡 طلب متوسط → راقب المخزون")
    else:
        st.error("🔴 طلب ضعيف → قلل المخزون")

    # =====================
    # 💡 توصيات
    # =====================
    st.subheader("💡 توصيات")

    if discount > 0.5:
        st.info("⚠️ الخصم عالي → قد يقلل الأرباح")

    if quantity > 80 and prediction > 300:
        st.success("📦 منتج قوي → يحتاج مخزون أعلى")

    if profit_ratio < 5:
        st.info("💰 الربحية ضعيفة → راجع التسعير")