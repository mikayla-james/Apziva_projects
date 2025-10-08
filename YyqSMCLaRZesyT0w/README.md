# Client Summary Report

## Project Objective
This project aimed to build and evaluate predictive models that identify customers most likely to subscribe to a **term deposit**.  
Primary performance metric: **AUC-PR (Average Precision)**, emphasizing precision–recall balance for the minority (positive) class.

---

## Model Performance Overview

Three models were developed and compared:

| Model | Key Strength | Summary of Test Performance |
|-------|---------------|-----------------------------|
| **Logistic Regression** | Simple baseline, interpretable coefficients | Precision: 0.12 Recall: 0.49 F1-Score: 0.20 Accuracy: 0.66 |
| **Random Forest** | Nonlinear model capturing complex relationships | Precision: 0.51 Recall: 0.73 F1-Score: 0.60 Accuracy: 0.92 |
| **XGBoost** | Optimized gradient-boosted ensemble, best precision–recall balance | Highest AUC-PR among all models (clear dominance over Random Forest and Logistic Regression) |

**Random Forest Best Parameters:**
```
n_estimators = 600
max_depth = 24
min_samples_split = 5
min_samples_leaf = 4
max_features = 0.5
max_samples = 0.5
oob_score = True
```

**Performance Summary**
- XGBoost achieved the **highest AUC-PR** and **ROC-AUC** values.
- Both tree-based models improved recall and precision for positive outcomes.
- Logistic Regression provided a reliable, interpretable baseline.

---

## Feature Importance Insights

Analysis combined **model-derived importance** and **SHAP interpretability** to ensure transparency.

| Rank | Feature | Influence Summary |
|------|----------|-------------------|
| 1 | **Duration** | Strongest positive effect. Longer call durations increased likelihood of subscription. |
| 2 | **Poutcome_success** | Prior successful outcomes strongly predicted future success. |
| 3 | **Previous (contacts)** | Moderate positive effect; diminishing returns after many contacts. |
| 4 | **Contact Type** | Cellular contacts outperformed traditional calls. |
| 5 | **Age** | Older customers showed slightly higher conversion rates. |
| 6 | **Balance & Education** | Socioeconomic indicators had moderate influence. |

Negative influences included **default = yes** and excessive prior contacts.

**Interpretability Tools Used**
- **SHAP Waterfall plots** for per-customer explanations.
- **Tree-based importance plots** for global ranking.

---

## Conclusions

- **XGBoost** provided the strongest predictive precision and generalization.
- **Duration** and **past campaign success** were the top predictive drivers.
- The model suite is **interpretable, scalable, and business-ready**.

**Recommended Next Steps**
1. Deploy XGBoost for live campaign predictions.  
2. Integrate SHAP-based visualization dashboard.  
3. Retrain quarterly with updated customer data.

---
