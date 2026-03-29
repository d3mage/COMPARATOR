import math

import pandas as pd


def calculate_editor_payment(
    total_characters: int, redacted_percentage: float
) -> pd.DataFrame:
    """
    Calculate payment for editing work.

    Args:
        total_characters: Number of characters including spaces
        redacted_percentage: Percentage of content that was redacted/edited

    Returns:
        DataFrame with payment breakdown
    """
    RATE_PER_1000 = 20

    if redacted_percentage < 10:
        coefficient = 1.0
    elif redacted_percentage < 20:
        coefficient = 1.2
    elif redacted_percentage < 30:
        coefficient = 1.4
    else:
        coefficient = 1.6

    base_pay = math.ceil(total_characters / 1000) * RATE_PER_1000
    result = round(base_pay * coefficient, 2)

    return pd.DataFrame(
        {
            "Показник": ["Базова оплата", "Коефіцієнт", "Результат"],
            "Значення": [base_pay, coefficient, result],
        }
    )


def calculate_translation_payment(total_characters: int, rank: int) -> pd.DataFrame:
    """
    Calculate payment for translation work.

    Args:
        total_characters: Number of characters including spaces
        rank: 0 for "Старшина", 1 for standard translation rate

    Returns:
        DataFrame with payment breakdown
    """
    RATE_PER_1000 = 65 if rank == 0 else 50
    result = math.ceil(total_characters / 1000) * RATE_PER_1000

    return pd.DataFrame(
        {
            "Показник": ["Тариф за 1000 символів", "Кількість символів", "Результат"],
            "Значення": [RATE_PER_1000, total_characters, result],
        }
    )


def calculate_redacted_percentage(
    edit_distance: float, formatting_changes: float, total_words: float
) -> float:
    """
    Calculate the redacted percentage based on edit statistics.

    Args:
        edit_distance: Number of edit operations
        formatting_changes: Number of formatting changes
        total_words: Total number of words in the document

    Returns:
        Redacted percentage as a float
    """
    return (edit_distance + 0.25 * formatting_changes) / total_words * 100
