import streamlit as st

st.title("Авторська стаття")

# Форма для введення кількості сторінок
num_pages = st.number_input("Введіть кількість сторінок", min_value=1, step=1)

# Розрахунок оплати
def calculate_payment(pages):
    if pages <= 3:
        return 250
    elif 4 <= pages <= 6:
        return 250 + (pages - 3) * 70
    elif 7 <= pages <= 10:
        return 250 + 3 * 70 + (pages - 6) * 100
    else:  # 11+ сторінок
        return 250 + 3 * 70 + 4 * 100 + (pages - 10) * 120

# Відображення результату
if num_pages:
    payment = calculate_payment(num_pages)
    st.write(f"### Розрахунок оплати:")
    st.write(f"Кількість сторінок: {num_pages}")
    st.write(f"Загальна сума до сплати: {payment} грн")

