
"""Groq LLM integration for AI explanations"""
import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class AIHelper:
    def __init__(self):
        """Initialize Groq client"""
        self.api_key = os.getenv('GROQ_API_KEY')
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None
            
    def is_available(self):
        """Check if AI helper is available"""
        return self.client is not None and self.api_key is not None
    
    def explain_interest_calculation(self, inputs, results):
        """Explain interest and time value calculations"""
        prompt = f"""
        You are a Chemical Engineering Economics expert. Explain the following Interest/Time Value of Money calculation in simple, practical terms:
        
        Inputs:
        - Principal Investment: ${inputs.get('principal', 0):,.2f}
        - Interest Rate: {inputs.get('interest_rate', 0):.2f}%
        - Time Period: {inputs.get('periods', 0)} years
        
        Results:
        - Future Value: ${results.get('future_value', 0):,.2f}
        - Total Interest: ${results.get('compound_interest', 0):,.2f}
        
        Please provide:
        1. What this calculation tells us about the investment
        2. Real-world implications for plant economics decisions
        3. Risk factors to consider
        4. A simple analogy to explain compound growth
        
        Keep the explanation practical and focused on chemical plant investment decisions.
        """
        
        return self._get_ai_response(prompt)
    
    def explain_depreciation_analysis(self, inputs, results):
        """Explain depreciation calculation results"""
        prompt = f"""
        You are a Chemical Engineering Economics expert. Explain this depreciation analysis:
        
        Equipment Details:
        - Purchase Cost: ${inputs.get('purchase_cost', 0):,.2f}
        - Salvage Value: ${inputs.get('salvage_value', 0):,.2f}
        - Useful Life: {inputs.get('useful_life', 0)} years
        - Method: {inputs.get('method', 'N/A')}
        
        Results:
        - Annual Depreciation: ${results.get('annual_depreciation', 0):,.2f}
        - Current Book Value: ${results.get('current_book_value', 0):,.2f}
        
        Please explain:
        1. What depreciation means for this equipment
        2. Tax implications and cash flow impact
        3. Why this method is appropriate for chemical equipment
        4. How this affects replacement decisions
        
        Focus on practical implications for plant operations and financial planning.
        """
        
        return self._get_ai_response(prompt)
    
    def explain_profitability_analysis(self, inputs, results):
        """Explain profitability analysis results"""
        prompt = f"""
        You are a Chemical Engineering Economics expert. Analyze this plant profitability assessment:
        
        Investment Details:
        - Initial Investment: ${inputs.get('initial_investment', 0):,.2f}
        - Annual Cash Flow: ${inputs.get('annual_cash_flow', 0):,.2f}
        - Project Life: {inputs.get('project_life', 0)} years
        - Discount Rate: {inputs.get('discount_rate', 0):.2f}%
        
        Results:
        - NPV: ${results.get('npv', 0):,.2f}
        - IRR: {results.get('irr_percent', 0):.2f}%
        - ROI: {results.get('roi_percent', 0):.2f}%
        - Payback Period: {results.get('payback_period', 0):.2f} years
        
        Please provide:
        1. Investment decision recommendation (Accept/Reject and why)
        2. Risk assessment and sensitivity concerns
        3. How this compares to typical chemical plant investments
        4. Key factors that could change the decision
        
        Focus on practical business decision-making for chemical plant investments.
        """
        
        return self._get_ai_response(prompt)
    
    def explain_cost_estimation(self, inputs, results):
        """Explain cost estimation results"""
        prompt = f"""
        You are a Chemical Engineering Economics expert. Explain this plant cost estimation:
        
        Estimation Parameters:
        - Base Equipment Cost: ${inputs.get('equipment_cost', 0):,.2f}
        - Industry Type: {inputs.get('industry_type', 'Chemical Processing')}
        - Scaling Factor: {inputs.get('scaling_factor', 'N/A')}
        
        Results:
        - Total Plant Cost: ${results.get('total_plant_cost', 0):,.2f}
        - Installation Cost: ${results.get('installation_cost', 0):,.2f}
        - Working Capital: ${results.get('working_capital', 0):,.2f}
        
        Please explain:
        1. Why the total cost is much higher than equipment cost
        2. Key cost components and their importance
        3. Accuracy and reliability of this estimation method
        4. Factors that could cause actual costs to vary
        
        Focus on helping engineers understand the full scope of plant investment costs.
        """
        
        return self._get_ai_response(prompt)
    
    def explain_breakeven_analysis(self, inputs, results):
        """Explain break-even analysis results"""
        prompt = f"""
        You are a Chemical Engineering Economics expert. Analyze this break-even calculation:
        
        Operating Parameters:
        - Fixed Costs: ${inputs.get('fixed_costs', 0):,.2f}
        - Variable Cost per Unit: ${inputs.get('variable_cost', 0):,.2f}
        - Selling Price per Unit: ${inputs.get('selling_price', 0):,.2f}
        
        Results:
        - Break-even Volume: {results.get('breakeven_units', 0):,.0f} units
        - Break-even Sales: ${results.get('breakeven_sales', 0):,.2f}
        - Contribution Margin: ${results.get('contribution_margin_per_unit', 0):,.2f} per unit
        
        Please provide:
        1. What this break-even volume means for plant operations
        2. How sensitive the results are to price/cost changes
        3. Operational challenges in achieving this volume
        4. Strategic implications for plant capacity and market positioning
        
        Focus on practical operational and strategic insights for chemical plant management.
        """
        
        return self._get_ai_response(prompt)
    
    def explain_replacement_analysis(self, inputs, results):
        """Explain equipment replacement analysis"""
        prompt = f"""
        You are a Chemical Engineering Economics expert. Analyze this equipment replacement decision:
        
        Current Equipment:
        - Current Value: ${inputs.get('old_salvage_value', 0):,.2f}
        - Annual Operating Cost: ${inputs.get('old_annual_cost', 0):,.2f}
        
        New Equipment:
        - Purchase Cost: ${inputs.get('new_equipment_cost', 0):,.2f}
        - Annual Operating Cost: ${inputs.get('new_annual_cost', 0):,.2f}
        - Expected Life: {inputs.get('new_equipment_life', 0)} years
        
        Analysis Results:
        - Net Investment: ${results.get('net_investment', 0):,.2f}
        - Annual Savings: ${results.get('annual_savings', 0):,.2f}
        - Recommendation: {results.get('recommendation', 'N/A')}
        
        Please explain:
        1. The economic logic behind this recommendation
        2. Non-economic factors to consider (reliability, technology, etc.)
        3. Timing considerations and risks
        4. How this fits into overall plant maintenance strategy
        
        Focus on practical maintenance and capital investment decision-making.
        """
        
        return self._get_ai_response(prompt)
    
    def generate_comprehensive_analysis(self, all_results):
        """Generate comprehensive analysis of all calculations"""
        prompt = f"""
        You are a Chemical Engineering Economics expert. Provide a comprehensive analysis of this complete plant economics evaluation:
        
        Key Results Summary:
        - Total Investment: ${all_results.get('total_investment', 0):,.2f}
        - NPV: ${all_results.get('npv', 0):,.2f}
        - IRR: {all_results.get('irr', 0):.2f}%
        - Break-even Volume: {all_results.get('breakeven_units', 0):,.0f} units
        - Payback Period: {all_results.get('payback_period', 0):.2f} years
        
        Please provide:
        1. EXECUTIVE SUMMARY: Overall investment attractiveness
        2. KEY RISKS: Major economic and operational risks
        3. SENSITIVITY FACTORS: What could significantly change outcomes
        4. RECOMMENDATIONS: Specific actions and next steps
        5. BENCHMARKING: How this compares to typical chemical plant projects
        
        Structure as a professional economic evaluation report for management decision-making.
        """
        
        return self._get_ai_response(prompt)
    
    def _get_ai_response(self, prompt):
        """Get response from Groq LLM"""
        if not self.is_available():
            return "AI explanations are not available. Please configure your GROQ_API_KEY in the .env file."
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating AI explanation: {str(e)}"

# Global AI helper instance
ai_helper = AIHelper()
