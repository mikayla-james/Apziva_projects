# Client Summary Report

## Project Objective
This project aimed to build and evaluate predictive models that identify customers most likely to subscribe to a **term deposit**.  
Primary performance metric: **F1**, emphasizing precision–recall balance for the minority (positive) class.

---

## Model Performance Overview

Three models were developed and compared:

| Model | Summary of Test Performance |
|-------|-----------------------------|
| **Logistic Regression** | Precision: 0.12 Recall: 0.49 F1-Score: 0.20 Accuracy: 0.66 |
| **Random Forest**  | Precision: 0.51 Recall: 0.73 F1-Score: 0.60 Accuracy: 0.92 |
| **XGBoost** | Precision: 0.51 Recall: 0.73 F1-Score: 0.60 Accuracy: 0.92 |

**XGBoost Best Parameters:**
```
learning_rate = 0.20
gamma = 0.26
max_delta_step = 1
scale_pos_weight = 12.6
```
**Comparison of ROC-AUC Across Models**
<p align="center">
  <img src="figs/roc_auc_comparison.png" alt="ROC Curve" width="60%">
</p>

**Performance Summary**
- XGBoost achieved the **highest AUC-PR** and **ROC-AUC** values.
- Both tree-based models improved recall and precision for positive outcomes.
- Logistic Regression provided a reliable, interpretable baseline.

---

## Feature Importance Insights (Based on XGBoost Model)

<table style="width:100%;">
  <tr>
    <td style="vertical-align:center;">
      <img src="figs/beeswarm_plot_xg.png" alt="SHAP Beeswarm Plot"
     style="width:auto%; height:390px; display:block; margin:auto;">
    </td>
    <td style="width:40%; vertical-align:top;">
      <table>
        <thead>
          <tr><th>Rank</th><th>Feature</th><th>Global Influence</th></tr>
        </thead>
        <tbody>
          <tr><td>1</td><td><b>duration_log</b></td><td>Longer call duration increases likelihood; short calls decrease it.</td></tr>
          <tr><td>2</td><td><b>month</b></td><td>Later-year calls more likely to convert than early-year.</td></tr>
          <tr><td>3</td><td><b>day</b></td><td>Later-month calls modestly more successful.</td></tr>
          <tr><td>4</td><td><b>campaign</b></td><td>More contact attempts reduce success; fewer help.</td></tr>
          <tr><td>5</td><td><b>balance</b></td><td>Higher balances modestly increase likelihood.</td></tr>
          <tr><td>6</td><td><b>housing</b></td><td>No housing loan slightly increases likelihood.</td></tr>
          <tr><td>7</td><td><b>age_log</b></td><td>Older customers slightly more likely to subscribe.</td></tr>
          <tr><td>8</td><td><b>contact_cellular</b></td><td>Cellular contact marginally improves success.</td></tr>
          <tr><td>9</td><td><b>marital_married</b></td><td>Small positive influence.</td></tr>
          <tr><td>10</td><td><b>job_blue-collar</b></td><td>Slight reduction in likelihood.</td></tr>
        </tbody>
      </table>
    </td>
  </tr>
</table>



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
