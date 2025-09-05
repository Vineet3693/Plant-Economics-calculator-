
"""Input validation functions"""
import streamlit as st

def validate_positive_number(value, field_name):
    """Validate that a number is positive"""
    if value <= 0:
        st.error(f"{field_name} must be greater than 0")
        return False
    return True

def validate_percentage(value, field_name):
    """Validate percentage input (0-100)"""
    if value < 0 or value > 100:
        st.error(f"{field_name} must be between 0 and 100")
        return False
    return True

def validate_years(value):
    """Validate number of years"""
    if value <= 0 or value > 100:
        st.error("Number of years must be between 1 and 100")
        return False
    return True

def validate_salvage_vs_purchase(salvage_value, purchase_cost):
    """Validate that salvage value is less than purchase cost"""
    if salvage_value >= purchase_cost:
        st.error("Salvage value must be less than purchase cost")
        return False
    return True
