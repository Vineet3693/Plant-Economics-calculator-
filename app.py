
"""Main Streamlit application file"""
import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from utils.styling import apply_custom_css, create_header, add_footer
from utils.ai_helper import ai_helper
from ui.tabs.tab_interest import show_interest_tab
from ui.tabs.tab_depreciation import show_depreciation_tab
from ui.tabs.tab_profitability import show_profitability_tab
from ui.tabs.tab_cost_estimation import show_cost_estimation_tab
from ui.tabs.tab_breakeven import show_breakeven_tab
from ui.tabs.tab_replacement import show_replacement_tab
from ui.tabs.tab_master import show_master_tab

def main():
    """Main application function"""
    
    # Page configuration
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon=Config.APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom styling
    apply_custom_css()
    
    # Header
    create_header(
        Config.APP_TITLE,
        "Comprehensive Economic Analysis Tool for Chemical Plant Investments"
    )
    
    # Sidebar
    with st.sidebar:
        st.image("assets/logo.png" if os.path.exists("assets/logo.png") else None, width=200)
        
        st.markdown("### 🎯 Navigation")
        st.markdown("""
        Select a tab to perform specific calculations or use the **Master Analysis** 
        for comprehensive evaluation.
        """)
        
        st.markdown("### 🤖 AI Assistant")
        if ai_helper.is_available():
            st.success("✅ AI explanations available")
            st.markdown("Click **'Explain with AI'** buttons for detailed insights.")
        else:
            st.warning("⚠️ AI assistant not configured")
            st.markdown("Set GROQ_API_KEY in .env file to enable AI explanations.")
        
        st.markdown("### 📚 About")
        st.markdown("""
        This tool helps chemical engineers perform comprehensive economic analysis including:
        
        - **Interest & TVM**: Time value of money calculations
        - **Depreciation**: Equipment depreciation analysis  
        - **Profitability**: NPV, IRR, ROI calculations
        - **Cost Estimation**: Plant cost estimation methods
        - **Break-Even**: Break-even and sensitivity analysis
        - **Replacement**: Equipment replacement decisions
        - **Master Analysis**: Complete project evaluation
        """)
        
        st.markdown("### 🔧 Quick Tips")
        with st.expander("Input Guidelines"):
            st.markdown("""
            - Enter realistic values based on your project
            - Use consistent units (all costs in same currency)
            - Consider industry-specific factors
            - Validate results with engineering judgment
            """)
        
        with st.expander("Interpretation Help"):
            st.markdown("""
            - **NPV > 0**: Project adds value
            - **IRR > Cost of Capital**: Project acceptable
            - **Payback < 5 years**: Generally good
            - **Break-even < 80% capacity**: Safe margin
            """)
    
    # Main content tabs
    tab_names = [
        "💰 Interest & TVM",
        "📉 Depreciation", 
        "📈 Profitability",
        "🏭 Cost Estimation",
        "⚖️ Break-Even",
        "🔄 Replacement",
        "🎯 Master Analysis"
    ]
    
    tabs = st.tabs(tab_names)
    
    with tabs[0]:
        show_interest_tab()
    
    with tabs[1]:
        show_depreciation_tab()
    
    with tabs[2]:
        show_profitability_tab()
    
    with tabs[3]:
        show_cost_estimation_tab()
    
    with tabs[4]:
        show_breakeven_tab()
    
    with tabs[5]:
        show_replacement_tab()
    
    with tabs[6]:
        show_master_tab()
    
    # Footer
    add_footer()
    
    # Session state cleanup
    if st.button("🗑️ Clear All Data", key="clear_all"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

if __name__ == "__main__":
    main()
