
"""Cost estimation calculations"""

def lang_factor_estimate(equipment_cost, lang_factor):
    """Estimate total plant cost using Lang factor"""
    total_plant_cost = equipment_cost * lang_factor
    installation_cost = total_plant_cost - equipment_cost
    
    return {
        'total_equipment_cost': equipment_cost,
        'total_plant_cost': total_plant_cost,
        'installation_cost': installation_cost,
        'equipment_percentage': (equipment_cost / total_plant_cost) * 100,
        'installation_percentage': (installation_cost / total_plant_cost) * 100
    }

def scaling_law_cost(base_cost, base_capacity, new_capacity, scaling_exponent):
    """Calculate cost using scaling law"""
    capacity_ratio = new_capacity / base_capacity
    cost_ratio = capacity_ratio ** scaling_exponent
    new_cost = base_cost * cost_ratio
    
    return {
        'base_cost': base_cost,
        'new_cost': new_cost,
        'capacity_ratio': capacity_ratio,
        'cost_ratio': cost_ratio,
        'cost_per_unit_capacity': new_cost / new_capacity
    }

def total_capital_investment(equipment_cost, industry_type, annual_sales, wc_factor):
    """Calculate total capital investment"""
    # Lang factor based on industry
    lang_factors = {
        "Chemical Processing": 4.3,
        "Petrochemical": 5.5,
        "Solid Processing": 3.1,
        "Fluid Processing": 4.8
    }
    
    lang_factor = lang_factors.get(industry_type, 4.3)
    fixed_capital = equipment_cost * lang_factor
    working_capital = annual_sales * wc_factor
    total_investment = fixed_capital + working_capital
    
    # Detailed breakdown
    fixed_capital_breakdown = {
        'costs': {
            'Equipment': equipment_cost,
            'Installation': equipment_cost * 0.5,
            'Buildings': equipment_cost * 0.3,
            'Utilities': equipment_cost * 0.2,
            'Engineering': equipment_cost * 0.3
        }
    }
    
    # Working capital breakdown
    wc_breakdown = {
        'raw_materials_inventory': working_capital * 0.4,
        'finished_goods_inventory': working_capital * 0.3,
        'accounts_receivable': working_capital * 0.2,
        'cash_on_hand': working_capital * 0.1,
        'total_working_capital': working_capital
    }
    
    return {
        'fixed_capital_investment': fixed_capital,
        'working_capital': working_capital,
        'total_capital_investment': total_investment,
        'fixed_capital_percentage': (fixed_capital / total_investment) * 100,
        'working_capital_percentage': (working_capital / total_investment) * 100,
        'fixed_capital_breakdown': fixed_capital_breakdown,
        'working_capital_breakdown': wc_breakdown
    }
