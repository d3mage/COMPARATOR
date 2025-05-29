import streamlit as st

st.title("Авторська стаття")

pages = st.number_input("Кількість сторінок", min_value=1, value=1, step=1)


# Розрахунок оплати
def calculate_payment(pages):
    base = 250
    if pages <= 3:
        return base
    elif pages <= 6:
        return base + (pages - 3) * 70
    elif pages <= 10:
        return base + 3 * 70 + (pages - 6) * 100
    else:
        return base + 3 * 70 + 4 * 100 + (pages - 10) * 120


# Відображення результату
if pages:
    payment = calculate_payment(pages)
    st.write("### Розрахунок оплати:")
    st.write(f"Кількість сторінок: {pages}")
    st.write(f"Загальна сума до сплати: {payment} грн")
