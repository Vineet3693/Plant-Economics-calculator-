
"""Reusable result display components"""
import streamlit as st
import pandas as pd
from utils.styling import *
from config import Config

def display_interest_results(results):
    """Display interest calculation results"""
    st.markdown("### 📊 Interest Calculation Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_metric_card(
            "Principal Investment",
            f"${results['principal']:,.2f}",
            color="primary"
        )
    
    with col2:
        create_metric_card(
            "Future Value",
            f"${results['future_value']:,.2f}",
            color="success"
        )
    
    with col3:
        create_metric_card(
            "Total Interest Earned",
            f"${results['compound_interest']:,.2f}",
            color="warning"
        )
    
    # Additional metrics
    col4, col5 = st.columns(2)
    
    with col4:
        growth_multiple = results['future_value'] / results['principal']
        create_metric_card(
            "Growth Multiple",
            f"{growth_multiple:.2f}x",
            color="primary"
        )
    
    with col5:
        annualized_return = ((results['future_value'] / results['principal']) ** (1/results['periods']) - 1) * 100
        create_metric_card(
            "Effective Annual Return",
            f"{annualized_return:.2f}%",
            color="success"
        )

def display_depreciation_results(results):
    """Display depreciation calculation results"""
    st.markdown("### 📉 Depreciation Analysis Results")
    
    method = results['method']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_metric_card(
            "Depreciation Method",
            method,
            color="primary"
        )
    
    with col2:
        if 'annual_depreciation' in results:
            create_metric_card(
                "Annual Depreciation",
                f"${results['annual_depreciation']:,.2f}",
                color="warning"
            )
        elif 'annual_payment' in results:
            create_metric_card(
                "Annual Sinking Fund",
                f"${results['annual_payment']:,.2f}",
                color="warning"
            )
    
    with col3:
        total_dep = results.get('total_depreciation', 0)
        create_metric_card(
            "Total Depreciation",
            f"${total_dep:,.2f}",
            color="error"
        )
    
    # Display depreciation table
    if 'depreciation_table' in results:
        st.markdown("#### Yearly Depreciation Schedule")
        
        # Format the table for better display
        table = results['depreciation_table'].copy()
        for col in table.columns:
            if table[col].dtype in ['float64', 'int64']:
                table[col] = table[col].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "$0.00")
        
        st.dataframe(table, use_container_width=True)

def display_profitability_results(results):
    """Display profitability analysis results"""
    st.markdown("### 📈 Profitability Analysis Results")
    
    # Key metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        npv_color = "success" if results['npv'] > 0 else "error"
        create_metric_card(
            "Net Present Value",
            f"${results['npv']:,.0f}",
            color=npv_color
        )
    
    with col2:
        if results.get('irr_percent'):
            create_metric_card(
                "Internal Rate of Return",
                f"{results['irr_percent']:.2f}%",
                color="primary"
            )
        else:
            create_metric_card(
                "Internal Rate of Return",
                "Cannot Calculate",
                color="error"
            )
    
    with col3:
        create_metric_card(
            "Return on Investment",
            f"{results['roi_percent']:.2f}%",
            color="warning"
        )
    
    with col4:
        pb_color = "success" if results['payback_period'] <= 5 else "warning"
        create_metric_card(
            "Payback Period",
            f"{results['payback_period']:.2f} years",
            color=pb_color
        )
    
    # Investment decision summary
    st.markdown("#### Investment Decision Summary")
    
    decision_data = {
        "Metric": ["NPV Decision", "IRR Decision", "Payback Assessment"],
        "Result": [
            results.get('npv_decision', 'N/A'),
            results.get('irr_decision', 'N/A'),
            results.get('payback_decision', 'N/A')
        ],
        "Value": [
            f"${results['npv']:,.0f}",
            f"{results.get('irr_percent', 0):.2f}%" if results.get('irr_percent') else "N/A",
            f"{results['payback_period']:.2f} years"
        ]
    }
    
    create_comparison_table(
        [list(row) for row in zip(decision_data["Metric"], decision_data["Result"], decision_data["Value"])],
        ["Metric", "Decision", "Value"]
    )

