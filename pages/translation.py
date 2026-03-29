import streamlit as st

from utils.calculate import (
    calculate_editor_payment,
    calculate_redacted_percentage,
    calculate_translation_payment,
)
from utils.utils import total_edit_stats

st.title("Оплата перекладу")

uploaded_file = st.file_uploader("Завантажте файл DOCX", type="docx")

if uploaded_file is None:
    st.warning("Будь ласка, завантажте файл DOCX для аналізу")
else:
    stats_df = total_edit_stats(uploaded_file)
    stats = stats_df.set_index("Показник")["Значення"]
    redacted_percentage = calculate_redacted_percentage(
        stats.at["Змінено слів"],
        stats.at["Змінено форматування"],
        stats.at["Загальна кількість слів"],
    )
    total_characters = stats.at["Загальна кількість символів з пробілами"]

    st.subheader("Статистика")
    st.dataframe(stats_df, hide_index=True)
    st.write(f"Відсоток редагування: {redacted_percentage:.2f}%")
    st.write(f"Кількість символів з пробілами: {int(total_characters)}")

    rank = st.radio(
        "Виберіть звання:",
        options=[0, 1],
        format_func=lambda x: "Старшина" if x == 0 else "Стандартний тариф",
        horizontal=True,
    )

    payment_df = calculate_translation_payment(total_characters, rank)
    st.dataframe(payment_df, hide_index=True)

    payment_df = calculate_editor_payment(total_characters, redacted_percentage)
    st.dataframe(payment_df, hide_index=True)
