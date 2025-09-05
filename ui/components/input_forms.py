
"""Reusable input form components"""
import streamlit as st
from utils.validators import *
from utils.constants import *
from config import Config

def interest_inputs():
    """Create input form for interest calculations"""
    st.subheader("💰 Interest & Time Value Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        principal = st.number_input(
            "Principal Investment ($)",
            min_value=0.0,
            value=100000.0,
            step=1000.0,
            format="%.2f",
            help="Initial amount invested"
        )
    
    with col2:
        interest_rate = st.number_input(
            "Interest Rate (%)",
            min_value=0.0,
            max_value=50.0,
            value=Config.DEFAULT_INTEREST_RATE,
            step=0.1,
            format="%.2f",
            help="Annual interest rate"
        )
    
    with col3:
        periods = st.number_input(
            "Time Period (years)",
            min_value=1,
            max_value=50,
            value=Config.DEFAULT_PROJECT_LIFE,
            step=1,
            help="Number of years for investment"
        )
    
    # Validation
    valid = True
    if not validate_positive_number(principal, "Principal Investment"):
        valid = False
    if not validate_percentage(interest_rate, "Interest Rate"):
        valid = False
    if not validate_years(periods):
        valid = False
    
    return {
        'principal': principal,
        'interest_rate': interest_rate / 100,  # Convert to decimal
        'periods': periods,
        'valid': valid
    }

def depreciation_inputs():
    """Create input form for depreciation calculations"""
    st.subheader("📉 Depreciation Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        purchase_cost = st.number_input(
            "Purchase Cost ($)",
            min_value=0.0,
            value=500000.0,
            step=1000.0,
            format="%.2f",
            help="Initial cost of equipment"
        )
        
        useful_life = st.number_input(
            "Useful Life (years)",
            min_value=1,
            max_value=50,
            value=10,
            step=1,
            help="Expected useful life of equipment"
        )
    
    with col2:
        salvage_value = st.number_input(
            "Salvage Value ($)",
            min_value=0.0,
            value=50000.0,
            step=1000.0,
            format="%.2f",
            help="Expected value at end of useful life"
        )
        
        method = st.selectbox(
            "Depreciation Method",
            DEPRECIATION_METHODS,
            index=0,
            help="Method for calculating depreciation"
        )
    
    # Additional parameters for specific methods
    depreciation_rate = None
    interest_rate = None
    
    if method == "Declining Balance":
        depreciation_rate = st.number_input(
            "Depreciation Rate (%)",
            min_value=0.0,
            max_value=50.0,
            value=20.0,
            step=1.0,
            format="%.1f",
            help="Annual depreciation rate (leave default for double declining balance)"
        ) / 100
    
    if method == "Sinking Fund":
        interest_rate = st.number_input(
            "Interest Rate for Sinking Fund (%)",
            min_value=0.0,
            max_value=20.0,
            value=8.0,
            step=0.5,
            format="%.1f",
            help="Interest rate earned on sinking fund"
        ) / 100
    
    # Validation
    valid = True
    if not validate_positive_number(purchase_cost, "Purchase Cost"):
        valid = False
    if not validate_positive_number(useful_life, "Useful Life"):
        valid = False
    if not validate_salvage_vs_purchase(salvage_value, purchase_cost):
        valid = False
    
    return {
        'purchase_cost': purchase_cost,
        'salvage_value': salvage_value,
        'useful_life': useful_life,
        'method': method,
        'depreciation_rate': depreciation_rate,
        'interest_rate': interest_rate,
        'valid': valid
    }

def profitability_inputs():
    """Create input form for profitability analysis"""
    st.subheader("📈 Profitability Analysis Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        initial_investment = st.number_input(
            "Initial Investment ($)",
            min_value=0.0,
            value=1000000.0,
            step=10000.0,
            format="%.2f",
            help="Total initial capital investment"
        )
        
        annual_cash_flow = st.number_input(
            "Annual Cash Flow ($)",
            min_value=0.0,
            value=200000.0,
            step=5000.0,
            format="%.2f",
            help="Net annual cash inflow from project"
        )
    
    with col2:
        project_life = st.number_input(
            "Project Life (years)",
            min_value=1,
            max_value=50,
            value=10,
            step=1,
            help="Expected project duration"
        )
        
        discount_rate = st.number_input(
            "Discount Rate (%)",
            min_value=0.0,
            max_value=30.0,
            value=12.0,
            step=0.5,
            format="%.1f",
            help="Required rate of return (WACC)"
        )
    
    # Validation
    valid = True
    if not validate_positive_number(initial_investment, "Initial Investment"):
        valid = False
    if not validate_positive_number(annual_cash_flow, "Annual Cash Flow"):
        valid = False
    if not validate_years(project_life):
        valid = False
    if not validate_percentage(discount_rate, "Discount Rate"):
        valid = False
    
    return {
        'initial_investment': initial_investment,
        'annual_cash_flow': annual_cash_flow,
        'project_life': project_life,
        'discount_rate': discount_rate / 100,  # Convert to decimal
        'valid': valid
    }

