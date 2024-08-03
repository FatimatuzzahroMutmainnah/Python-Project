## Survival Analysys
### Overview

<p align="left">This project demonstrates the application of survival analysis techniques using Python. Survival analysis is a set of statistical approaches used to investigate the time it takes for an event of interest to occur, such as time to failure of a machine, time to recovery for patients, or customer churn.</p>

### Project Structure

<p align="left">
  - 📑 <strong>Data:</strong> The dataset used for this analysis is sourced from Loprinzi CL. Laurie JA. Wieand HS. et al., "Prospective evaluation of prognostic variables from patient-completed questionnaires," Journal of Clinical Oncology, 1994. It includes data on survival times and various patient characteristics. The dataset contains 200 observations and 6 variables.<br>
  - 📊 <strong>Data Preparation:</strong> Clean and preprocess the data, including handling missing values.<br>
  - 🔎 <strong>Survival Analysis Techniques:</strong> This project explores the following survival analysis methods: the Kaplan-Meier Estimator, which is a non-parametric statistic used to estimate the survival function from lifetime data; the Cox Proportional Hazards Model, a semi-parametric model that examines the relationship between survival time and one or more predictor variables; and the Accelerated Failure Time (AFT) Model, a parametric model that directly models the survival time.<br></p>

### Key Files

<p align="left">
  - <tt>Dengue_Fever_survival.py</tt>: Scripts for implementing and visualizing the survival analysis techniques.<br>
  - <tt>Survival Analisys.xlsx/</tt>: The data file used for the analysis..<br>
  - <tt>README.md</tt>: This file, providing an overview and instructions for the project.<br></p>

### Getting Started

<p align="left">
  - <strong>Requirements:</strong> Ensure you have Python installed along with the necessary packages:<br>

  ```
pip install numpy pandas matplotlib lifelines
```
  - <strong>Running the Analysis:</strong> To reproduce the analysis, run the scripts in the order specified in the project structure section.</p>
  

### Model Estimation

<p align="left">In this analysis, we fit three key regression models to the panel data: the fixed effects model, which controls for entity-specific characteristics by allowing each entity to have its own intercept; the random effects model, which assumes that entity-specific effects are uncorrelated with the regressors for potentially more efficient estimation; and the pooled OLS model, which treats the panel data as a single combined sample. To determine the most appropriate model, we compare these models using statistical tests and criteria, including the Hausman test to assess the validity of random effects versus fixed effects, and other diagnostic tests to evaluate model fit and efficiency.</p>

### Conclusion

<p align="left">The analysis provides insights into the survival probabilities over time and the impact of covariates on the hazard function. The Kaplan-Meier estimator visualizes the survival function, while the Cox model identifies significant predictors. The AFT model offers an alternative parametric approach to analyzing survival data.</p>

### Future Work

<p align="left">Future work could include exploring additional covariates, testing other parametric models like Gamma or Generalized Gamma, applying machine learning techniques for survival prediction, analyzing the Cox model assumptions more deeply, incorporating time-dependent covariates, and extending the analysis to include competing risks and multi-state models.</p>  
