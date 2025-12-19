import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# Set the page configuration
st.set_page_config(
    page_title="FinServe: Credit Risk Assessment",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enterprise-level styling
st.markdown("""
    <style>
    /* Main styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #667eea;
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    /* Risk level colors */
    .risk-excellent {
        color: #10b981;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    .risk-good {
        color: #3b82f6;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    .risk-average {
        color: #f59e0b;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    .risk-poor {
        color: #ef4444;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    /* Input styling */
    .stNumberInput > div > div > input {
        border-radius: 8px;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 8px;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Results container */
    .results-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-top: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Try to import the prediction helper
try:
    from prediction_helper import predict
except ImportError as e:
    st.error(f"Error importing prediction_helper: {str(e)}")
    st.stop()
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.info("Please ensure the model file exists at: artifacts/model_data.joblib")
    st.stop()

# Main Header
st.markdown("""
    <div class="main-header">
        <h1>🏦 FinServe</h1>
        <p>Enterprise Credit Risk Assessment Platform</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">AI-Powered Credit Scoring & Risk Analysis</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for additional information
with st.sidebar:
    st.markdown("### 📋 Application Information")
    st.markdown("---")
    st.markdown("**Assessment Date:**")
    st.write(datetime.now().strftime("%B %d, %Y"))
    st.markdown("**Model Version:** 1.0")
    st.markdown("**Status:** ✅ Active")
    
    st.markdown("---")
    st.markdown("### 📊 Credit Score Ranges")
    st.markdown("""
    - **Excellent:** 750 - 900
    - **Good:** 650 - 749
    - **Average:** 500 - 649
    - **Poor:** 300 - 499
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This platform uses advanced machine learning 
    models to assess credit risk and calculate 
    credit scores based on applicant information.
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">📝 Applicant Information</div>', unsafe_allow_html=True)
    
    # Personal Information Section
    st.markdown("#### 👤 Personal Details")
    personal_col1, personal_col2, personal_col3 = st.columns(3)
    
    with personal_col1:
        age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28, help="Applicant's age")
    with personal_col2:
        income = st.number_input('Annual Income (₹)', min_value=0, value=1200000, step=10000, format="%d", help="Total annual income")
    with personal_col3:
        loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=2560000, step=10000, format="%d", help="Requested loan amount")
    
    # Calculate and display Loan to Income Ratio
    loan_to_income_ratio = loan_amount / income if income > 0 else 0
    
    # Loan Information Section
    st.markdown("#### 💰 Loan Details")
    loan_col1, loan_col2, loan_col3 = st.columns(3)
    
    with loan_col1:
        loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36, help="Loan repayment period in months")
    with loan_col2:
        loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'], help="Purpose of the loan")
    with loan_col3:
        loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'], help="Type of loan security")
    
    # Credit History Section
    st.markdown("#### 📈 Credit History")
    credit_col1, credit_col2, credit_col3 = st.columns(3)
    
    with credit_col1:
        avg_dpd_per_delinquency = st.number_input('Average DPD', min_value=0, value=20, step=1, help="Average Days Past Due per delinquency")
    with credit_col2:
        delinquency_ratio = st.number_input('Delinquency Ratio (%)', min_value=0, max_value=100, step=1, value=30, help="Percentage of delinquent accounts")
    with credit_col3:
        credit_utilization_ratio = st.number_input('Credit Utilization Ratio (%)', min_value=0, max_value=100, step=1, value=30, help="Percentage of credit used")
    
    # Additional Information Section
    st.markdown("#### 🏠 Additional Information")
    additional_col1, additional_col2 = st.columns(2)
    
    with additional_col1:
        residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'], help="Type of residence")
    with additional_col2:
        num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2, help="Number of currently open loan accounts")

with col2:
    st.markdown('<div class="section-header">📊 Quick Metrics</div>', unsafe_allow_html=True)
    
    # Display key metrics
    st.metric("Loan to Income Ratio", f"{loan_to_income_ratio:.2f}", help="Ratio of loan amount to annual income")
    
    # Visual indicator for loan to income ratio
    if loan_to_income_ratio > 0:
        ratio_percentage = min(loan_to_income_ratio * 10, 100)  # Scale for visualization
        st.progress(ratio_percentage / 100)
        
        if loan_to_income_ratio > 3:
            st.warning("⚠️ High loan-to-income ratio")
        elif loan_to_income_ratio > 2:
            st.info("ℹ️ Moderate loan-to-income ratio")
        else:
            st.success("✅ Healthy loan-to-income ratio")
    
    st.markdown("---")
    st.markdown("### 📋 Input Summary")
    st.markdown(f"""
    - **Age:** {age} years
    - **Income:** ₹{income:,.0f}
    - **Loan Amount:** ₹{loan_amount:,.0f}
    - **Tenure:** {loan_tenure_months} months
    - **Purpose:** {loan_purpose}
    - **Type:** {loan_type}
    """)

# Calculate Risk Button
st.markdown("---")
calculate_col1, calculate_col2, calculate_col3 = st.columns([1, 2, 1])

with calculate_col2:
    calculate_button = st.button('🔍 Calculate Credit Risk', use_container_width=True)

# Results Section
if calculate_button:
    with st.spinner('🔄 Analyzing credit risk... Please wait.'):
        try:
            # Call the predict function
            probability, credit_score, rating = predict(
                age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                                                delinquency_ratio, credit_utilization_ratio, num_open_accounts,
                residence_type, loan_purpose, loan_type
            )
            
            # Display results in an enterprise-style layout
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">📊 Risk Assessment Results</div>', unsafe_allow_html=True)
            
            # Main results in columns
            result_col1, result_col2, result_col3 = st.columns(3)
            
            # Credit Score with visual gauge
            with result_col1:
                st.markdown("### Credit Score")
                # Determine color based on rating
                color_map = {
                    'Excellent': '#10b981',
                    'Good': '#3b82f6',
                    'Average': '#f59e0b',
                    'Poor': '#ef4444'
                }
                score_color = color_map.get(rating, '#6b7280')
                
                # Create gauge chart
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = credit_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Credit Score"},
                    delta = {'reference': 650},
                    gauge = {
                        'axis': {'range': [None, 900]},
                        'bar': {'color': score_color},
                        'steps': [
                            {'range': [0, 500], 'color': "lightgray"},
                            {'range': [500, 650], 'color': "gray"},
                            {'range': [650, 750], 'color': "lightblue"},
                            {'range': [750, 900], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 500
                        }
                    }
                ))
                fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Default Probability
            with result_col2:
                st.markdown("### Default Probability")
                # Create probability bar chart
                prob_percentage = probability * 100
                fig_prob = go.Figure(go.Bar(
                    x=[prob_percentage],
                    y=['Risk Level'],
                    orientation='h',
                    marker=dict(
                        color=prob_percentage,
                        colorscale='RdYlGn',
                        reversescale=True,
                        showscale=True,
                        cmin=0,
                        cmax=100
                    ),
                    text=[f"{prob_percentage:.2f}%"],
                    textposition='inside',
                ))
                fig_prob.update_layout(
                    height=250,
                    xaxis=dict(range=[0, 100], title="Probability (%)"),
                    yaxis=dict(showticklabels=False),
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig_prob, use_container_width=True)
                
                # Risk level indicator
                if prob_percentage < 10:
                    risk_level = "🟢 Low Risk"
                    risk_color = "#10b981"
                elif prob_percentage < 25:
                    risk_level = "🟡 Moderate Risk"
                    risk_color = "#f59e0b"
                elif prob_percentage < 50:
                    risk_level = "🟠 High Risk"
                    risk_color = "#f97316"
                else:
                    risk_level = "🔴 Very High Risk"
                    risk_color = "#ef4444"
                
                st.markdown(f"<h3 style='color: {risk_color}; text-align: center;'>{risk_level}</h3>", unsafe_allow_html=True)
            
            # Rating
            with result_col3:
                st.markdown("### Credit Rating")
                rating_emoji = {
                    'Excellent': '⭐',
                    'Good': '👍',
                    'Average': '⚠️',
                    'Poor': '❌'
                }
                emoji = rating_emoji.get(rating, '❓')
                
                rating_class = f"risk-{rating.lower()}"
                st.markdown(f"<div style='text-align: center; padding: 2rem;'>", unsafe_allow_html=True)
                st.markdown(f"<h1 style='font-size: 4rem; margin: 0;'>{emoji}</h1>", unsafe_allow_html=True)
                st.markdown(f"<h2 class='{rating_class}' style='text-align: center;'>{rating}</h2>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Detailed metrics
            st.markdown("---")
            st.markdown("### 📈 Detailed Metrics")
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric("Default Probability", f"{probability:.2%}", delta=None)
            with metric_col2:
                st.metric("Credit Score", f"{credit_score}", delta=f"{credit_score - 650}")
            with metric_col3:
                st.metric("Credit Rating", rating)
            with metric_col4:
                non_default_prob = (1 - probability) * 100
                st.metric("Repayment Probability", f"{non_default_prob:.2f}%")
            
            # Recommendation section
            st.markdown("---")
            st.markdown("### 💡 Recommendations")
            
            if rating == "Excellent":
                st.success("✅ **Excellent Credit Profile**: This applicant demonstrates exceptional creditworthiness. Recommend approval with favorable terms.")
            elif rating == "Good":
                st.info("✅ **Good Credit Profile**: This applicant shows strong creditworthiness. Recommend approval with standard terms.")
            elif rating == "Average":
                st.warning("⚠️ **Average Credit Profile**: This applicant has moderate credit risk. Recommend approval with additional conditions or higher interest rate.")
            else:
                st.error("❌ **Poor Credit Profile**: This applicant presents significant credit risk. Recommend rejection or require additional collateral/guarantor.")
            
            # Risk factors visualization
            st.markdown("---")
            st.markdown("### 🔍 Risk Factor Analysis")
            
            risk_factors = {
                "Loan-to-Income Ratio": min(loan_to_income_ratio / 3 * 100, 100),
                "Delinquency Ratio": delinquency_ratio,
                "Credit Utilization": credit_utilization_ratio,
                "Average DPD": min(avg_dpd_per_delinquency / 30 * 100, 100)
            }
            
            risk_df = pd.DataFrame(list(risk_factors.items()), columns=['Factor', 'Risk Score'])
            risk_df = risk_df.sort_values('Risk Score', ascending=False)
            
            fig_risk = px.bar(
                risk_df,
                x='Risk Score',
                y='Factor',
                orientation='h',
                color='Risk Score',
                color_continuous_scale='RdYlGn',
                range_color=[0, 100],
                title="Risk Factor Analysis"
            )
            fig_risk.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_risk, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error calculating risk: {str(e)}")
            st.info("Please check that all inputs are valid and the model file is accessible.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 1rem;'>
        <p>© 2024 FinServe | Enterprise Credit Risk Assessment Platform</p>
        
    </div>
""", unsafe_allow_html=True)
