
"""Interest and time value of money calculations"""
import pandas as pd
import numpy as np

def simple_interest(principal, rate, periods):
    """Calculate simple interest"""
    simple_int = principal * rate * periods
    return {
        'simple_interest': simple_int,
        'total_amount': principal + simple_int,
        'principal': principal
    }

def compound_interest(principal, rate, periods):
    """Calculate compound interest"""
    future_value = principal * (1 + rate) ** periods
    compound_int = future_value - principal
    return {
        'future_value': future_value,
        'compound_interest': compound_int,
        'principal': principal,
        'periods': periods
    }

def present_worth(future_value, rate, periods):
    """Calculate present worth"""
    return future_value / (1 + rate) ** periods

def create_cashflow_table(principal, rate, periods, method='compound'):
    """Create cash flow table"""
    data = []
    balance = principal
    
    for year in range(periods + 1):
        if year == 0:
            data.append({
                'Year': year,
                'Beginning_Balance': 0,
                'Interest_Earned': 0,
                'Ending_Balance': principal
            })
        else:
            interest = balance * rate
            balance = balance + interest
            data.append({
                'Year': year,
                'Beginning_Balance': balance - interest,
                'Interest_Earned': interest,
                'Ending_Balance': balance
            })
    
    return pd.DataFrame(data)