def display_cost_estimation_results(results, method):
    """Display cost estimation results"""
    st.markdown("### 🏭 Cost Estimation Results")
    
    if method == 'lang_factor':
        col1, col2, col3 = st.columns(3)
        
        with col1:
            create_metric_card(
                "Equipment Cost",
                f"${results['total_equipment_cost']:,.0f}",
                color="primary"
            )
        
        with col2:
            create_metric_card(
                "Total Plant Cost",
                f"${results['total_plant_cost']:,.0f}",
                color="success"
            )
        
        with col3:
            create_metric_card(
                "Installation Cost",
                f"${results['installation_cost']:,.0f}",
                color="warning"
            )
        
        # Cost breakdown percentages
        st.markdown("#### Cost Distribution")
        col4, col5 = st.columns(2)
        
        with col4:
            create_metric_card(
                "Equipment %",
                f"{results['equipment_percentage']:.1f}%",
                color="primary"
            )
        
        with col5:
            create_metric_card(
                "Installation %",
                f"{results['installation_percentage']:.1f}%",
                color="warning"
            )
    
    elif method == 'scaling_law':
        col1, col2, col3 = st.columns(3)
        
        with col1:
            create_metric_card(
                "Base Cost",
                f"${results['base_cost']:,.0f}",
                color="primary"
            )
        
        with col2:
            create_metric_card(
                "New Equipment Cost",
                f"${results['new_cost']:,.0f}",
                color="success"
            )
        
        with col3:
            create_metric_card(
                "Capacity Ratio",
                f"{results['capacity_ratio']:.2f}",
                color="warning"
            )
        
        col4, col5 = st.columns(2)
        
        with col4:
            create_metric_card(
                "Cost Ratio",
                f"{results['cost_ratio']:.2f}",
                color="primary"
            )
        
        with col5:
            create_metric_card(
                "Cost per Unit Capacity",
                f"${results['cost_per_unit_capacity']:,.2f}",
                color="warning"
            )
    
    elif method == 'detailed':
        # Display total investment breakdown
        col1, col2, col3 = st.columns(3)
        
        with col1:
            create_metric_card(
                "Fixed Capital",
                f"${results['fixed_capital_investment']:,.0f}",
                color="primary"
            )
        
        with col2:
            create_metric_card(
                "Working Capital",
                f"${results['working_capital']:,.0f}",
                color="warning"
            )
        
        with col3:
            create_metric_card(
                "Total Investment",
                f"${results['total_capital_investment']:,.0f}",
                color="success"
            )
        
        # Investment percentages
        st.markdown("#### Investment Distribution")
        col4, col5 = st.columns(2)
        
        with col4:
            create_metric_card(
                "Fixed Capital %",
                f"{results['fixed_capital_percentage']:.1f}%",
                color="primary"
            )
        
        with col5:
            create_metric_card(
                "Working Capital %",
                f"{results['working_capital_percentage']:.1f}%",
                color="warning"
            )

def display_breakeven_results(results):
    """Display break-even analysis results"""
    st.markdown("### ⚖️ Break-Even Analysis Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_metric_card(
            "Break-Even Volume",
            f"{results['breakeven_units']:,.0f} units",
            color="primary"
        )
    
    with col2:
        create_metric_card(
            "Break-Even Sales",
            f"${results['breakeven_sales']:,.0f}",
            color="success"
        )
    
    with col3:
        create_metric_card(
            "Contribution Margin",
            f"${results['contribution_margin_per_unit']:.2f}/unit",
            color="warning"
        )
    
    # Additional metrics
    col4, col5 = st.columns(2)
    
    with col4:
        margin_ratio = results['contribution_margin_ratio'] * 100
        create_metric_card(
            "Contribution Margin %",
            f"{margin_ratio:.1f}%",
            color="primary"
        )
    
    with col5:
        # Calculate margin of safety if analysis volume provided
        if 'analysis_volume' in results:
            safety_margin = ((results['analysis_volume'] - results['breakeven_units']) / results['analysis_volume']) * 100
            safety_color = "success" if safety_margin > 20 else "warning" if safety_margin > 0 else "error"
            create_metric_card(
                "Margin of Safety",
                f"{safety_margin:.1f}%",
                color=safety_color
            )

def display_replacement_results(results):
    """Display replacement analysis results"""
    st.markdown("### 🔄 Equipment Replacement Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_metric_card(
            "Net Investment",
            f"${results['net_investment']:,.0f}",
            color="primary"
        )
    
    with col2:
        savings_color = "success" if results['net_savings'] > 0 else "error"
        create_metric_card(
            "Net Savings (PV)",
            f"${results['net_savings']:,.0f}",
            color=savings_color
        )
    
    with col3:
        annual_savings_color = "success" if results['annual_savings'] > 0 else "error"
        create_metric_card(
            "Annual Savings",
            f"${results['annual_savings']:,.0f}",
            color=annual_savings_color
        )
    
    # Decision summary
    st.markdown("#### Replacement Decision")
    
    recommendation = results['recommendation']
    rec_color = "success" if recommendation == "Replace" else "warning"
    
    create_info_box(
        f"<strong>Recommendation:</strong> {recommendation}<br>"
        f"<strong>Economic Justification:</strong> {'Positive net savings justify replacement' if results['net_savings'] > 0 else 'Negative savings suggest keeping current equipment'}",
        "success" if recommendation == "Replace" else "warning"
    )
    
    # Comparison table
    comparison_data = [
        ["Present Worth - Keep Old", f"${results['present_worth_old']:,.0f}"],
        ["Present Worth - Replace", f"${results['present_worth_new']:,.0f}"],
        ["Net Savings", f"${results['net_savings']:,.0f}"],
        ["EAC - Old Equipment", f"${results['equivalent_annual_cost_old']:,.0f}"],
        ["EAC - New Equipment", f"${results['equivalent_annual_cost_new']:,.0f}"],
        ["Annual Savings", f"${results['annual_savings']:,.0f}"]
    ]
    
    create_comparison_table(comparison_data, ["Analysis Item", "Value"])

