import streamlit as st

st.title("Авторська стаття")

pages = st.number_input("Кількість сторінок", min_value=1, value=1, step=1)


# Розрахунок оплати
def calculate_payment(pages):
    if pages <= 3:
        return 250
    elif 4 <= pages <= 6:
        return pages * 70
    elif 7 <= pages <= 10:
        return pages * 100
    elif pages <= 11
        return pages * 120


# Відображення результату
if pages:
    payment = calculate_payment(pages)
    st.write("### Розрахунок оплати:")
    st.write(f"Кількість сторінок: {pages}")
    st.write(f"Загальна сума до сплати: {payment} грн")
