 # PortfolioGuard - Credit Risk Intelligence Platform

 A retail credit portfolio risk analytics tool built on 2.26 million LendingClub loan records(2007-2018). Designed to address the challenges facing retail banking risk teams: moving from reactive, manual reporting to proactive, data-driven portfolio monitoring. 
 ---

 ## Business Context  

Retail lenders face growing pressure to monitor credit portfolio health proactively. For a lender operating at scale, the inability to rapidly segment risk exposure by borrower profile, product type, or geography creates both capital efficiency gaps and regulatory reporting risk under Basel III.  

PortfolioGuard delivers an on-demand credit portfolio intelligence tool - a risk-tiered scorecard and probability of default model - enabling Credit Risk and Portfolio Management teams to identify concentration risk and flag high-PD segments before losses materialise.
---

## What's Built

### 1. Exploratory Data Analysis (Notebook 1: 01_eda)  
- Target variable definition with documented business rationale
- 75-column reduction - missing data, leakage and redundancy removed
- Business framed EDA: default rate by grade, interest rate and DTI
- Risk Scorecard: Green / Amber / Red tier classification

### 2. Predictive Model - Probability of Default (Notebook 2: 02_model)  
- Logistic regression PD model (industry standard, Basel III compliant)
- 5 model iterations with documented improvement rationale
- Final model: Gini 42.8%, AUC 0.714
- SHAP explainability - feature contribution analysis
- Key findings: **interest rate** and **loan grade** are dominant default predictors

### 3. PortfolioGuard Dashboard (Streamlit)
- **Portfolio Overview** - KPI Cards, Default Rate by Grade, Loan Purpose
- **Risk Scorecard** - G/A/R tier distribution, default rates by tier
- **Loan Assessment Tool** - live PD scoring for individual borrowers
---

## Risk Scorecard

| Tier | Grade | Interest Rate | DTI | Default Rate |
|---|---|---|---|---|
| 🟢 Green | A–B | < 12% | < 20 | 8.9% |
| 🟡 Amber | C–D | 12–20% | 20–30 | 23.2% |
| 🔴 Red | E–G | > 20% | > 30 | 41.7% |

Portfolio average default rate : 20.5%
---

## Key Findings
1. **Grade is the strongest risk signal** - default rate climbs from 5.3% (Grade A) to 56.5% (Grade G)
2. **Risk based pricing validation** - interest rate tracks default rate consistently across all bands
3. **Portfolio Concentration Risk** - 15% of loans in Red tier carry 41.7% default rate, 4.7x the Green tier
4. **FICO multicollinearity** - FICO adds marginal lift (+0.6% Gini) because grade already encodes credit quality
---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python / pandas / numpy | Data wrangling and EDA |
| scikit-learn | Logistic regression PD model |
| SHAP | Model explainability |
| Streamlit + Plotly | Interactive dashboard |
| Jupyter Notebooks | Analysis and documentation |

---

## Project Structure
```
credit-risk-project/
├── data/
│   └── loans_clean.csv
├── notebooks/
│   ├── 01_eda.ipynb
│   └── 02_model.ipynb
├── src/
│   └── app.py
└── README.md
```
---

## PACE Framework
- **Plan** - Business problem, stakeholders, success metrics
- **Analyse** - EDA, target variable, missing data treatment
- **Construct** - Feature engineering, scorecard, PD model
- **Execute** - Dashboard delivery, validation, documentation

---

## Running the Dashboard

​```bash```
```cd src```
```streamlit run app.py```
​
## Live Dashboard

🔗 [PortfolioGuard - Live App](https://credit-risk-project-h4bger8hnwq7caw6a2bmy5.streamlit.app/)
---

*Dataset: LendingClub Loan Data 2007–2018 (Kaggle)*  
*Author: Shubham Yadav | [LinkedIn](https://linkedin.com/in/sy1394/)*
