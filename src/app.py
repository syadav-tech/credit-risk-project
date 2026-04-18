# ── SECTION 1: IMPORTS ──────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# ── SECTION 2: PAGE CONFIG ───────────────────────────────────
st.set_page_config(
    page_title = "Credit Risk Dashboard",
    page_icon = "🏦",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

# ── SECTION 3: LOAD DATA ─────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('data/loans_clean.csv')
    return df
df = load_data()

# ── SECTION 4: SIDEBAR ───────────────────────────────────────
st.sidebar.markdown("## 🏦 PortfolioGuard")
st.sidebar.markdown("*Credit Risk Intelligence Platform*")
st.sidebar.markdown("---")
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Portfolio Overview",
     "Risk Scorecard",
     "Loan Assessment Tool"]
)                    
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Dataset:** LendingClub Loan Data (2007-2018)  
    **Loans:** 44,006  
    **Default Rate:** 20.5%  
    **Model:** Logistic Regression  
    **Gini:** 42.8%  
    """
)

# ── SECTION 5: PAGE 1 - PORTFOLIO OVERVIEW ───────────────────
if page == "Portfolio Overview":
    st.title("Credit Portfolio Overview")
    st.markdown("Executive summary of portfolio health "
                "and risk distribution.")
    st.markdown("---")
        
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    total_loans = len(df)
    default_rate = df['default'].mean()*100
    avg_int_rate = df['int_rate'].mean()
    avg_loan = df['loan_amnt'].mean()

    col1.metric("Total Loans",f"{total_loans:,}")
    col2.metric("Default Rate", f"{default_rate:.1f}%")
    col3.metric("Avg. Interest Rate:",f"{avg_int_rate:.1f}%")
    col4.metric("Avg. Loan Amount:",f"${avg_loan:,.0f}")

    st.markdown("---")

    # Two charts side-by-side
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Default Rate by Loan Grade")
        grade_analysis = df.groupby('grade')['default'].agg(
            total = 'count', defaults = 'sum'
        ).reset_index()

        grade_analysis['default_rate'] = (grade_analysis['defaults']/grade_analysis['total']*100).round(1)

        fig_grade = px.bar(
            grade_analysis,
            x = 'grade',
            y = 'default_rate',
            color_discrete_sequence = ['#2471a3'],
            labels = {'default_rate':'Default Rate %', 'grade':'Loan Grade'},
            text = 'default_rate'
        )
        fig_grade.update_traces(
            texttemplate = '%{text:.1f}%',
            textposition = 'outside'
        )
        fig_grade.update_layout(
            showlegend = False,
            coloraxis_showscale = False,
            height = 400
        )
        st.plotly_chart(fig_grade,use_container_width = True)

    with col_right:
        st.subheader("Portfolio by Loan Purpose")
        purpose_df = df['purpose'].value_counts().head(8).reset_index()
        purpose_df.columns = ['purpose','count']

        fig_purpose = px.bar(
            purpose_df,
            x = 'count',
            y = 'purpose',
            orientation = 'h',
            color_discrete_sequence = ['#2471a3'],
            labels = {'count':'Number of Loans','purpose':'Loan Purpose'}
        )
        fig_purpose.update_layout(
            showlegend = False,
            coloraxis_showscale = False,
            height = 400
        )
        st.plotly_chart(fig_purpose,use_container_width = True)

# ── SECTION 6: PAGE 2 - RISK SCORECARD ───────────────────────

elif page == "Risk Scorecard":
    st.title("🎯 Risk Scorecard")
    st.markdown("Green / Amber / Red Portfolio classification "
                "based on loan grade, interest rate, and DTI.")
    st.markdown("---")

    # KPI cards
    tier_counts = df['risk_tier'].value_counts()
    tier_pcts = (tier_counts/len(df)*100).round(1)

    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Green Tier",
                f"{tier_counts.get('Green', 0):,}",
                f"{tier_pcts.get('Green', 0)}% of portfolio"
                )
    col2.metric("🟡 Amber Tier",
                f"{tier_counts.get('Amber', 0):,}",
                f"{tier_pcts.get('Amber', 0)}% of portfolio"
                )
    col3.metric("🔴 Red Tier",
                f"{tier_counts.get('Red', 0):,}",
                f"{tier_pcts.get('Red',0)}% of portfolio"
                )
    st.markdown("---")

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Portfolio Distribution")
        tier_df = pd.DataFrame({
            'Tier':['Green','Amber','Red'],
            'Count':[tier_counts.get('Green', 0),
                    tier_counts.get('Amber', 0),
                    tier_counts.get('Red', 0)]
        })

        fig_tier = px.pie(
            tier_df, values = 'Count',
            names = 'Tier', color = 'Tier',
            color_discrete_map = {'Green': '#2ecc71',
                    'Amber': '#f39c12',
                    'Red': '#e74c3c'}, hole = 0.4
        )
        fig_tier.update_layout(height = 400)
        st.plotly_chart(fig_tier, use_container_width = True)

    with col_right:
        st.subheader("Default Rate by Tier")
        tier_default = df.groupby('risk_tier')['default'].agg(
            total = 'count', defaults = 'sum'
        ).reset_index()

        tier_default['default_rate'] = (tier_default['defaults']/tier_default['total']*100).round(1)

        tier_order = ['Green','Amber','Red']
        tier_color = {'Green': '#2ecc71',
                'Amber': '#f39c12',
                'Red': '#e74c3c'}
        
        tier_default['order'] = tier_default['risk_tier'].map(
            {'Green':0,
            'Amber':1,
            'Red':2}
        )
        tier_default = tier_default.sort_values('order')

        fig_default = px.bar(
            tier_default,
            x = 'risk_tier',
            y = 'default_rate',
            color = 'risk_tier',
            color_discrete_map = tier_color, 
            labels = {'default_rate':'Default Rate %',
                    'risk_tier':'Risk Tier'},
            text = 'default_rate'
        )
        fig_default.update_traces(
            texttemplate = '%{text:.1f}%',
            textposition = 'outside'
        )
        fig_default.add_hline(
            y = 20.5,
            line_dash = 'dash',
            line_color = 'white',
            annotation_text = 'Portfolio average 20.5%'
        )
        fig_default.update_layout(
            showlegend = False,
            height = 400,
            yaxis = dict(range=[0, tier_default['default_rate'].max()+10])
        )
        st.plotly_chart(fig_default,use_container_width = True)
    st.markdown("---")

    # Scorecard Rules Table

    st.subheader('Scorecard Logic')
    rules_df = pd.DataFrame({
        'Tier': ['🟢 Green', '🟡 Amber', '🔴 Red'],
        'Loan Grade': ['A - B', 'C - D', 'E - G'],
        'Interest Rate': ['<12%', '12% - 20%','>20%'],
        'DTI Ratio': ['<20', '20 - 30', '>30'],
        'Typical Default Rates': ['8.9%','23.2%','41.7%']
    })
    st.dataframe(rules_df,use_container_width = True, hide_index = True)

# ── SECTION 7: PAGE 3 - LOAN ASSESSMENT TOOL ─────────────────
elif page == "Loan Assessment Tool":

    st.title("Loan Assessment Tool")
    st.markdown("Enter borrower details to get an instant "
                "Probability of Default score and Risk Tier.")
    st.markdown("---")

    # Load model dependecy
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    import joblib

    # Rebuild model on Load (notebook v4)
    @st.cache_resource
    def build_model():
        feature_cols_v4 = [
            'loan_amnt','installment', 'annual_inc','int_rate', 'dti',
            'delinq_2yrs', 'inq_last_6mths', 'open_acc', 'pub_rec', 'revol_bal',
            'revol_util', 'total_acc', 'installment_to_income','fico_range_low'
        ]
        # Fix Zero Income Error
        median_income = df[df['annual_inc'] > 0]['annual_inc'].median()
        df['annual_inc'] = df['annual_inc'].replace(0, median_income)

        # Recreate installment to income
        df['installment_to_income'] = (
            df['installment']/ (df['annual_inc']/12)
        )
        X = df[feature_cols_v4]
        y = df['default']
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced')
        model.fit(X_scaled, y)
        return model, scaler, feature_cols_v4
    
    model, scaler, feature_cols = build_model()
    st.markdown("### Borrower Details")
    st.caption("Input fields reflect the model's strongest "
           "predictive features. Low-signal variables "
           "are held at portfolio median values.")

    # Input form - Two Columns
    col1, col2 = st.columns(2)

    with col1:
        loan_amnt = st.number_input(
            "Loan Amount ($)", min_value = 500, max_value = 40000, value = 10000, step = 500)
        int_rate = st.slider(
            "Interest Rate (%)", min_value = 5.0, max_value = 30.0, value = 12.0, step = 0.1)
        annual_inc = st.number_input(
            "Annual Income ($)", min_value = 10000, max_value = 500000, value = 65000, step = 1000)
        dti = st.slider(
            "Debt to Income Ratio", min_value = 0.0, max_value = 50.0, value = 15.0, step = 0.5)
        fico = st.slider(
            "FICO Score", min_value = 500, max_value = 850, value = 700, step = 5)
        
    with col2:
        installment = st.number_input(
            "Monthly Installment ($)", min_value = 10, max_value = 2000, value = 300, step = 10)
        delinq_2yrs = st.number_input(
            "Delinquencies (last 2 years)", min_value = 0, max_value = 20, value = 0)
        inq_last_6mths = st.number_input(
            "Credit Enquiries (last 6 months)", min_value = 0, max_value = 10, value = 1)
        open_acc = st.number_input(
            "Open Credit Lines", min_value = 1, max_value = 50, value = 10)
        pub_rec = st.number_input(
            "Public Derogatory Records", min_value = 0, max_value = 10, value = 0)
        total_acc = st.number_input(
            "Total Credit Lines Ever", min_value = 1, max_value = 100, value = 25)
        revol_bal = st.number_input(
            "Revolving Balance ($)", min_value = 0, max_value = 100000, value = 5000, step = 500)
    # Fixed at median — low predictive value, excluded from UI
    revol_util = 40.0
    st.markdown("---")

    # Assessment Button
    if st.button("Run Assessment", type = "primary"):

        # Calculate derived features
        installment_to_income = installment / (annual_inc/12)

        # Build Input Vector
        input_data = pd.DataFrame([{
            'loan_amnt': loan_amnt,
            'installment':installment,
            'annual_inc': annual_inc,
            'int_rate': int_rate,
            'dti': dti,
            'delinq_2yrs': delinq_2yrs,
            'inq_last_6mths': inq_last_6mths,
            'open_acc': open_acc,
            'pub_rec': pub_rec,
            'revol_bal': revol_bal,
            'revol_util': revol_util,
            'total_acc': total_acc,
            'installment_to_income': installment_to_income,
            'fico_range_low': fico
        }])

        # Scale and Predict
        input_scaled = scaler.transform(input_data)
        pd_score = model.predict_proba(input_scaled)[0][1]

        # Assign Risk Tier
        if pd_score < 0.3:
            tier = "🟢 Green"
            tier_color = "green"
            recommendation = "Low Risk - Standard Approval Process"
        elif pd_score <0.5:
            tier = "🟡 Amber"
            tier_color = "orange"
            recommendation = "Moderate Risk - Enhanced Due Deligence recommended"
        else:
            tier = "🔴 Red"
            tier_color = "red"
            recommendation = "High risk — escalate to senior credit review"
        
        # Display Results
        st.markdown("### Assessment Result")

        res_col1, res_col2, res_col3, = st.columns(3)
        res_col1.metric("Probalility of Default", f"{pd_score*100:.1f}%")
        res_col2.metric("Risk Tier", tier)
        res_col3.metric("Installment-to-Income", f"{installment_to_income*100:.1f}%")

        st.markdown(f"**Recommendation:** {recommendation}")

        # PD Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = pd_score * 100,
            title = {'text': "Probability of Default (%)"},
            gauge = { 'axis': {'range': [0,100]},
                     'bar': {'color': tier_color},
                     'steps': [
                        {'range': [0,30],
                          'color': 'rgba(46,204,113,0.3)'},
                        {'range': [30,50],
                          'color': 'rgba(243,156,18,0.3)'},
                        {'range': [50,100],
                          'color': 'rgba(231,76,60,0.3)'}
                     ],
                     'threshold': {'line': {'color':'white', 'width': 2},
                                   'thickness': 0.75,
                                   'value': pd_score * 100
                                   } 
                    }
        ))

        fig_gauge.update_layout(height = 300)
        st.plotly_chart(fig_gauge, use_container_width = True)
