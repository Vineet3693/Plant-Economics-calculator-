
"""Depreciation calculation methods"""
import numpy as np
import pandas as pd

def straight_line_depreciation(purchase_cost, salvage_value, useful_life):
    """Calculate Straight Line Depreciation
    
    Args:
        purchase_cost (float): Initial cost (P)
        salvage_value (float): Salvage value (S)
        useful_life (int): Useful life in years (n)
    
    Returns:
        dict: Depreciation details and yearly table
    """
    annual_depreciation = (purchase_cost - salvage_value) / useful_life
    
    # Create yearly depreciation table
    years = list(range(1, useful_life + 1))
    cumulative_dep = [annual_depreciation * year for year in years]
    book_values = [purchase_cost - cum_dep for cum_dep in cumulative_dep]
    
    depreciation_table = pd.DataFrame({
        'Year': years,
        'Annual_Depreciation': [annual_depreciation] * useful_life,
        'Cumulative_Depreciation': cumulative_dep,
        'Book_Value': book_values
    })
    
    return {
        'method': 'Straight Line',
        'annual_depreciation': annual_depreciation,
        'total_depreciation': purchase_cost - salvage_value,
        'depreciation_table': depreciation_table
    }

def declining_balance_depreciation(purchase_cost, salvage_value, useful_life, depreciation_rate=None):
    """Calculate Declining Balance Depreciation
    
    Args:
        purchase_cost (float): Initial cost (P)
        salvage_value (float): Salvage value (S)
        useful_life (int): Useful life in years (n)
        depreciation_rate (float): Depreciation rate (if None, uses 2/n for double declining)
    
    Returns:
        dict: Depreciation details and yearly table
    """
    if depreciation_rate is None:
        depreciation_rate = 2.0 / useful_life
    
    years = []
    annual_dep = []
    cumulative_dep = []
    book_values = []
    
    current_book_value = purchase_cost
    
    for year in range(1, useful_life + 1):
        # Calculate depreciation for this year
        year_depreciation = current_book_value * depreciation_rate
        
        # Ensure book value doesn't go below salvage value
        if current_book_value - year_depreciation < salvage_value:
            year_depreciation = current_book_value - salvage_value
        
        current_book_value -= year_depreciation
        
        years.append(year)
        annual_dep.append(year_depreciation)
        cumulative_dep.append(purchase_cost - current_book_value)
        book_values.append(current_book_value)
    
    depreciation_table = pd.DataFrame({
        'Year': years,
        'Annual_Depreciation': annual_dep,
        'Cumulative_Depreciation': cumulative_dep,
        'Book_Value': book_values
    })
    
    return {
        'method': 'Declining Balance',
        'depreciation_rate': depreciation_rate,
        'total_depreciation': sum(annual_dep),
        'depreciation_table': depreciation_table
    }

def sum_of_years_digits_depreciation(purchase_cost, salvage_value, useful_life):
    """Calculate Sum of Years Digits Depreciation
    
    Args:
        purchase_cost (float): Initial cost (P)
        salvage_value (float): Salvage value (S)
        useful_life (int): Useful life in years (n)
    
    Returns:
        dict: Depreciation details and yearly table
    """
    total_depreciation = purchase_cost - salvage_value
    sum_of_years = sum(range(1, useful_life + 1))
    
    years = []
    annual_dep = []
    cumulative_dep = []
    book_values = []
    
    cumulative_depreciation = 0
    
    for year in range(1, useful_life + 1):
        # Fraction for this year (remaining years / sum of years)
        remaining_years = useful_life - year + 1
        year_fraction = remaining_years / sum_of_years
        year_depreciation = total_depreciation * year_fraction
        
        cumulative_depreciation += year_depreciation
        current_book_value = purchase_cost - cumulative_depreciation
        
        years.append(year)
        annual_dep.append(year_depreciation)
        cumulative_dep.append(cumulative_depreciation)
        book_values.append(current_book_value)
    
    depreciation_table = pd.DataFrame({
        'Year': years,
        'Annual_Depreciation': annual_dep,
        'Cumulative_Depreciation': cumulative_dep,
        'Book_Value': book_values
    })
    
    return {
        'method': 'Sum of Years Digits',
        'sum_of_years': sum_of_years,
        'total_depreciation': total_depreciation,
        'depreciation_table': depreciation_table
    }

def sinking_fund_depreciation(purchase_cost, salvage_value, useful_life, interest_rate):
    """Calculate Sinking Fund Depreciation
    
    Args:
        purchase_cost (float): Initial cost (P)
        salvage_value (float): Salvage value (S)
        useful_life (int): Useful life in years (n)
        interest_rate (float): Interest rate as decimal (i)
    
    Returns:
        dict: Depreciation details and yearly table
    """
    total_depreciation = purchase_cost - salvage_value
    
    # Annual sinking fund payment
    if interest_rate == 0:
        annual_payment = total_depreciation / useful_life
    else:
        annual_payment = total_depreciation * interest_rate / ((1 + interest_rate) ** useful_life - 1)
    
    years = []
    annual_dep = []
    cumulative_dep = []
    book_values = []
    sinking_fund_balance = []
    
    fund_balance = 0
    
    for year in range(1, useful_life + 1):
        # Add annual payment and interest
        fund_balance = (fund_balance + annual_payment) * (1 + interest_rate)
        
        years.append(year)
        annual_dep.append(annual_payment)
        cumulative_dep.append(fund_balance)
        book_values.append(purchase_cost - fund_balance)
        sinking_fund_balance.append(fund_balance)
    
    depreciation_table = pd.DataFrame({
        'Year': years,
        'Annual_Payment': annual_dep,
        'Sinking_Fund_Balance': sinking_fund_balance,
        'Book_Value': book_values
    })
    
    return {
        'method': 'Sinking Fund',
        'annual_payment': annual_payment,
        'interest_rate': interest_rate,
        'total_depreciation': total_depriciation,
    }
