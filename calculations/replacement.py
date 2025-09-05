
"""Equipment replacement analysis"""

def replacement_analysis(old_equipment_cost, old_salvage_value, old_annual_cost,
                        new_equipment_cost, new_salvage_value, new_annual_cost,
                        new_equipment_life, interest_rate, analysis_period):
    """Analyze equipment replacement decision"""
    
    # Present worth of keeping old equipment
    pw_factor_old = ((1 + interest_rate) ** analysis_period - 1) / (interest_rate * (1 + interest_rate) ** analysis_period)
    present_worth_old = old_annual_cost * pw_factor_old
    
    # Present worth of new equipment
    pw_factor_new = ((1 + interest_rate) ** new_equipment_life - 1) / (interest_rate * (1 + interest_rate) ** new_equipment_life)
    present_worth_new = new_equipment_cost + (new_annual_cost * pw_factor_new) - (new_salvage_value / (1 + interest_rate) ** new_equipment_life)
    
    # Net investment
    net_investment = new_equipment_cost - old_salvage_value
    
    # Net savings
    net_savings = present_worth_old - present_worth_new
    annual_savings = old_annual_cost - new_annual_cost
    
    # Equivalent annual costs
    eac_old = present_worth_old / pw_factor_old if pw_factor_old > 0 else old_annual_cost
    eac_new = present_worth_new / pw_factor_new if pw_factor_new > 0 else new_annual_cost
    
    recommendation = "Replace" if net_savings > 0 else "Keep Old"
    
    return {
        'net_investment': net_investment,
        'net_savings': net_savings,
        'annual_savings': annual_savings,
        'present_worth_old': present_worth_old,
        'present_worth_new': present_worth_new,
        'equivalent_annual_cost_old': eac_old,
        'equivalent_annual_cost_new': eac_new,
        'recommendation': recommendation
    }

def economic_life_analysis(equipment_cost, salvage_values, annual_costs, interest_rate):
    """Determine economic life of equipment"""
    eac_analysis = []
    min_eac = float('inf')
    optimal_life = 1
    
    for year in range(1, len(annual_costs) + 1):
        # Calculate present worth of costs
        pw_costs = sum(annual_costs[i] / (1 + interest_rate) ** (i + 1) for i in range(year))
        pw_salvage = salvage_values[year - 1] / (1 + interest_rate) ** year
        
        total_pw = equipment_cost + pw_costs - pw_salvage
        
        # Calculate equivalent annual cost
        pw_factor = ((1 + interest_rate) ** year - 1) / (interest_rate * (1 + interest_rate) ** year)
        eac = total_pw / pw_factor if pw_factor > 0 else total_pw
        
        eac_analysis.append({
            'year': year,
            'equivalent_annual_cost': eac
        })
        
        if eac < min_eac:
            min_eac = eac
            optimal_life = year
    
    return {
        'optimal_economic_life': optimal_life,
        'minimum_equivalent_annual_cost': min_eac,
        'eac_analysis': eac_analysis
    }

def replacement_timing_analysis(current_equipment_age, max_life, current_salvage,
                               annual_costs_old, new_equipment_cost, new_salvage_values,
                               new_annual_costs, interest_rate):
    """Analyze optimal replacement timing"""
    
    replacement_analysis_results = []
    min_pw = float('inf')
    best_timing = "Replace now"
    
    for replace_after_years in range(max_life + 1):
        # Cost of keeping old equipment
        if replace_after_years > 0:
            pw_old_costs = sum(annual_costs_old[i] / (1 + interest_rate) ** (i + 1) for i in range(replace_after_years))
            old_salvage_value = current_salvage * (0.9 ** replace_after_years)  # Declining salvage
        else:
            pw_old_costs = 0
            old_salvage_value = current_salvage
        
        # Cost of new equipment (present worth)
        new_investment = (new_equipment_cost - old_salvage_value) / (1 + interest_rate) ** replace_after_years
        
        # Present worth of new equipment costs
        remaining_life = len(new_annual_costs)
        pw_new_costs = sum(new_annual_costs[i] / (1 + interest_rate) ** (replace_after_years + i + 1) for i in range(remaining_life))
        pw_new_salvage = new_salvage_values[0] / (1 + interest_rate) ** (replace_after_years + remaining_life)
        
        total_pw = pw_old_costs + new_investment + pw_new_costs - pw_new_salvage
        
        replacement_analysis_results.append({
            'replace_after_years': replace_after_years,
            'total_present_worth': total_pw,
            'old_salvage_value': old_salvage_value
        })
        
        if total_pw < min_pw:
            min_pw = total_pw
            best_timing = f"Replace after {replace_after_years} years" if replace_after_years > 0 else "Replace now"
    
    return {
        'recommendation': best_timing,
        'minimum_present_worth': min_pw,
        'replacement_analysis': replacement_analysis_results
    }
