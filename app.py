import streamlit as st
import joblib
import numpy as np

# =====================
# 📦 تحميل الموديل
# =====================
model = joblib.load("model.pkl")

# =====================
# 🏷️ العنوان
# =====================
st.title("نظام السوبر ماركت")
st.write("تحليل المبيعات + التسعير + المخزون")

# =====================
# 📥 المدخلات الأساسية
# =====================
quantity = st.number_input("الكمية", 1, 200)
discount = st.number_input("الخصم", 0.0, 1.0)

# =====================
# 💰 التسعير
# =====================
cost_price = st.number_input("سعر الشراء", 1.0)
selling_price = st.number_input("سعر البيع", 1.0)

# =====================
# 🛒 نوع المنتج (بقالة)
# =====================
product = st.selectbox(
    "نوع المنتج",
    ["Rice", "Sugar", "Oil", "Flour", "Milk", "Tea", "Pasta"]
)

# One-Hot Encoding
rice = 1 if product == "Rice" else 0
sugar = 1 if product == "Sugar" else 0
oil = 1 if product == "Oil" else 0
flour = 1 if product == "Flour" else 0
milk = 1 if product == "Milk" else 0
tea = 1 if product == "Tea" else 0
pasta = 1 if product == "Pasta" else 0

# =====================
# 🧠 Features هندسية
# =====================
profit = selling_price - cost_price
profit_ratio = profit / (quantity + 1)
discount_impact = discount * quantity

# =====================
# 🚀 التوقع
# =====================
if st.button("تحليل شامل"):

    input_data = np.array([[
        quantity,
        discount,
        profit,
        profit_ratio,
        discount_impact,
        5,   # Month
        2,   # DayOfWeek
        0,   # IsWeekend

        rice,
        sugar,
        oil,
        flour,
        milk,
        tea,
        pasta,

        1, 0, 0,   # Segment
        1, 0, 0, 0  # Region + Ship Mode
    ]])

    prediction = model.predict(input_data)[0]

    # =====================
    # 📊 Dashboard
    # =====================
    st.subheader("📊 النتائج")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 المبيعات المتوقعة", round(prediction, 2))
    col2.metric("📦 الكمية", quantity)
    col3.metric("💵 الربح", round(profit, 2))

    # =====================
    # 💰 تحليل التسعير
    # =====================
    st.subheader("💰 تحليل التسعير")

    profit_margin = (profit / cost_price) * 100

    st.metric("📊 هامش الربح %", round(profit_margin, 2))

    if profit_margin < 10:
        st.error("🔴 تسعير ضعيف → خسارة أو ربح قليل")
    elif profit_margin < 25:
        st.warning("🟡 تسعير متوسط → يمكن تحسينه")
    else:
        st.success("🟢 تسعير ممتاز")

    # =====================
    # 🧠 تحليل الطلب
    # =====================
    st.subheader("🧠 تحليل الطلب")

    if prediction > 500:
        st.success("🟢 طلب عالي → زوّد المخزون")
    elif prediction > 200:
        st.warning("🟡 طلب متوسط → راقب المخزون")
    else:
        st.error("🔴 طلب ضعيف → قلل المخزون")

    # =====================
    # 💡 توصيات ذكية
    # =====================
    st.subheader("💡 توصيات")

    if discount > 0.5:
        st.info("⚠️ خصم عالي قد يقلل الربح")

    if quantity > 80 and prediction > 300:
        st.success("📦 منتج قوي → يحتاج مخزون أعلى")

    if profit_ratio < 5:
        st.info("💰 الربحية ضعيفة → راجع التسعير")