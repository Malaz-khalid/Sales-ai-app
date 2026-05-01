import streamlit as st
import joblib
import numpy as np

# تحميل الموديل
model = joblib.load("model.pkl")

# عنوان التطبيق
st.title("🇸🇩 نظام ذكاء المبيعات للسوبرماركت")
st.write("أدخلي بيانات البيع لمعرفة التوقع")

# مدخلات المستخدم
quantity = st.number_input("الكمية", min_value=1, max_value=100)
discount = st.number_input("الخصم", min_value=0.0, max_value=1.0)
profit = st.number_input("الربح")

# زر التوقع
if st.button("توقع المبيعات"):
    input_data = np.array([[quantity, discount, profit]])
    
    prediction = model.predict(input_data)

    st.success(f"📊 المبيعات المتوقعة: {prediction[0]:.2f}")