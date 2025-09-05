
"""Plotting utilities for visualizations"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import Config

def plot_compound_interest_growth(principal, interest_rate, periods):
    """Create compound interest growth chart"""
    years = list(range(0, periods + 1))
    values = [principal * (1 + interest_rate) ** year for year in years]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=values,
        mode='lines+markers',
        name='Investment Value',
        line=dict(color=Config.PRIMARY_COLOR, width=3)
    ))
    
    fig.update_layout(
        title='Compound Interest Growth Over Time',
        xaxis_title='Years',
        yaxis_title='Value ($)',
        hovermode='x unified',
        height=Config.CHART_HEIGHT
    )
    
    return fig

def plot_depreciation_comparison(depreciation_results):
    """Create depreciation comparison chart"""
    fig = go.Figure()
    
    for method, result in depreciation_results.items():
        if 'depreciation_table' in result:
            table = result['depreciation_table']
            fig.add_trace(go.Scatter(
                x=table['Year'],
                y=table['Book_Value'],
                mode='lines+markers',
                name=f'{method} Method',
                line=dict(width=3)
            ))
    
    fig.update_layout(
        title='Depreciation Methods Comparison - Book Value Over Time',
        xaxis_title='Years',
        yaxis_title='Book Value ($)',
        hovermode='x unified',
        height=Config.CHART_HEIGHT
    )
    
    return fig

def plot_cash_flow_analysis(cash_flow_df):
    """Create cash flow analysis chart"""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=['Cumulative Cash Flow', 'Annual Cash Flow'],
        vertical_spacing=0.15
    )
    
    # Cumulative cash flow
    fig.add_trace(
        go.Scatter(
            x=cash_flow_df['Year'],
            y=cash_flow_df['Cumulative_Cash_Flow'],
            mode='lines+markers',
            name='Cumulative Cash Flow',
            line=dict(color=Config.PRIMARY_COLOR, width=3)
        ),
        row=1, col=1
    )
    
    # Add break-even line
    fig.add_hline(y=0, line_dash="dash", line_color="red", row=1, col=1)
    
    # Annual cash flow bars
    colors = ['red' if x < 0 else 'green' for x in cash_flow_df['Cash_Flow']]
    fig.add_trace(
        go.Bar(
            x=cash_flow_df['Year'],
            y=cash_flow_df['Cash_Flow'],
            name='Annual Cash Flow',
            marker_color=colors
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        title='Cash Flow Analysis',
        height=Config.CHART_HEIGHT * 1.5,
        showlegend=True
    )
    
    fig.update_xaxes(title_text="Years", row=2, col=1)
    fig.update_yaxes(title_text="Cumulative ($)", row=1, col=1)
    fig.update_yaxes(title_text="Annual ($)", row=2, col=1)
    
    return fig

def plot_breakeven_analysis(chart_data, breakeven_units):
    """Create break-even analysis chart"""
    fig = go.Figure()
    
    # Revenue line
    fig.add_trace(go.Scatter(
        x=chart_data['Volume'],
        y=chart_data['Revenue'],
        mode='lines',
        name='Total Revenue',
        line=dict(color='green', width=3)
    ))
    
    # Total cost line
    fig.add_trace(go.Scatter(
        x=chart_data['Volume'],
        y=chart_data['Total_Cost'],
        mode='lines',
        name='Total Cost',
        line=dict(color='red', width=3)
    ))
    
    # Fixed cost line
    fig.add_trace(go.Scatter(
        x=chart_data['Volume'],
        y=chart_data['Fixed_Cost'],
        mode='lines',
        name='Fixed Cost',
        line=dict(color='orange', width=2, dash='dash')
    ))
    
    # Break-even point
    breakeven_revenue = breakeven_units * chart_data['Revenue'].iloc[-1] / chart_data['Volume'].iloc[-1]
    fig.add_trace(go.Scatter(
        x=[breakeven_units],
        y=[breakeven_revenue],
        mode='markers',
        name='Break-Even Point',
        marker=dict(color='blue', size=12, symbol='diamond')
    ))
    
    # Profit/Loss areas
    fig.add_trace(go.Scatter(
        x=chart_data['Volume'],
        y=chart_data['Profit'],
        fill='tozeroy',
        name='Profit/Loss',
        fillcolor='rgba(0,255,0,0.3)',
        line=dict(color='rgba(0,0,0,0)')
    ))
    
    fig.update_layout(
        title='Break-Even Analysis',
        xaxis_title='Production Volume (units)',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        height=Config.CHART_HEIGHT
    )
    
    return fig

def plot_sensitivity_analysis(sensitivity_data):
    """Create sensitivity analysis chart"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Fixed Costs Impact', 'Selling Price Impact', 
                       'Variable Cost Impact', 'Volume Impact'],
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Fixed costs sensitivity
    fc_data = sensitivity_data['fixed_costs_sensitivity']
    fig.add_trace(
        go.Scatter(
            x=[item['change_percent'] for item in fc_data],
            y=[item['new_profit'] for item in fc_data],
            mode='lines+markers',
            name='Fixed Costs',
            line=dict(color=Config.PRIMARY_COLOR)
        ),
        row=1, col=1
    )
    
    # Selling price sensitivity
    sp_data = sensitivity_data['selling_price_sensitivity']
    fig.add_trace(
        go.Scatter(
            x=[item['change_percent'] for item in sp_data],
            y=[item['new_profit'] for item in sp_data],
            mode='lines+markers',
            name='Selling Price',
            line=dict(color=Config.SUCCESS_COLOR)
        ),
        row=1, col=2
    )
    
    # Variable cost sensitivity
    vc_data = sensitivity_data['variable_cost_sensitivity']
    fig.add_trace(
        go.Scatter(
            x=[item['change_percent'] for item in vc_data],
            y=[item['new_profit'] for item in vc_data],
            mode='lines+markers',
            name='Variable Costs',
            line=dict(color=Config.WARNING_COLOR)
        ),
        row=2, col=1
    )
    
    # Volume sensitivity
    vol_data = sensitivity_data['volume_sensitivity']
    fig.add_trace(
        go.Scatter(
            x=[item['change_percent'] for item in vol_data],
            y=[item['new_profit'] for item in vol_data],
            mode='lines+markers',
            name='Volume',
            line=dict(color=Config.ERROR_COLOR)
        ),
        row=2, col=2
    )
    
    # Add zero profit line to all subplots
    for row in [1, 2]:
        for col in [1, 2]:
            fig.add_hline(y=0, line_dash="dash", line_color="red", row=row, col=col)
    
    fig.update_layout(
        title='Sensitivity Analysis - Impact on Profit',
        height=Config.CHART_HEIGHT * 1.2,
        showlegend=False
    )
    
    # Update axes
    for row in [1, 2]:
        for col in [1, 2]:
            fig.update_xaxes(title_text="Change (%)", row=row, col=col)
            fig.update_yaxes(title_text="Profit ($)", row=row, col=col)
    
    return fig

