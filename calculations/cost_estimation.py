
"""Cost estimation calculations"""
import numpy as np
import pandas as pd

def scaling_law_cost(base_cost, base_capacity, new_capacity, scaling_exponent=0.6):
    """Calculate cost using scaling law (six-tenths factor rule)
    
    Args:
        base_cost (float): Cost of base equipment (C1)
        base_capacity (float): Capacity of base equipment (Q1)
        new_capacity (float): Capacity of new equipment (Q2)
        scaling_exponent (float): Scaling exponent (n), default 0.6
    
    Returns:
        dict: Cost estimation details
    """
    if base_capacity == 0:
        return {'error': 'Base capacity cannot be zero'}
    
    capacity_ratio = new_capacity / base_capacity
    new_cost = base_cost * (capacity_ratio ** scaling_exponent)
    cost_ratio = new_cost / base_cost
    
    return {
        'new_cost': new_cost,
        'base_cost': base_cost,
        'capacity_ratio': capacity_ratio,
        'cost_ratio': cost_ratio,
        'scaling_exponent': scaling_exponent,
        'cost_per_unit_capacity': new_cost / new_capacity
    }

def lang_factor_estimate(equipment_costs, lang_factor):
    """Calculate total plant cost using Lang factor method
    
    Args:
        equipment_costs (list or float): Equipment costs
        lang_factor (float): Lang factor for the industry
    
    Returns:
        dict: Plant cost estimation details
    """
    if isinstance(equipment_costs, (int, float)):
        total_equipment_cost = equipment_costs
    else:
        total_equipment_cost = sum(equipment_costs)
    
    total_plant_cost = lang_factor * total_equipment_cost
    installation_cost = total_plant_cost - total_equipment_cost
    
    return {
        'total_plant_cost': total_plant_cost,
        'total_equipment_cost': total_equipment_cost,
        'installation_cost': installation_cost,
        'lang_factor': lang_factor,
        'equipment_percentage': (total_equipment_cost / total_plant_cost) * 100,
        'installation_percentage': (installation_cost / total_plant_cost) * 100
    }

def detailed_cost_breakdown(equipment_cost, industry_type='Chemical Processing'):
    """Calculate detailed cost breakdown for plant investment
    
    Args:
        equipment_cost (float): Total equipment cost
        industry_type (str): Type of industry for factor selection
    
    Returns:
        dict: Detailed cost breakdown
    """
    # Industry-specific factors
    factors = {
        'Chemical Processing': {
            'equipment': 1.0,
            'installation': 0.45,
            'instrumentation': 0.25,
            'piping': 0.35,
            'electrical': 0.15,
            'buildings': 0.20,
            'utilities': 0.30,
            'site_preparation': 0.10,
            'engineering': 0.25,
            'contingency': 0.15
        },
        'Petrochemical': {
            'equipment': 1.0,
            'installation': 0.40,
            'instrumentation': 0.30,
            'piping': 0.40,
            'electrical': 0.20,
            'buildings': 0.15,
            'utilities': 0.35,
            'site_preparation': 0.08,
            'engineering': 0.30,
            'contingency': 0.20
        }
    }
    
    if industry_type not in factors:
        industry_type = 'Chemical Processing'
    
    factor_set = factors[industry_type]
    
    costs = {}
    total_cost = 0
    
    for category, factor in factor_set.items():
        cost = equipment_cost * factor
        costs[category] = cost
        total_cost += cost
    
    # Calculate percentages
    percentages = {category: (cost / total_cost) * 100 for category, cost in costs.items()}
    
    return {
        'costs': costs,
        'percentages': percentages,
        'total_fixed_capital': total_cost,
        'equipment_cost': equipment_cost,
        'industry_type': industry_type
    }

def working_capital_estimate(annual_sales, working_capital_factor=0.15):
    """Estimate working capital requirements
    
    Args:
        annual_sales (float): Annual sales revenue
        working_capital_factor (float): Working capital as fraction of annual sales
    
    Returns:
        dict: Working capital estimation
    """
    working_capital = annual_sales * working_capital_factor
    
    # Breakdown of working capital components
    raw_materials = working_capital * 0.30
    finished_goods = working_capital * 0.25
    accounts_receivable = working_capital * 0.35
    cash_on_hand = working_capital * 0.10
    
    return {
        'total_working_capital': working_capital,
        'raw_materials_inventory': raw_materials,
        'finished_goods_inventory': finished_goods,
        'accounts_receivable': accounts_receivable,
        'cash_on_hand': cash_on_hand,
        'working_capital_factor': working_capital_factor,
        'annual_sales': annual_sales
    }

def total_capital_investment(equipment_cost, industry_type, annual_sales, working_capital_factor=0.15):
    """Calculate total capital investment (fixed + working capital)
    
    Args:
        equipment_cost (float): Total equipment cost
        industry_type (str): Industry type
        annual_sales (float): Annual sales revenue
        working_capital_factor (float): Working capital factor
    
    Returns:
        dict: Complete capital investment analysis
    """
    fixed_capital = detailed_cost_breakdown(equipment_cost, industry_type)
    working_capital = working_capital_estimate(annual_sales, working_capital_factor)
    
    total_investment = fixed_capital['total_fixed_capital'] + working_capital['total_working_capital']
    
    return {
        'total_capital_investment': total_investment,
        'fixed_capital_investment': fixed_capital['total_fixed_capital'],
        'working_capital': working_capital['total_working_capital'],
        'fixed_capital_breakdown': fixed_capital,
        'working_capital_breakdown': working_capital,
        'fixed_capital_percentage': (fixed_capital['total_fixed_capital'] / total_investment) * 100,
        'working_capital_percentage': (working_capital['total_working_capital'] / total_investment) * 100
    }

def production_cost_estimate(raw_material_cost, utilities_cost, labor_cost, maintenance_factor=0.06, 
                           overhead_factor=0.50, admin_factor=0.20):
    """Estimate annual production costs
    
    Args:
        raw_material_cost (float): Annual raw material cost
        utilities_cost (float): Annual utilities cost
        labor_cost (float): Annual direct labor cost
        maintenance_factor (float): Maintenance as fraction of fixed capital
        overhead_factor (float): Overhead as fraction of direct costs
        admin_factor (float): Administrative costs as fraction of direct costs
    
    Returns:
        dict: Production cost breakdown
    """
    direct_costs = raw_material_cost + utilities_cost + labor_cost
    maintenance_cost = direct_costs * maintenance_factor
    overhead_cost = direct_costs * overhead_factor
    administrative_cost = direct_costs * admin_factor
    
    total_production_cost = direct_costs + maintenance_cost + overhead_cost + administrative_cost
    
    cost_breakdown = {
        'raw_materials': raw_material_cost,
        'utilities': utilities_cost,
        'direct_labor': labor_cost,
        'maintenance': maintenance_cost,
        'overhead': overhead_cost,
        'administrative': administrative_cost,
        'total_production_cost': total_production_cost
    }
    
    # Calculate percentages
    percentages = {category: (cost / total_production_cost) * 100 for category, cost in cost_breakdown.items() if category != 'total_production_cost'}
    
    return {
        'cost_breakdown': cost_breakdown,
        'cost_percentages': percentages,
        'direct_costs': direct_costs,
        'indirect_costs': maintenance_cost + overhead_cost + administrative_cost,
        'total_annual_cost': total_production_cost
    }
