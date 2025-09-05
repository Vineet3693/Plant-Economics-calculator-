
"""Break-even analysis calculations"""
import numpy as np
import pandas as pd

def calculate_breakeven_units(fixed_costs, selling_price_per_unit, variable_cost_per_unit):
    """Calculate break-even point in units
    
    Args:
        fixed_costs (float): Total fixed costs
        selling_price_per_unit (float): Selling price per unit
        variable_cost_per_unit (float): Variable cost per unit
    
    Returns:
        dict: Break-even analysis results
    """
    if selling_price_per_unit <= variable_cost_per_unit:
        return {'error': 'Selling price must be greater than variable cost per unit'}
    
    contribution_margin = selling_price_per_unit - variable_cost_per_unit
    breakeven_units = fixed_costs / contribution_margin
    breakeven_sales = breakeven_units * selling_price_per_unit
    
    return {
        'breakeven_units': breakeven_units,
        'breakeven_sales': breakeven_sales,
        'contribution_margin_per_unit': contribution_margin,
        'contribution_margin_ratio': contribution_margin / selling_price_per_unit,
        'fixed_costs': fixed_costs,
        'variable_cost_per_unit': variable_cost_per_unit,
        'selling_price_per_unit': selling_price_per_unit
    }

def profit_at_volume(fixed_costs, selling_price_per_unit, variable_cost_per_unit, production_volume):
    """Calculate profit at specific production volume
    
    Args:
        fixed_costs (float): Total fixed costs
        selling_price_per_unit (float): Selling price per unit
        variable_cost_per_unit (float): Variable cost per unit
        production_volume (float): Production volume in units
    
    Returns:
        dict: Profit analysis at given volume
    """
    total_revenue = production_volume * selling_price_per_unit
    total_variable_costs = production_volume * variable_cost_per_unit
    total_costs = fixed_costs + total_variable_costs
    profit = total_revenue - total_costs
    
    contribution_margin = selling_price_per_unit - variable_cost_per_unit
    total_contribution = contribution_margin * production_volume
    
    return {
        'production_volume': production_volume,
        'total_revenue': total_revenue,
        'total_variable_costs': total_variable_costs,
        'total_fixed_costs': fixed_costs,
        'total_costs': total_costs,
        'profit': profit,
        'profit_margin': (profit / total_revenue) * 100 if total_revenue > 0 else 0,
        'contribution_margin_total': total_contribution
    }

def sensitivity_analysis(base_fixed_costs, base_selling_price, base_variable_cost, 
                        base_volume, change_percentages=[-20, -10, 0, 10, 20]):
    """Perform sensitivity analysis on break-even parameters
    
    Args:
        base_fixed_costs (float): Base fixed costs
        base_selling_price (float): Base selling price
        base_variable_cost (float): Base variable cost
        base_volume (float): Base production volume
        change_percentages (list): List of percentage changes to analyze
    
    Returns:
        dict: Sensitivity analysis results
    """
    base_breakeven = calculate_breakeven_units(base_fixed_costs, base_selling_price, base_variable_cost)
    base_profit = profit_at_volume(base_fixed_costs, base_selling_price, base_variable_cost, base_volume)
    
    sensitivity_results = {
        'fixed_costs_sensitivity': [],
        'selling_price_sensitivity': [],
        'variable_cost_sensitivity': [],
        'volume_sensitivity': []
    }
    
    for change_pct in change_percentages:
        change_factor = 1 + (change_pct / 100)
        
        # Fixed costs sensitivity
        new_fixed_costs = base_fixed_costs * change_factor
        fc_breakeven = calculate_breakeven_units(new_fixed_costs, base_selling_price, base_variable_cost)
        fc_profit = profit_at_volume(new_fixed_costs, base_selling_price, base_variable_cost, base_volume)
        sensitivity_results['fixed_costs_sensitivity'].append({
            'change_percent': change_pct,
            'new_breakeven_units': fc_breakeven.get('breakeven_units', 0),
            'new_profit': fc_profit['profit']
        })
        
        # Selling price sensitivity
        new_selling_price = base_selling_price * change_factor
        if new_selling_price > base_variable_cost:
            sp_breakeven = calculate_breakeven_units(base_fixed_costs, new_selling_price, base_variable_cost)
            sp_profit = profit_at_volume(base_fixed_costs, new_selling_price, base_variable_cost, base_volume)
            sensitivity_results['selling_price_sensitivity'].append({
                'change_percent': change_pct,
                'new_breakeven_units': sp_breakeven.get('breakeven_units', 0),
                'new_profit': sp_profit['profit']
            })
        
        # Variable cost sensitivity
        new_variable_cost = base_variable_cost * change_factor
        if new_variable_cost < base_selling_price:
            vc_breakeven = calculate_breakeven_units(base_fixed_costs, base_selling_price, new_variable_cost)
            vc_profit = profit_at_volume(base_fixed_costs, base_selling_price, new_variable_cost, base_volume)
            sensitivity_results['variable_cost_sensitivity'].append({
                'change_percent': change_pct,
                'new_breakeven_units': vc_breakeven.get('breakeven_units', 0),
                'new_profit': vc_profit['profit']
            })
        
        # Volume sensitivity
        new_volume = base_volume * change_factor
        vol_profit = profit_at_volume(base_fixed_costs, base_selling_price, base_variable_cost, new_volume)
        sensitivity_results['volume_sensitivity'].append({
            'change_percent': change_pct,
            'new_volume': new_volume,
            'new_profit': vol_profit['profit']
        })
    
    return {
        'base_breakeven': base_breakeven,
        'base_profit': base_profit,
        'sensitivity_analysis': sensitivity_results
    }

def create_breakeven_chart_data(fixed_costs, selling_price_per_unit, variable_cost_per_unit, max_volume=None):
    """Create data for break-even chart visualization
    
    Args:
        fixed_costs (float): Fixed costs
        selling_price_per_unit (float): Selling price per unit
        variable_cost_per_unit (float): Variable cost per unit
        max_volume (float): Maximum volume for chart (if None, calculated automatically)
    
    Returns:
        pandas.DataFrame: Data for break-even chart
    """
    breakeven_result = calculate_breakeven_units(fixed_costs, selling_price_per_unit, variable_cost_per_unit)
    
    if 'error' in breakeven_result:
        return None
    
    breakeven_units = breakeven_result['breakeven_units']
    
    if max_volume is None:
        max_volume = breakeven_units * 2
    
    # Create volume range
    volumes = np.linspace(0, max_volume, 100)
    
    # Calculate revenue and costs for each volume
    revenues = volumes * selling_price_per_unit
    total_costs = fixed_costs + (volumes * variable_cost_per_unit)
    variable_costs = volumes * variable_cost_per_unit
    fixed_costs_line = [fixed_costs] * len(volumes)
    profits = revenues - total_costs
    
    df = pd.DataFrame({
        'Volume': volumes,
        'Revenue': revenues,
        'Total_Cost': total_costs,
        'Variable_Cost': variable_costs,
        'Fixed_Cost': fixed_costs_line,
        'Profit': profits
    })
    
    return df, breakeven_units