def cost_estimation_inputs():
    """Create input form for cost estimation"""
    st.subheader("🏭 Cost Estimation Parameters")
    
    # Method selection
    estimation_method = st.selectbox(
        "Estimation Method",
        ["Lang Factor", "Scaling Law", "Detailed Breakdown"],
        help="Choose the cost estimation approach"
    )
    
    if estimation_method == "Lang Factor":
        col1, col2 = st.columns(2)
        
        with col1:
            equipment_cost = st.number_input(
                "Total Equipment Cost ($)",
                min_value=0.0,
                value=2000000.0,
                step=10000.0,
                format="%.2f",
                help="Sum of all major equipment costs"
            )
        
        with col2:
            industry_type = st.selectbox(
                "Industry Type",
                list(LANG_FACTORS.keys()),
                help="Select industry for appropriate Lang factor"
            )
            
            lang_factor = st.number_input(
                "Lang Factor",
                min_value=1.0,
                max_value=10.0,
                value=LANG_FACTORS[industry_type],
                step=0.1,
                format="%.1f",
                help="Multiplier for equipment cost"
            )
        
        return {
            'method': 'lang_factor',
            'equipment_cost': equipment_cost,
            'industry_type': industry_type,
            'lang_factor': lang_factor,
            'valid': validate_positive_number(equipment_cost, "Equipment Cost")
        }
    
    elif estimation_method == "Scaling Law":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            base_cost = st.number_input(
                "Base Equipment Cost ($)",
                min_value=0.0,
                value=500000.0,
                step=1000.0,
                format="%.2f",
                help="Cost of reference equipment"
            )
            
            base_capacity = st.number_input(
                "Base Capacity",
                min_value=0.1,
                value=1000.0,
                step=10.0,
                format="%.2f",
                help="Capacity of reference equipment"
            )
        
        with col2:
            new_capacity = st.number_input(
                "New Capacity",
                min_value=0.1,
                value=1500.0,
                step=10.0,
                format="%.2f",
                help="Desired capacity for new equipment"
            )
            
            equipment_type = st.selectbox(
                "Equipment Type",
                list(SCALING_EXPONENTS.keys()),
                help="Type of equipment for scaling exponent"
            )
        
        with col3:
            scaling_exponent = st.number_input(
                "Scaling Exponent",
                min_value=0.1,
                max_value=1.0,
                value=SCALING_EXPONENTS[equipment_type],
                step=0.05,
                format="%.2f",
                help="Scaling factor (typically 0.6)"
            )
        
        valid = (validate_positive_number(base_cost, "Base Cost") and 
                validate_positive_number(base_capacity, "Base Capacity") and
                validate_positive_number(new_capacity, "New Capacity"))
        
        return {
            'method': 'scaling_law',
            'base_cost': base_cost,
            'base_capacity': base_capacity,
            'new_capacity': new_capacity,
            'scaling_exponent': scaling_exponent,
            'equipment_type': equipment_type,
            'valid': valid
        }
    
    else:  # Detailed Breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            equipment_cost = st.number_input(
                "Equipment Cost ($)",
                min_value=0.0,
                value=2000000.0,
                step=10000.0,
                format="%.2f",
                help="Total major equipment cost"
            )
            
            industry_type = st.selectbox(
                "Industry Type",
                ["Chemical Processing", "Petrochemical"],
                help="Industry type for cost factors"
            )
        
        with col2:
            annual_sales = st.number_input(
                "Annual Sales ($)",
                min_value=0.0,
                value=10000000.0,
                step=100000.0,
                format="%.2f",
                help="Expected annual sales revenue"
            )
            
            working_capital_factor = st.number_input(
                "Working Capital Factor",
                min_value=0.05,
                max_value=0.50,
                value=0.15,
                step=0.01,
                format="%.2f",
                help="Working capital as fraction of sales"
            )
        
        valid = (validate_positive_number(equipment_cost, "Equipment Cost") and
                validate_positive_number(annual_sales, "Annual Sales"))
        
        return {
            'method': 'detailed',
            'equipment_cost': equipment_cost,
            'industry_type': industry_type,
            'annual_sales': annual_sales,
            'working_capital_factor': working_capital_factor,
            'valid': valid
        }