def plot_cost_breakdown_pie(cost_breakdown):
    """Create cost breakdown pie chart"""
    categories = list(cost_breakdown['costs'].keys())
    values = list(cost_breakdown['costs'].values())
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=values,
        textinfo='label+percent',
        textposition='outside',
        hole=0.3
    )])
    
    fig.update_layout(
        title='Plant Cost Breakdown',
        height=Config.CHART_HEIGHT,
        showlegend=True
    )
    
    return fig

def plot_replacement_analysis(replacement_options):
    """Create replacement timing analysis chart"""
    years = [option['replace_after_years'] for option in replacement_options]
    costs = [option['total_present_worth'] for option in replacement_options]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=costs,
        mode='lines+markers',
        name='Total Present Worth',
        line=dict(color=Config.PRIMARY_COLOR, width=3),
        marker=dict(size=8)
    ))
    
    # Highlight optimal point
    min_cost_idx = costs.index(min(costs))
    fig.add_trace(go.Scatter(
        x=[years[min_cost_idx]],
        y=[costs[min_cost_idx]],
        mode='markers',
        name='Optimal Replacement Time',
        marker=dict(color='red', size=15, symbol='star')
    ))
    
    fig.update_layout(
        title='Equipment Replacement Timing Analysis',
        xaxis_title='Years Before Replacement',
        yaxis_title='Total Present Worth Cost ($)',
        hovermode='x unified',
        height=Config.CHART_HEIGHT
    )
    
    return fig

def plot_npv_sensitivity(base_npv, discount_rates):
    """Create NPV sensitivity to discount rate"""
    # This would require recalculating NPV for different discount rates
    # Simplified version for demonstration
    npv_values = [base_npv * (1.2 - rate/100) for rate in discount_rates]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=discount_rates,
        y=npv_values,
        mode='lines+markers',
        name='NPV',
        line=dict(color=Config.PRIMARY_COLOR, width=3)
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    
    fig.update_layout(
        title='NPV Sensitivity to Discount Rate',
        xaxis_title='Discount Rate (%)',
        yaxis_title='Net Present Value ($)',
        height=Config.CHART_HEIGHT
    )
    
    return fig

def create_dashboard_metrics(results_dict):
    """Create dashboard-style metrics display"""
    metrics = []
    
    if 'npv' in results_dict:
        color = "green" if results_dict['npv'] > 0 else "red"
        metrics.append({
            'title': 'Net Present Value',
            'value': f"${results_dict['npv']:,.0f}",
            'color': color
        })
    
    if 'irr_percent' in results_dict:
        metrics.append({
            'title': 'Internal Rate of Return',
            'value': f"{results_dict['irr_percent']:.1f}%",
            'color': "blue"
        })
    
    if 'payback_period' in results_dict:
        metrics.append({
            'title': 'Payback Period',
            'value': f"{results_dict['payback_period']:.1f} years",
            'color': "purple"
        })
    
    if 'breakeven_units' in results_dict:
        metrics.append({
            'title': 'Break-Even Volume',
            'value': f"{results_dict['breakeven_units']:,.0f} units",
            'color': "orange"
        })
    
    return metrics

