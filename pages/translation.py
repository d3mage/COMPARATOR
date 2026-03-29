import pandas as pd
import streamlit as st

from utils.calculate import (
    calculate_editor_payment,
    calculate_redacted_percentage,
    calculate_translation_payment,
    calculate_translation_penalty_percentage,
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
        options=[1, 0],
        format_func=lambda x: "Стандартний тариф" if x == 1 else "Старшина",
        horizontal=True,
    )

    payment_df = calculate_translation_payment(total_characters, rank)
    translation_base = float(
        payment_df.loc[payment_df["Показник"] == "Результат", "Значення"].iloc[0]
    )
    translation_penalty_percentage = calculate_translation_penalty_percentage(
        redacted_percentage
    )
    translation_penalty_amount = round(
        translation_base * translation_penalty_percentage / 100, 2
    )
    translation_result = round(translation_base - translation_penalty_amount, 2)

    first_range_penalty = max(min(redacted_percentage, 15) - 5, 0)
    second_range_penalty = max(min(redacted_percentage, 50) - 15, 0)

    st.subheader("Переклад")
    st.caption(
        "Розрахунок зняття: "
        f"0% за перші 5% правок + "
        f"{first_range_penalty:.2f}% x 1% + "
        f"{second_range_penalty:.2f}% x 1.8571% = "
        f"{translation_penalty_percentage:.2f}%"
    )

    payment_df = pd.DataFrame(
        {
            "Показник": [
                "Тариф за 1000 символів",
                "Кількість символів",
                "Базова оплата",
                "Відсоток зняття, %",
                "Штраф, грн",
                "Результат",
            ],
            "Значення": [
                payment_df.loc[
                    payment_df["Показник"] == "Тариф за 1000 символів", "Значення"
                ].iloc[0],
                total_characters,
                translation_base,
                translation_penalty_percentage,
                translation_penalty_amount,
                translation_result,
            ],
        }
    )
    st.dataframe(payment_df, hide_index=True)

    st.subheader("Редактура")
    payment_df = calculate_editor_payment(total_characters, redacted_percentage)
    st.dataframe(payment_df, hide_index=True)
