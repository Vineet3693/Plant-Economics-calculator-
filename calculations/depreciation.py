
"""Depreciation calculation methods"""
import pandas as pd

def straight_line_depreciation(purchase_cost, salvage_value, useful_life):
    """Calculate straight line depreciation"""
    annual_depreciation = (purchase_cost - salvage_value) / useful_life
    total_depreciation = annual_depreciation * useful_life
    
    # Create table
    data = []
    book_value = purchase_cost
    
    for year in range(useful_life + 1):
        if year == 0:
            data.append({
                'Year': year,
                'Annual_Depreciation': 0,
                'Cumulative_Depreciation': 0,
                'Book_Value': purchase_cost
            })
        else:
            cumulative = annual_depreciation * year
            book_value = purchase_cost - cumulative
            data.append({
                'Year': year,
                'Annual_Depreciation': annual_depreciation,
                'Cumulative_Depreciation': cumulative,
                'Book_Value': max(book_value, salvage_value)
            })
    
    return {
        'method': 'Straight Line',
        'annual_depreciation': annual_depreciation,
        'total_depreciation': total_depreciation,
        'depreciation_table': pd.DataFrame(data)
    }

def declining_balance_depreciation(purchase_cost, salvage_value, useful_life, rate=None):
    """Calculate declining balance depreciation"""
    if rate is None:
        rate = 2 / useful_life  # Double declining balance
    
    data = []
    book_value = purchase_cost
    
    for year in range(useful_life + 1):
        if year == 0:
            data.append({
                'Year': year,
                'Annual_Depreciation': 0,
                'Cumulative_Depreciation': 0,
                'Book_Value': purchase_cost
            })
        else:
            depreciation = min(book_value * rate, book_value - salvage_value)
            book_value -= depreciation
            cumulative = purchase_cost - book_value
            
            data.append({
                'Year': year,
                'Annual_Depreciation': depreciation,
                'Cumulative_Depreciation': cumulative,
                'Book_Value': book_value
            })
    
    return {
        'method': 'Declining Balance',
        'depreciation_table': pd.DataFrame(data)
    }

def sum_of_years_digits_depreciation(purchase_cost, salvage_value, useful_life):
    """Calculate sum of years digits depreciation"""
    sum_years = useful_life * (useful_life + 1) / 2
    depreciable_base = purchase_cost - salvage_value
    
    data = []
    cumulative = 0
    
    for year in range(useful_life + 1):
        if year == 0:
            data.append({
                'Year': year,
                'Annual_Depreciation': 0,
                'Cumulative_Depreciation': 0,
                'Book_Value': purchase_cost
            })
        else:
            remaining_life = useful_life - year + 1
            annual_dep = (remaining_life / sum_years) * depreciable_base
            cumulative += annual_dep
            book_value = purchase_cost - cumulative
            
            data.append({
                'Year': year,
                'Annual_Depreciation': annual_dep,
                'Cumulative_Depreciation': cumulative,
                'Book_Value': book_value
            })
    
    return {
        'method': 'Sum of Years Digits',
        'depreciation_table': pd.DataFrame(data)
    }

def sinking_fund_depreciation(purchase_cost, salvage_value, useful_life, interest_rate):
    """Calculate sinking fund depreciation"""
    depreciable_amount = purchase_cost - salvage_value
    annual_payment = depreciable_amount * interest_rate / ((1 + interest_rate) ** useful_life - 1)
    
    return {
        'method': 'Sinking Fund',
        'annual_payment': annual_payment,
        'total_amount': annual_payment * useful_life
    }
