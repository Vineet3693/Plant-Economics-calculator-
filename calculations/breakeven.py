
"""Break-even analysis calculations"""
import pandas as pd

def calculate_breakeven_units(fixed_costs, selling_price_per_unit, variable_cost_per_unit):
    """Calculate break-even point in units"""
    contribution_margin = selling_price_per_unit - variable_cost_per_unit
    breakeven_units = fixed_costs / contribution_margin
    breakeven_sales = breakeven_units * selling_price_per_unit
    
    return {
        'breakeven_units': breakeven_units,
        'breakeven_sales': breakeven_sales,
        'contribution_margin_per_unit': contribution_margin,
        'contribution_margin_ratio': contribution_margin / selling_price_per_unit
    }

def profit_at_volume(fixed_costs, selling_price_per_unit, variable_cost_per_unit, volume):
    """Calculate profit at given volume"""
    contribution_margin = selling_price_per_unit - variable_cost_per_unit
    total_contribution = volume * contribution_margin
    profit = total_contribution - fixed_costs
    
    return {
        'volume': volume,
        'profit': profit,
        'total_revenue': volume * selling_price_per_unit,
        'total_variable_costs': volume * variable_cost_per_unit,
        'analysis_volume': volume
    }

def create_breakeven_chart_data(fixed_costs, selling_price, variable_cost, max_volume):
    """Create data for break-even chart"""
    breakeven_result = calculate_breakeven_units(fixed_costs, selling_price, variable_cost)
    breakeven_units = breakeven_result['breakeven_units']
    
    volumes = list(range(0, int(max_volume) + 1, int(max_volume / 100)))
    
    data = []
    for vol in volumes:
        revenue = vol * selling_price
        total_costs = fixed_costs + (vol * variable_cost)
        
        data.append({
            'Volume': vol,
            'Revenue': revenue,
            'Total_Costs': total_costs,
            'Profit': revenue - total_costs
        })
    
    return pd.DataFrame(data), breakeven_units

def sensitivity_analysis(fixed_costs, selling_price, variable_cost, volume):
    """Simple sensitivity analysis"""
    base_profit = profit_at_volume(fixed_costs, selling_price, variable_cost, volume)['profit']
    
    # Test ±10% changes
    changes = [-10, -5, 0, 5, 10]
    
    sensitivity_results = {
        'sensitivity_analysis': {
            'fixed_costs_sensitivity': [],
            'selling_price_sensitivity': [],
            'variable_cost_sensitivity': [],
            'volume_sensitivity': []
        }
    }
    
    for change in changes:
        # Fixed costs sensitivity
        new_fc = fixed_costs * (1 + change/100)
        new_profit = profit_at_volume(new_fc, selling_price, variable_cost, volume)['profit']
        sensitivity_results['sensitivity_analysis']['fixed_costs_sensitivity'].append({
            'change_percent': change,
            'new_profit': new_profit
        })
        
        # Selling price sensitivity
        new_sp = selling_price * (1 + change/100)
        new_profit = profit_at_volume(fixed_costs, new_sp, variable_cost, volume)['profit']
        sensitivity_results['sensitivity_analysis']['selling_price_sensitivity'].append({
            'change_percent': change,
            'new_profit': new_profit
        })
        
        # Variable cost sensitivity  
        new_vc = variable_cost * (1 + change/100)
        new_profit = profit_at_volume(fixed_costs, selling_price, new_vc, volume)['profit']
        sensitivity_results['sensitivity_analysis']['variable_cost_sensitivity'].append({
            'change_percent': change,
            'new_profit': new_profit
        })
        
        # Volume sensitivity
        new_vol = volume * (1 + change/100)
        new_profit = profit_at_volume(fixed_costs, selling_price, variable_cost, new_vol)['profit']
        sensitivity_results['sensitivity_analysis']['volume_sensitivity'].append({
            'change_percent': change,
            'new_profit': new_profit
        })
    
    return sensitivity_results
