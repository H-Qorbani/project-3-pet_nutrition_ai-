# interface.py

import streamlit as st
from core.recommendation import generate_weight_loss_plan
from analysis import analyze_diet_text

def calculate_rer(weight_kg: float) -> float:
    return round(70 * weight_kg ** 0.75, 2)

def calculate_der(rer: float, species: str, neutered: bool, activity_level: str) -> float:
    factor = 1.6  # default for dog, neutered, normal activity
    if species == 'dog':
        if not neutered:
            factor = 1.8
        if activity_level == 'high':
            factor = 2.0
    elif species == 'cat':
        if not neutered:
            factor = 1.4
        else:
            factor = 1.2
        if activity_level == 'high':
            factor = 1.6
    return round(rer * factor, 2)

def main():
    st.set_page_config(page_title="Pet Nutrition AI Tool", layout="centered")

    st.title("🐾 ابزار هوش مصنوعی تغذیه پت (نسخه آفلاین)")
    st.markdown("ابزار محاسبه کالری، تحلیل رژیم فعلی و پیشنهاد رژیم کاهش وزن برای سگ و گربه")

    with st.form("pet_form"):
        name = st.text_input("نام پت:")
        species = st.selectbox("گونه:", options=["dog", "cat"])
        weight = st.number_input("وزن فعلی (کیلوگرم):", min_value=0.5, step=0.1)
        bcs = st.slider("وضعیت بدنی (BCS)", min_value=1, max_value=9, value=5)
        neutered = st.checkbox("عقیم شده است؟", value=True)
        activity_level = st.selectbox("سطح فعالیت:", options=["low", "normal", "high"])
        diet_text = st.text_area("توضیحات رژیم فعلی (متن آزاد):")
        submitted = st.form_submit_button("محاسبه")

    if submitted:
        st.subheader("📊 نتایج تغذیه‌ای")
        rer = calculate_rer(weight)
        der = calculate_der(rer, species, neutered, activity_level)
        st.write(f"**RER:** {rer} kcal/day")
        st.write(f"**DER:** {der} kcal/day")

        if diet_text.strip():
            try:
                estimated_kcal = analyze_diet_text(diet_text)
                st.write(f"**کالری مصرفی رژیم فعلی (تخمینی):** {estimated_kcal:.2f} kcal/day")
            except FileNotFoundError:
                st.error("❌ فایل داده غذاها پیدا نشد. لطفاً فایل sample_diet_data.json را بررسی کنید.")

        plan = generate_weight_loss_plan(der, species)
        st.subheader("📉 رژیم کاهش وزن پیشنهادی")
        st.write(f"**هدف کالری روزانه:** {plan['target_kcal']} kcal")
        st.write(f"**درصد کاهش از DER:** {plan['reduction_percent']}٪")
        st.info(plan["note"])

if __name__ == "__main__":
    main()
