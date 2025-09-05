
"""Profitability analysis calculations"""
import pandas as pd
import numpy as np

def calculate_npv_uniform(annual_cash_flow, discount_rate, project_life, initial_investment):
    """Calculate NPV with uniform annual cash flows"""
    pv_factor = ((1 + discount_rate) ** project_life - 1) / (discount_rate * (1 + discount_rate) ** project_life)
    pv_cash_flows = annual_cash_flow * pv_factor
    npv = pv_cash_flows - initial_investment
    
    return {'npv': npv}

def calculate_irr(initial_investment, annual_cash_flow, project_life):
    """Calculate IRR using approximation"""
    # Simple approximation - for exact calculation, use numpy.irr or scipy
    for rate in np.arange(0.01, 0.50, 0.001):
        pv_factor = ((1 + rate) ** project_life - 1) / (rate * (1 + rate) ** project_life)
        npv = annual_cash_flow * pv_factor - initial_investment
        if npv <= 0:
            return rate * 100  # Return as percentage
    return None

def profitability_summary(initial_investment, annual_cash_flow, project_life, discount_rate):
    """Complete profitability analysis"""
    # NPV
    npv_result = calculate_npv_uniform(annual_cash_flow, discount_rate, project_life, initial_investment)
    npv = npv_result['npv']
    
    # IRR
    irr_percent = calculate_irr(initial_investment, annual_cash_flow, project_life)
    
    # ROI
    annual_profit = annual_cash_flow  # Simplified
    roi_percent = (annual_profit / initial_investment) * 100
    
    # Payback Period
    payback_period = initial_investment / annual_cash_flow
    
    return {
        'npv': npv,
        'irr_percent': irr_percent if irr_percent else 0,
        'roi_percent': roi_percent,
        'payback_period': payback_period
    }

def create_cash_flow_table(initial_investment, annual_cash_flow, project_life, discount_rate):
    """Create cash flow analysis table"""
    data = []
    cumulative_pv = -initial_investment
    
    # Year 0
    data.append({
        'Year': 0,
        'Cash_Flow': -initial_investment,
        'Discount_Factor': 1.0,
        'Discounted_Cash_Flow': -initial_investment,
        'Cumulative_PV_Cash_Flow': -initial_investment
    })
    
    # Years 1 to project_life
    for year in range(1, project_life + 1):
        discount_factor = 1 / (1 + discount_rate) ** year
        discounted_cf = annual_cash_flow * discount_factor
        cumulative_pv += discounted_cf
        
        data.append({
            'Year': year,
            'Cash_Flow': annual_cash_flow,
            'Discount_Factor': discount_factor,
            'Discounted_Cash_Flow': discounted_cf,
            'Cumulative_PV_Cash_Flow': cumulative_pv
        })
    
    return pd.DataFrame(data)