def breakeven_inputs():
    """Create input form for break-even analysis"""
    st.subheader("⚖️ Break-Even Analysis Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fixed_costs = st.number_input(
            "Fixed Costs ($)",
            min_value=0.0,
            value=500000.0,
            step=1000.0,
            format="%.2f",
            help="Annual fixed costs (rent, salaries, etc.)"
        )
        
        variable_cost_per_unit = st.number_input(
            "Variable Cost per Unit ($)",
            min_value=0.0,
            value=15.0,
            step=0.10,
            format="%.2f",
            help="Variable cost per unit produced"
        )
    
    with col2:
        selling_price_per_unit = st.number_input(
            "Selling Price per Unit ($)",
            min_value=0.0,
            value=25.0,
            step=0.10,
            format="%.2f",
            help="Revenue per unit sold"
        )
        
        analysis_volume = st.number_input(
            "Analysis Volume (units)",
            min_value=0.0,
            value=50000.0,
            step=1000.0,
            format="%.0f",
            help="Production volume for profit analysis"
        )
    
    # Validation
    valid = True
    if not validate_positive_number(fixed_costs, "Fixed Costs"):
        valid = False
    if not validate_positive_number(selling_price_per_unit, "Selling Price"):
        valid = False
    if selling_price_per_unit <= variable_cost_per_unit:
        st.error("Selling price must be greater than variable cost per unit")
        valid = False
    
    return {
        'fixed_costs': fixed_costs,
        'variable_cost_per_unit': variable_cost_per_unit,
        'selling_price_per_unit': selling_price_per_unit,
        'analysis_volume': analysis_volume,
        'valid': valid
    }

def replacement_inputs():
    """Create input form for replacement analysis"""
    st.subheader("🔄 Equipment Replacement Parameters")
    
    st.markdown("**Current Equipment:**")
    col1, col2 = st.columns(2)
    
    with col1:
        old_salvage_value = st.number_input(
            "Current Salvage Value ($)",
            min_value=0.0,
            value=100000.0,
            step=1000.0,
            format="%.2f",
            help="Current market value of old equipment"
        )
        
        old_annual_cost = st.number_input(
            "Annual Operating Cost ($)",
            min_value=0.0,
            value=80000.0,
            step=1000.0,
            format="%.2f",
            help="Annual cost to operate current equipment"
        )
    
    with col2:
        old_remaining_life = st.number_input(
            "Remaining Life (years)",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
            help="Remaining useful life of current equipment"
        )
    
    st.markdown("**New Equipment:**")
    col3, col4 = st.columns(2)
    
    with col3:
        new_equipment_cost = st.number_input(
            "Purchase Cost ($)",
            min_value=0.0,
            value=400000.0,
            step=1000.0,
            format="%.2f",
            help="Cost to purchase new equipment"
        )
        
        new_annual_cost = st.number_input(
            "Annual Operating Cost ($)",
            min_value=0.0,
            value=50000.0,
            step=1000.0,
            format="%.2f",
            help="Annual cost to operate new equipment"
        )
    
    with col4:
        new_equipment_life = st.number_input(
            "Equipment Life (years)",
            min_value=1,
            max_value=30,
            value=15,
            step=1,
            help="Expected life of new equipment"
        )
        
        new_salvage_value = st.number_input(
            "Salvage Value ($)",
            min_value=0.0,
            value=40000.0,
            step=1000.0,
            format="%.2f",
            help="Expected salvage value of new equipment"
        )
    
    interest_rate = st.number_input(
        "Interest Rate (%)",
        min_value=0.0,
        max_value=25.0,
        value=10.0,
        step=0.5,
        format="%.1f",
        help="Interest rate for economic analysis"
    )
    
    # Validation
    valid = True
    if not validate_positive_number(new_equipment_cost, "New Equipment Cost"):
        valid = False
    if not validate_positive_number(old_annual_cost, "Old Equipment Annual Cost"):
        valid = False
    if not validate_positive_number(new_annual_cost, "New Equipment Annual Cost"):
        valid = False
    if not validate_years(new_equipment_life):
        valid = False
    if not validate_percentage(interest_rate, "Interest Rate"):
        valid = False
    
    return {
        'old_salvage_value': old_salvage_value,
        'old_annual_cost': old_annual_cost,
        'old_remaining_life': old_remaining_life,
        'new_equipment_cost': new_equipment_cost,
        'new_annual_cost': new_annual_cost,
        'new_equipment_life': new_equipment_life,
        'new_salvage_value': new_salvage_value,
        'interest_rate': interest_rate / 100,  # Convert to decimal
        'valid': valid
    }

