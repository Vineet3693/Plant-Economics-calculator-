
"""Interest and Time Value of Money calculations"""
import numpy as np
import pandas as pd

def simple_interest(principal, interest_rate, time_periods):
    """Calculate Simple Interest
    
    Args:
        principal (float): Initial investment (P)
        interest_rate (float): Interest rate as decimal (i)
        time_periods (int): Number of periods (n)
    
    Returns:
        dict: Simple interest and total amount
    """
    simple_int = principal * interest_rate * time_periods
    total_amount = principal + simple_int
    
    return {
        'simple_interest': simple_int,
        'total_amount': total_amount,
        'principal': principal,
        'rate': interest_rate,
        'periods': time_periods
    }

def compound_interest(principal, interest_rate, time_periods):
    """Calculate Compound Interest (Future Value)
    
    Args:
        principal (float): Initial investment (P)
        interest_rate (float): Interest rate as decimal (i)
        time_periods (int): Number of periods (n)
    
    Returns:
        dict: Future value and compound interest
    """
    future_value = principal * (1 + interest_rate) ** time_periods
    compound_int = future_value - principal
    
    return {
        'future_value': future_value,
        'compound_interest': compound_int,
        'principal': principal,
        'rate': interest_rate,
        'periods': time_periods
    }

def present_worth(future_value, interest_rate, time_periods):
    """Calculate Present Worth
    
    Args:
        future_value (float): Future amount (F)
        interest_rate (float): Interest rate as decimal (i)
        time_periods (int): Number of periods (n)
    
    Returns:
        float: Present worth value
    """
    present_value = future_value / ((1 + interest_rate) ** time_periods)
    return present_value

def uniform_series_present_worth(annual_payment, interest_rate, time_periods):
    """Calculate Present Worth of Uniform Series (Annuity)
    
    Args:
        annual_payment (float): Annual payment (A)
        interest_rate (float): Interest rate as decimal (i)
        time_periods (int): Number of periods (n)
    
    Returns:
        float: Present worth of annuity
    """
    if interest_rate == 0:
        return annual_payment * time_periods
    
    factor = ((1 + interest_rate) ** time_periods - 1) / (interest_rate * (1 + interest_rate) ** time_periods)
    present_worth_annuity = annual_payment * factor
    return present_worth_annuity

def uniform_series_future_worth(annual_payment, interest_rate, time_periods):
    """Calculate Future Worth of Uniform Series
    
    Args:
        annual_payment (float): Annual payment (A)
        interest_rate (float): Interest rate as decimal (i)
        time_periods (int): Number of periods (n)
    
    Returns:
        float: Future worth of annuity
    """
    if interest_rate == 0:
        return annual_payment * time_periods
    
    factor = ((1 + interest_rate) ** time_periods - 1) / interest_rate
    future_worth_annuity = annual_payment * factor
    return future_worth_annuity

def create_cashflow_table(principal, interest_rate, time_periods, payment_type='compound'):
    """Create cash flow table for visualization
    
    Args:
        principal (float): Initial investment
        interest_rate (float): Interest rate as decimal
        time_periods (int): Number of periods
        payment_type (str): 'simple', 'compound', or 'annuity'
    
    Returns:
        pandas.DataFrame: Cash flow table
    """
    years = list(range(0, time_periods + 1))
    
    if payment_type == 'simple':
        values = [principal + (principal * interest_rate * year) for year in years]
    elif payment_type == 'compound':
        values = [principal * (1 + interest_rate) ** year for year in years]
    else:  # annuity
        values = [0] + [uniform_series_present_worth(principal, interest_rate, year) for year in range(1, time_periods + 1)]
    
    df = pd.DataFrame({
        'Year': years,
        'Value': values,
        'Interest_Earned': [val - principal if year > 0 else 0 for year, val in zip(years, values)]
    })
    
    return df
