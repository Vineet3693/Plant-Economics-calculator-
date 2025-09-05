
"""Replacement and salvage value calculations"""
import numpy as np
import pandas as pd

def calculate_salvage_value(purchase_cost, depreciation_method, useful_life, current_age, 
                          salvage_rate=0.10, interest_rate=0.10):
    """Calculate current salvage value of equipment
    
    Args:
        purchase_cost (float): Original purchase cost
        depreciation_method (str): Depreciation method used
        useful_life (int): Total useful life
        current_age (int): Current age of equipment
        salvage_rate (float): Salvage value as percentage of original cost
        interest_rate (float): Interest rate for sinking fund method
    
    Returns:
        dict: Salvage value calculation details
    """
    if current_age >= useful_life:
        return {
            'current_salvage_value': purchase_cost * salvage_rate,
            'book_value': purchase_cost * salvage_rate,
            'method': depreciation_method,
            'status': 'Fully Depreciated'
        }
    
    # Import depreciation functions
    from . import depreciation
    
    if depreciation_method.lower() == 'straight line':
        dep_result = depreciation.straight_line_depreciation(
            purchase_cost, purchase_cost * salvage_rate, useful_life
        )
    elif depreciation_method.lower() == 'declining balance':
        dep_result = depreciation.declining_balance_depreciation(
            purchase_cost, purchase_cost * salvage_rate, useful_life
        )
    elif depreciation_method.lower() == 'sum of years digits':
        dep_result = depreciation.sum_of_years_digits_depreciation(
            purchase_cost, purchase_cost * salvage_rate, useful_life
        )
    elif depreciation_method.lower() == 'sinking fund':
        dep_result = depreciation.sinking_fund_depreciation(
            purchase_cost, purchase_cost * salvage_rate, useful_life, interest_rate
        )
    else:
        # Default to straight line
        dep_result = depreciation.straight_line_depreciation(
            purchase_cost, purchase_cost * salvage_rate, useful_life
        )
    
    # Get book value at current age
    dep_table = dep_result['depreciation_table']
    if current_age <= len(dep_table):
        current_book_value = dep_table.iloc[current_age - 1]['Book_Value']
    else:
        current_book_value = purchase_cost * salvage_rate
    
    return {
        'current_salvage_value': current_book_value,
        'book_value': current_book_value,
        'original_cost': purchase_cost,
        'current_age': current_age,
        'useful_life': useful_life,
        'depreciation_method': depreciation_method,
        'accumulated_depreciation': purchase_cost - current_book_value
    }

def replacement_analysis(old_equipment_cost, old_salvage_value, old_annual_cost,
                        new_equipment_cost, new_salvage_value, new_annual_cost,
                        new_equipment_life, interest_rate, analysis_period=None):
    """Perform equipment replacement economic analysis
    
    Args:
        old_equipment_cost (float): Current book value of old equipment
        old_salvage_value (float): Current salvage value of old equipment
        old_annual_cost (float): Annual operating cost of old equipment
        new_equipment_cost (float): Purchase cost of new equipment
        new_salvage_value (float): Salvage value of new equipment at end of life
        new_annual_cost (float): Annual operating cost of new equipment
        new_equipment_life (int): Life of new equipment
        interest_rate (float): Interest rate for analysis
        analysis_period (int): Analysis period (if None, uses new equipment life)
    
    Returns:
        dict: Replacement analysis results
    """
    if analysis_period is None:
        analysis_period = new_equipment_life
    
    # Calculate present worth of keeping old equipment
    pw_old_annual_costs = old_annual_cost * present_worth_annuity_factor(interest_rate, analysis_period)
    pw_old_total = pw_old_annual_costs  # No initial investment (already owned)
    
    # Calculate present worth of new equipment
    net_investment = new_equipment_cost - old_salvage_value
    pw_new_annual_costs = new_annual_cost * present_worth_annuity_factor(interest_rate, analysis_period)
    pw_new_salvage = new_salvage_value / ((1 + interest_rate) ** analysis_period)
    pw_new_total = net_investment + pw_new_annual_costs - pw_new_salvage
    
    # Calculate equivalent annual costs
    eac_old = pw_old_total / present_worth_annuity_factor(interest_rate, analysis_period)
    eac_new = pw_new_total / present_worth_annuity_factor(interest_rate, analysis_period)
    
    savings = pw_old_total - pw_new_total
    annual_savings = eac_old - eac_new
    
    recommendation = "Replace" if savings > 0 else "Keep Old"
    
    return {
        'present_worth_old': pw_old_total,
        'present_worth_new': pw_new_total,
        'net_savings': savings,
        'equivalent_annual_cost_old': eac_old,
        'equivalent_annual_cost_new': eac_new,
        'annual_savings': annual_savings,
        'net_investment': net_investment,
        'recommendation': recommendation,
        'analysis_period': analysis_period,
        'interest_rate': interest_rate
    }

