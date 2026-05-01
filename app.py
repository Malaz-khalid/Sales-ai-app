import streamlit as st
import joblib
import numpy as np

# =====================
# 📦 تحميل الموديل
# =====================
model = joblib.load("model.pkl")

# =====================
# 🏷️ عنوان التطبيق
# =====================
st.title("🇸🇩 نظام ذكاء السوبرماركت - توقع الطلب")
st.write("توقع المبيعات + تحليل المخزون فقط (بدون تسعير)")

# =====================
# 📥 المدخلات
# =====================
quantity = st.number_input("الكمية", 1, 200)
discount = st.number_input("الخصم", 0.0, 1.0)
profit = st.number_input("الربح (اختياري للتحليل فقط)")

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
# 🧠 Features مشتقة
# =====================
profit_ratio = profit / (quantity + 1)
discount_impact = discount * quantity

# =====================
# 🚀 التنبؤ
# =====================
if st.button("تحليل الطلب"):

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
    # 📊 النتائج
    # =====================
    st.subheader("📊 النتائج")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 المبيعات المتوقعة", round(prediction, 2))
    col2.metric("📦 الكمية", quantity)
    col3.metric("💵 الربح (معلومة فقط)", profit)

    # =====================
    # 🧠 تحليل الطلب
    # =====================
    st.subheader("🧠 تحليل المخزون")

    if prediction > 500:
        st.success("🟢 طلب عالي → زوّد المخزون فوراً")
    elif prediction > 200:
        st.warning("🟡 طلب متوسط → راقب المخزون")
    else:
        st.error("🔴 طلب ضعيف → قلل الكمية أو غيّر المنتج")

    # =====================
    # 💡 توصيات تشغيلية
    # =====================
    st.subheader("💡 توصيات")

    if quantity > 80 and prediction > 300:
        st.success("📦 منتج قوي → يحتاج مخزون أعلى")

    if discount > 0.5:
        st.info("⚠️ خصم عالي → راقب تأثيره على الطلب")

    if profit_ratio < 5:
        st.info("📊 ملاحظة: الربحية ضعيفة (للمراقبة فقط)")