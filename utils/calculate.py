import math
import pandas as pd


def calculate_editor_payment(pages: int, redacted_percentage: float) -> pd.DataFrame:
    """
    Calculate payment for editing work.
    
    Args:
        pages: Number of pages
        redacted_percentage: Percentage of content that was redacted/edited
        
    Returns:
        DataFrame with payment breakdown
    """
    BASE = 200
    PER_PAGE = 20
    
    base_pay = BASE + pages * PER_PAGE
    redact_pay = math.ceil(redacted_percentage) * 20
    result = base_pay + redact_pay
    
    return pd.DataFrame({
        "Metric": ["Base Pay", "Redact Pay", "Result"],
        "Value": [base_pay, redact_pay, result]
    })


def calculate_translation_payment(pages: int, redacted_percentage: float, rank: int) -> pd.DataFrame:
    """
    Calculate payment for translation work.
    
    Args:
        pages: Number of pages
        redacted_percentage: Percentage of content that was redacted/edited
        rank: 0 for "Старшина" (120 per page), 1 for "Рядовий" (100 per page)
        
    Returns:
        DataFrame with payment breakdown
    """
    THRESHOLD = 8
    
    base_per_page = 120 if rank == 0 else 100
    
    base_pay = pages * base_per_page
    penalty = (
        0 if redacted_percentage <= THRESHOLD 
        else (redacted_percentage - THRESHOLD) * 2
    )
    result = base_pay - penalty
    
    return pd.DataFrame({
        "Metric": ["Base Pay", "Penalty", "Result"],
        "Value": [base_pay, penalty, result]
    })


def calculate_redacted_percentage(edit_distance: float, formatting_changes: float, total_words: float) -> float:
    """
    Calculate the redacted percentage based on edit statistics.
    
    Args:
        edit_distance: Number of edit operations
        formatting_changes: Number of formatting changes
        total_words: Total number of words in the document
        
    Returns:
        Redacted percentage as a float
    """
    return ((edit_distance + 0.25 * formatting_changes) / total_words * 100)