def present_worth_annuity_factor(interest_rate, periods):
    """Calculate present worth annuity factor
    
    Args:
        interest_rate (float): Interest rate as decimal
        periods (int): Number of periods
    
    Returns:
        float: Present worth annuity factor
    """
    if interest_rate == 0:
        return periods
    return ((1 + interest_rate) ** periods - 1) / (interest_rate * (1 + interest_rate) ** periods)

def economic_life_analysis(equipment_cost, salvage_values, annual_costs, interest_rate):
    """Determine economic life of equipment
    
    Args:
        equipment_cost (float): Initial equipment cost
        salvage_values (list): Salvage values for each year
        annual_costs (list): Annual operating costs for each year
        interest_rate (float): Interest rate for analysis
    
    Returns:
        dict: Economic life analysis results
    """
    years = len(annual_costs)
    equivalent_annual_costs = []
    
    for n in range(1, years + 1):
        # Present worth of costs
        pw_operating = sum(annual_costs[i] / ((1 + interest_rate) ** (i + 1)) for i in range(n))
        pw_initial = equipment_cost
        pw_salvage = salvage_values[n-1] / ((1 + interest_rate) ** n)
        
        total_pw = pw_initial + pw_operating - pw_salvage
        
        # Calculate equivalent annual cost
        pw_factor = present_worth_annuity_factor(interest_rate, n)
        eac = total_pw / pw_factor
        
        equivalent_annual_costs.append({
            'year': n,
            'equivalent_annual_cost': eac,
            'present_worth_total': total_pw,
            'present_worth_operating': pw_operating,
            'present_worth_salvage': pw_salvage
        })
    
    # Find minimum EAC
    min_eac_index = min(range(len(equivalent_annual_costs)), 
                       key=lambda i: equivalent_annual_costs[i]['equivalent_annual_cost'])
    optimal_life = equivalent_annual_costs[min_eac_index]['year']
    minimum_eac = equivalent_annual_costs[min_eac_index]['equivalent_annual_cost']
    
    return {
        'optimal_economic_life': optimal_life,
        'minimum_equivalent_annual_cost': minimum_eac,
        'eac_analysis': equivalent_annual_costs,
        'equipment_cost': equipment_cost,
        'interest_rate': interest_rate
    }

def replacement_timing_analysis(current_equipment_age, max_life, current_salvage, 
                              annual_costs_old, new_equipment_cost, new_salvage_values,
                              new_annual_costs, interest_rate):
    """Analyze optimal timing for equipment replacement
    
    Args:
        current_equipment_age (int): Current age of equipment
        max_life (int): Maximum possible life of current equipment
        current_salvage (float): Current salvage value
        annual_costs_old (list): Projected annual costs for old equipment
        new_equipment_cost (float): Cost of new equipment
        new_salvage_values (list): Salvage values of new equipment by year
        new_annual_costs (list): Annual costs of new equipment
        interest_rate (float): Interest rate for analysis
    
    Returns:
        dict: Replacement timing analysis
    """
    replacement_options = []
    
    for replace_year in range(0, max_life - current_equipment_age + 1):
        # Cost of keeping old equipment for replace_year more years
        if replace_year == 0:
            pw_old_cost = 0
            old_salvage = current_salvage
        else:
            old_costs_period = annual_costs_old[:replace_year]
            pw_old_cost = sum(cost / ((1 + interest_rate) ** (i + 1)) 
                            for i, cost in enumerate(old_costs_period))
            old_salvage = current_salvage * (0.9 ** replace_year)  # Depreciate salvage
        
        # Remaining analysis period
        remaining_period = max_life - replace_year
        
        # Cost of new equipment for remaining period
        if remaining_period > 0 and remaining_period <= len(new_annual_costs):
            new_costs_period = new_annual_costs[:remaining_period]
            pw_new_operating = sum(cost / ((1 + interest_rate) ** (replace_year + i + 1)) 
                                 for i, cost in enumerate(new_costs_period))
            
            new_salvage_pv = (new_salvage_values[remaining_period - 1] / 
                            ((1 + interest_rate) ** (replace_year + remaining_period)))
            
            net_investment = (new_equipment_cost - old_salvage) / ((1 + interest_rate) ** replace_year)
            
            total_pw = pw_old_cost + net_investment + pw_new_operating - new_salvage_pv
        else:
            total_pw = float('inf')  # Not feasible
        
        replacement_options.append({
            'replace_after_years': replace_year,
            'total_present_worth': total_pw,
            'old_equipment_cost': pw_old_cost,
            'net_investment_pv': net_investment if remaining_period > 0 else 0,
            'new_equipment_operating_pv': pw_new_operating if remaining_period > 0 else 0,
            'old_salvage_value': old_salvage
        })
    
    # Find optimal replacement time
    optimal_option = min(replacement_options, key=lambda x: x['total_present_worth'])
    optimal_replace_year = optimal_option['replace_after_years']
    
    return {
        'optimal_replacement_year': optimal_replace_year,
        'minimum_present_worth': optimal_option['total_present_worth'],
        'replacement_analysis': replacement_options,
        'recommendation': f"Replace after {optimal_replace_year} years" if optimal_replace_year > 0 else "Replace immediately"
    }


utils/ai_he