def master_inputs():
    """Create comprehensive input form for master calculation"""
    st.subheader("🎯 Comprehensive Plant Economics Analysis")
    
    st.markdown("### 📊 Project Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input(
            "Project Name",
            value="Chemical Plant Investment",
            help="Name of the project for reporting"
        )
        
        total_equipment_cost = st.number_input(
            "Total Equipment Cost ($)",
            min_value=0.0,
            value=5000000.0,
            step=50000.0,
            format="%.2f",
            help="Sum of all major equipment costs"
        )
    
    with col2:
        industry_type = st.selectbox(
            "Industry Type",
            list(LANG_FACTORS.keys()),
            help="Type of chemical processing industry"
        )
        
        project_life = st.number_input(
            "Project Life (years)",
            min_value=5,
            max_value=30,
            value=15,
            step=1,
            help="Expected project duration"
        )
    
    st.markdown("### 💰 Financial Parameters")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        annual_sales = st.number_input(
            "Annual Sales Revenue ($)",
            min_value=0.0,
            value=20000000.0,
            step=100000.0,
            format="%.2f",
            help="Expected annual sales"
        )
    
    with col4:
        annual_operating_cost = st.number_input(
            "Annual Operating Cost ($)",
            min_value=0.0,
            value=15000000.0,
            step=100000.0,
            format="%.2f",
            help="Annual production costs"
        )
    
    with col5:
        discount_rate = st.number_input(
            "Discount Rate (%)",
            min_value=5.0,
            max_value=25.0,
            value=12.0,
            step=0.5,
            format="%.1f",
            help="Cost of capital/required return"
        )
    
    st.markdown("### 🏭 Production Parameters")
    col6, col7, col8 = st.columns(3)
    
    with col6:
        annual_production = st.number_input(
            "Annual Production (units)",
            min_value=1000.0,
            value=1000000.0,
            step=10000.0,
            format="%.0f",
            help="Annual production capacity"
        )
    
    with col7:
        variable_cost_per_unit = st.number_input(
            "Variable Cost per Unit ($)",
            min_value=0.0,
            value=12.0,
            step=0.10,
            format="%.2f",
            help="Variable production cost per unit"
        )
    
    with col8:
        selling_price_per_unit = st.number_input(
            "Selling Price per Unit ($)",
            min_value=0.0,
            value=20.0,
            step=0.10,
            format="%.2f",
            help="Revenue per unit sold"
        )
    
    # Calculate derived values
    annual_cash_flow = annual_sales - annual_operating_cost
    lang_factor = LANG_FACTORS.get(industry_type, 4.3)
    total_fixed_capital = total_equipment_cost * lang_factor
    working_capital = annual_sales * 0.15
    total_investment = total_fixed_capital + working_capital
    fixed_costs = annual_operating_cost - (variable_cost_per_unit * annual_production)
    
    # Display calculated values
    st.markdown("### 📋 Calculated Parameters")
    col9, col10, col11 = st.columns(3)
    
    with col9:
        st.metric("Annual Cash Flow", f"${annual_cash_flow:,.0f}")
        st.metric("Total Fixed Capital", f"${total_fixed_capital:,.0f}")
    
    with col10:
        st.metric("Working Capital", f"${working_capital:,.0f}")
        st.metric("Total Investment", f"${total_investment:,.0f}")
    
    with col11:
        st.metric("Fixed Costs", f"${fixed_costs:,.0f}")
        st.metric("Lang Factor", f"{lang_factor:.1f}")
    
    # Validation
    valid = True
    error_messages = []
    
    if not validate_positive_number(total_equipment_cost, "Equipment Cost"):
        valid = False
        error_messages.append("Equipment cost must be positive")
    
    if not validate_positive_number(annual_sales, "Annual Sales"):
        valid = False
        error_messages.append("Annual sales must be positive")
    
    if annual_operating_cost >= annual_sales:
        valid = False
        error_messages.append("Operating costs cannot exceed sales revenue")
    
    if selling_price_per_unit <= variable_cost_per_unit:
        valid = False
        error_messages.append("Selling price must be greater than variable cost per unit")
    
    if fixed_costs < 0:
        valid = False
        error_messages.append("Check production parameters - fixed costs cannot be negative")
    
    if error_messages:
        for msg in error_messages:
            st.error(msg)
    
    return {
        'project_name': project_name,
        'total_equipment_cost': total_equipment_cost,
        'industry_type': industry_type,
        'project_life': project_life,
        'annual_sales': annual_sales,
        'annual_operating_cost': annual_operating_cost,
        'annual_cash_flow': annual_cash_flow,
        'discount_rate': discount_rate / 100,  # Convert to decimal
        'annual_production': annual_production,
        'variable_cost_per_unit': variable_cost_per_unit,
        'selling_price_per_unit': selling_price_per_unit,
        'lang_factor': lang_factor,
        'total_fixed_capital': total_fixed_capital,
        'working_capital': working_capital,
        'total_investment': total_investment,
        'fixed_costs': fixed_costs,
        'valid': valid
    }