def display_master_dashboard(all_results):
    """Display comprehensive dashboard for master analysis"""
    st.markdown("# 🎯 Plant Economics Dashboard")
    st.markdown("### Executive Summary")
    
    # Key Performance Indicators
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        npv_color = "success" if all_results.get('npv', 0) > 0 else "error"
        create_metric_card(
            "Net Present Value",
            f"${all_results.get('npv', 0):,.0f}",
            color=npv_color
        )
    
    with col2:
        create_metric_card(
            "Total Investment",
            f"${all_results.get('total_investment', 0):,.0f}",
            color="primary"
        )
    
    with col3:
        irr = all_results.get('irr_percent', 0)
        irr_color = "success" if irr > 15 else "warning" if irr > 10 else "error"
        create_metric_card(
            "IRR",
            f"{irr:.1f}%" if irr else "N/A",
            color=irr_color
        )
    
    with col4:
        payback = all_results.get('payback_period', 0)
        pb_color = "success" if payback <= 3 else "warning" if payback <= 5 else "error"
        create_metric_card(
            "Payback Period",
            f"{payback:.1f} years",
            color=pb_color
        )
    
    with col5:
        breakeven = all_results.get('breakeven_units', 0)
        create_metric_card(
            "Break-Even Volume",
            f"{breakeven:,.0f} units",
            color="warning"
        )
    
    # Investment Decision Summary
    st.markdown("### Investment Decision Matrix")
    
    # Determine overall recommendation
    npv_positive = all_results.get('npv', 0) > 0
    irr_acceptable = all_results.get('irr_percent', 0) > all_results.get('discount_rate', 0.12) * 100
    payback_reasonable = all_results.get('payback_period', 100) <= 5
    
    decision_score = sum([npv_positive, irr_acceptable, payback_reasonable])
    
    if decision_score >= 3:
        overall_decision = "STRONG ACCEPT"
        decision_color = "success"
    elif decision_score >= 2:
        overall_decision = "CONDITIONAL ACCEPT"
        decision_color = "warning"
    else:
        overall_decision = "REJECT"
        decision_color = "error"
    
    # Decision matrix table
    decision_matrix = [
        ["NPV Analysis", "Accept" if npv_positive else "Reject", f"${all_results.get('npv', 0):,.0f}"],
        ["IRR Analysis", "Accept" if irr_acceptable else "Reject", f"{all_results.get('irr_percent', 0):.1f}%"],
        ["Payback Analysis", "Accept" if payback_reasonable else "Reject", f"{all_results.get('payback_period', 0):.1f} years"],
        ["Overall Decision", overall_decision, f"Score: {decision_score}/3"]
    ]
    
    create_comparison_table(decision_matrix, ["Criteria", "Decision", "Value"])
    
    # Financial Summary
    st.markdown("### Financial Performance Summary")
    
    col6, col7, col8 = st.columns(3)
    
    with col6:
        st.markdown("**Investment Breakdown**")
        fixed_capital = all_results.get('fixed_capital_investment', 0)
        working_capital = all_results.get('working_capital', 0)
        
        investment_data = [
            ["Fixed Capital", f"${fixed_capital:,.0f}"],
            ["Working Capital", f"${working_capital:,.0f}"],
            ["Total Investment", f"${all_results.get('total_investment', 0):,.0f}"]
        ]
        
        create_comparison_table(investment_data, ["Component", "Amount"])
    
    with col7:
        st.markdown("**Annual Performance**")
        annual_sales = all_results.get('annual_sales', 0)
        annual_cash_flow = all_results.get('annual_cash_flow', 0)
        
        performance_data = [
            ["Annual Sales", f"${annual_sales:,.0f}"],
            ["Annual Cash Flow", f"${annual_cash_flow:,.0f}"],
            ["Cash Flow Margin", f"{(annual_cash_flow/annual_sales*100):.1f}%" if annual_sales > 0 else "N/A"]
        ]
        
        create_comparison_table(performance_data, ["Metric", "Value"])
    
    with col8:
        st.markdown("**Break-Even Analysis**")
        breakeven_sales = all_results.get('breakeven_sales', 0)
        margin_of_safety = 0
        if annual_sales > 0 and breakeven_sales > 0:
            margin_of_safety = ((annual_sales - breakeven_sales) / annual_sales) * 100
        
        breakeven_data = [
            ["Break-Even Sales", f"${breakeven_sales:,.0f}"],
            ["Expected Sales", f"${annual_sales:,.0f}"],
            ["Margin of Safety", f"{margin_of_safety:.1f}%"]
        ]
        
        create_comparison_table(breakeven_data, ["Metric", "Value"])
    
    # Risk Assessment
    st.markdown("### Risk Assessment")
    
    risk_factors = []
    
    # High investment risk
    if all_results.get('total_investment', 0) > 10000000:
        risk_factors.append("High capital investment requires careful cash flow management")
    
    # Low margin of safety
    if 0 <= margin_of_safety < 20:
        risk_factors.append("Low margin of safety - sensitive to sales volume changes")
    
    # Long payback period
    if all_results.get('payback_period', 0) > 5:
        risk_factors.append("Extended payback period increases investment risk")
    
    # IRR close to discount rate
    irr_spread = all_results.get('irr_percent', 0) - (all_results.get('discount_rate', 0.12) * 100)
    if 0 <= irr_spread < 3:
        risk_factors.append("IRR only marginally exceeds required return")
    
    if risk_factors:
        risk_content = "<br>".join([f"• {risk}" for risk in risk_factors])
        create_info_box(
            f"<strong>Key Risk Factors:</strong><br>{risk_content}",
            "warning"
        )
    else:
        create_info_box(
            "<strong>Risk Assessment:</strong> Low risk investment with strong financial indicators",
            "success"
        )
    
    # Sensitivity Indicators
    st.markdown("### Sensitivity Indicators")
    
    col9, col10, col11 = st.columns(3)
    
    with col9:
        # Sales sensitivity
        sales_sensitivity = abs(all_results.get('npv', 0)) / all_results.get('annual_sales', 1)
        sensitivity_color = "success" if sales_sensitivity < 0.1 else "warning" if sales_sensitivity < 0.2 else "error"
        create_metric_card(
            "Sales Sensitivity",
            f"{sales_sensitivity:.3f}",
            color=sensitivity_color
        )
        st.caption("NPV impact per $1 change in annual sales")
    
    with col10:
        # Cost sensitivity
        cost_sensitivity = abs(all_results.get('npv', 0)) / all_results.get('annual_operating_cost', 1)
        create_metric_card(
            "Cost Sensitivity",
            f"{cost_sensitivity:.3f}",
            color=sensitivity_color
        )
        st.caption("NPV impact per $1 change in annual costs")
    
    with col11:
        # Investment sensitivity
        investment_sensitivity = abs(all_results.get('npv', 0)) / all_results.get('total_investment', 1)
        create_metric_card(
            "Investment Sensitivity",
            f"{investment_sensitivity:.3f}",
            color=sensitivity_color
        )
        st.caption("NPV impact per $1 change in investment")
    
    # Project Timeline
    st.markdown("### Project Financial Timeline")
    
    project_life = all_results.get('project_life', 10)
    annual_cf = all_results.get('annual_cash_flow', 0)
    
    # Create simple timeline data
    timeline_data = []
    cumulative_cf = -all_results.get('total_investment', 0)
    
    timeline_data.append(["Year 0", "Initial Investment", f"-${all_results.get('total_investment', 0):,.0f}", f"${cumulative_cf:,.0f}"])
    
    for year in range(1, min(6, project_life + 1)):  # Show first 5 years
        cumulative_cf += annual_cf
        timeline_data.append([
            f"Year {year}",
            "Operating Cash Flow",
            f"${annual_cf:,.0f}",
            f"${cumulative_cf:,.0f}"
        ])
    
    if project_life > 5:
        # Add summary for remaining years
        remaining_years = project_life - 5
        remaining_cf = remaining_years * annual_cf
        cumulative_cf += remaining_cf
        timeline_data.append([
            f"Years 6-{project_life}",
            f"Operating Cash Flow ({remaining_years} years)",
            f"${remaining_cf:,.0f}",
            f"${cumulative_cf:,.0f}"
        ])
    
    create_comparison_table(timeline_data, ["Period", "Description", "Cash Flow", "Cumulative"])
