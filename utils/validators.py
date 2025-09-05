
"""Input validation functions"""
import streamlit as st

def validate_positive_number(value, field_name):
    """Validate that a number is positive"""
    if value <= 0:
        st.error(f"{field_name} must be positive")
        return False
    return True

def validate_percentage(value, field_name):
    """Validate percentage values"""
    if not (0 <= value <= 100):
        st.error(f"{field_name} must be between 0 and 100")
        return False
    return True

def validate_years(value):
    """Validate year inputs"""
    if not (1 <= value <= 50):
        st.error("Years must be between 1 and 50")
        return False
    return True

def validate_salvage_vs_purchase(salvage, purchase):
    """Validate salvage value vs purchase cost"""
    if salvage >= purchase:
        st.error("Salvage value must be less than purchase cost")
        return False
    return True
