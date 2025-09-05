
"""Profitability analysis calculations"""
import numpy as np
import pandas as pd
from scipy.optimize import fsolve

def calculate_roi(annual_profit, total_investment):
    """Calculate Return on Investment
    
    Args:
        annual_profit (float): Annual profit
        total_investment (float): Total investment
    
    Returns:
        float: ROI as percentage
    """
    if total_investment == 0:
        return 0
    roi = (annual_profit / total_investment) * 100
    return roi

def calculate_payback_period(initial_investment, annual_cash_flow):
    """Calculate Payback Period
    
    Args:
        initial_investment (float): Initial investment
        annual_cash_flow (float): Annual cash inflow
    
    Returns:
        float: Payback period in years
    """
    if annual_cash_flow == 0:
        return float('inf')
    payback_period = initial_investment / annual_cash_flow
    return payback_period

def calculate_npv(cash_flows, discount_rate, initial_investment):
    """Calculate Net Present Value
    
    Args:
        cash_flows (list): List of annual cash flows
        discount_rate (float): Discount rate as decimal
        initial_investment (float): Initial investment (negative)
    
    Returns:
        dict: NPV calculation details
    """
    if isinstance(cash_flows, (int, float)):
        # If uniform cash flow, convert to list
        cash_flows = [cash_flows] * len(range(len(cash_flows))) if hasattr(cash_flows, '__len__') else [cash_flows]
    
    # Calculate present value of each cash flow
    pv_cash_flows = []
    for i, cf in enumerate(cash_flows):
        pv = cf / ((1 + discount_rate) ** (i + 1))
        pv_cash_flows.append(pv)
    
    total_pv = sum(pv_cash_flows)
    npv = total_pv - initial_investment
    
    return {
        'npv': npv,
        'total_pv_inflows': total_pv,
        'initial_investment': initial_investment,
        'pv_cash_flows': pv_cash_flows,
        'discount_rate': discount_rate
    }

def calculate_npv_uniform(annual_cash_flow, discount_rate, project_life, initial_investment):
    """Calculate NPV for uniform annual cash flows
    
    Args:
        annual_cash_flow (float): Uniform annual cash flow
        discount_rate (float): Discount rate as decimal
        project_life (int): Project life in years
        initial_investment (float): Initial investment
    
    Returns:
        dict: NPV calculation details
    """
    if discount_rate == 0:
        total_pv = annual_cash_flow * project_life
    else:
        # Present worth of annuity factor
        pw_factor = ((1 + discount_rate) ** project_life - 1) / (discount_rate * (1 + discount_rate) ** project_life)
        total_pv = annual_cash_flow * pw_factor
    
    npv = total_pv - initial_investment
    
    return {
        'npv': npv,
        'total_pv_inflows': total_pv,
        'initial_investment': initial_investment,
        'annual_cash_flow': annual_cash_flow,
        'project_life': project_life,
        'discount_rate': discount_rate,
        'pw_factor': pw_factor if discount_rate != 0 else project_life
    }

def calculate_irr_uniform(annual_cash_flow, project_life, initial_investment):
    """Calculate Internal Rate of Return for uniform cash flows
    
    Args:
        annual_cash_flow (float): Uniform annual cash flow
        project_life (int): Project life in years
        initial_investment (float): Initial investment
    
    Returns:
        float: IRR as decimal (None if cannot be calculated)
    """
    def npv_equation(rate):
        if rate == 0:
            return annual_cash_flow * project_life - initial_investment
        pw_factor = ((1 + rate) ** project_life - 1) / (rate * (1 + rate) ** project_life)
        return annual_cash_flow * pw_factor - initial_investment
    
    try:
        # Initial guess for IRR
        irr = fsolve(npv_equation, 0.1)[0]
        # Verify the solution
        if abs(npv_equation(irr)) < 1e-6 and irr > -0.99:
            return irr
        else:
            return None
    except:
        return None

def profitability_summary(initial_investment, annual_cash_flow, project_life, discount_rate):
    """Calculate comprehensive profitability analysis
    
    Args:
        initial_investment (float): Initial investment
        annual_cash_flow (float): Annual cash flow
        project_life (int): Project life in years
        discount_rate (float): Discount rate as decimal
    
    Returns:
        dict: Complete profitability analysis
    """
    # Calculate all metrics
    roi = calculate_roi(annual_cash_flow, initial_investment)
    payback = calculate_payback_period(initial_investment, annual_cash_flow)
    npv_result = calculate_npv_uniform(annual_cash_flow, discount_rate, project_life, initial_investment)
    irr = calculate_irr_uniform(annual_cash_flow, project_life, initial_investment)
    
    # Decision criteria
    npv_decision = "Accept" if npv_result['npv'] > 0 else "Reject"
    irr_decision = "Accept" if irr and irr > discount_rate else "Reject"
    payback_decision = "Good" if payback <= project_life / 2 else "Poor"
    
    return {
        'roi_percent': roi,
        'payback_period': payback,
        'npv': npv_result['npv'],
        'irr_decimal': irr,
        'irr_percent': irr * 100 if irr else None,
        'npv_decision': npv_decision,
        'irr_decision': irr_decision,
        'payback_decision': payback_decision,
        'total_cash_inflow': annual_cash_flow * project_life,
        'net_profit': annual_cash_flow * project_life - initial_investment
    }

def create_cash_flow_table(initial_investment, annual_cash_flow, project_life, discount_rate):
    """Create detailed cash flow analysis table
    
    Args:
        initial_investment (float): Initial investment
        annual_cash_flow (float): Annual cash flow
        project_life (int): Project life in years
        discount_rate (float): Discount rate as decimal
    
    Returns:
        pandas.DataFrame: Cash flow analysis table
    """
    years = list(range(0, project_life + 1))
    cash_flows = [-initial_investment] + [annual_cash_flow] * project_life
    
    pv_factors = [1.0] + [1 / ((1 + discount_rate) ** year) for year in range(1, project_life + 1)]
    pv_cash_flows = [cf * pv_factor for cf, pv_factor in zip(cash_flows, pv_factors)]
    
    cumulative_pv = np.cumsum(pv_cash_flows)
    cumulative_cash_flow = np.cumsum(cash_flows)
    
    df = pd.DataFrame({
        'Year': years,
        'Cash_Flow': cash_flows,
        'PV_Factor': pv_factors,
        'Present_Value': pv_cash_flows,
        'Cumulative_PV': cumulative_pv,
        'Cumulative_Cash_Flow': cumulative_cash_flow
    })
    
    return df
