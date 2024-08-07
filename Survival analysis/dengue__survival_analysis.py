# -*- coding: utf-8 -*-
"""Dengue_ Survival_analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GKoGReIgJ5FFRD4Len5_VSD3CoNOeySf

### Load libraries
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd

!pip install lifelines

from lifelines import KaplanMeierFitter
from lifelines import CoxPHFitter
import matplotlib.pyplot as plt

"""### Data Source

Loprinzi CL. Laurie JA. Wieand HS. Krook JE. Novotny PJ. Kugler JW. Bartel J. Law M. Bateman M. Klatt NE. et al. Prospective evaluation of prognostic variables from patient-completed questionnaires. North Central Cancer Treatment Group. Journal of Clinical Oncology. 12(3):601-7, 1994.
"""

data = pd.read_excel("/content/drive/MyDrive/Bahan port/Survival Analysis/Survival Analisys.xlsx")
data.head()

data.shape

"""### Variable description
* inst: Institution code
* SURVIVAL TIME : The length of time a dengue fever patient recovers in days
* GENDER : Male = 0 Female = 1
* AGE: The patient's age in years
* THROMBOCYTES : The number of platelets in the blood
* HEMATOCRIT : The level of red blood cells in the blood
* HEMOGLOBIN : Protein content in red blood cells
* LEUKOCYTES : White blood cell levels in the blood

"""

data["GENDER"] = data["GENDER"] - 1
data.head()

data.dtypes

data.isnull().sum()

data.columns

T = data["SURVIVAL TIME"]
plt.hist(T, bins = 10)
plt.show()

"""## Fitting a non-parametric model [Kaplan Meier Curve]"""

kmf = KaplanMeierFitter()
kmf.fit(durations = T)
kmf.plot_survival_function()

kmf.survival_function_.plot()
plt.title('Survival function')

"""This graph shows that the majority of dengue fever patients recover in a relatively short time after observation begins. Most of the healing occurs in the first 5 days, with a slower but steady rate of healing until about 10 days. After that, almost all patients had recovered, and only a few took longer to recover."""

kmf.plot_cumulative_density()

"""This CDF graph shows that the majority of dengue fever patients recover within the first 5 days after observation begins. Healing continues for about 10 days, after which almost all patients have recovered. This indicates the effectiveness of a treatment or condition that causes most patients to recover in a relatively short time."""

kmf.median_survival_time_

"""Half of dengue fever patients are expected to recover within 3 days after diagnosis or start of treatment."""

from lifelines.utils import median_survival_times

median_ = kmf.median_survival_time_
median_confidence_interval_ = median_survival_times(kmf.confidence_interval_)
print(median_)
print(median_confidence_interval_)

"""With a 95% confidence level, we can say that the median time to recovery is 3 days. This provides an idea of ​​the uncertainty or variability in median time estimates."""

ax = plt.subplot(111)

m = (data["GENDER"] == 0)

kmf.fit(durations = T[m], label = "Male")
kmf.plot_survival_function(ax = ax)

kmf.fit(T[~m], label = "Female")
kmf.plot_survival_function(ax = ax, at_risk_counts = True)

plt.title("Survival of different gender group")

"""## Fitting Cox Proportional Hazard Model

The Cox proportional hazards model, by contrast, is not a fully parametric model. Rather it is a semi-parametric model because even if the regression parameters (the betas) are known, the distribution of the outcome remains unknown.

[Cox Proportional Hazard Model (lifelines webpage)](https://lifelines.readthedocs.io/en/latest/Survival%20Regression.html)

Cox proportional hazards regression model assumptions includes:

* Independence of survival times between distinct individuals in the sample,
* A multiplicative relationship between the predictors and the hazard, and
* A constant hazard ratio over time. This assumption implies that, the hazard curves for the groups should be proportional and cannot cross.

### Hazard and Hazard Ratio

* Hazard is defined as the slope of the survival curve — a measure of how rapidly subjects are dying.
* The hazard ratio compares two treatments. If the hazard ratio is 2.0, then the rate of deaths in one treatment group is twice the rate in the other group.
"""

data.head()

cph = CoxPHFitter()
cph.fit(data, duration_col = 'SURVIVAL TIME')

cph.print_summary()

"""### Interpretation

* Wt.loss has a coefficient of about -0.01.

* We can recall that in the Cox proportional hazard model, a higher hazard means more at risk of the event occurring.
The value $exp(-0.01)$ is called the hazard ratio.

* Here, a one unit increase in wt loss means the baseline hazard will increase by a factor
of $exp(-0.01)$ = 0.99 -> about a 1% decrease.

* Similarly, the values in the ecog column are: \[0 = asymptomatic, 1 = symptomatic but completely ambulatory, 2 = in bed $<$50\% of the day\]. The value of the coefficient associated with ecog2, $exp(1.20)$, is the value of ratio of hazards associated with being "in bed $<$50% of the day (coded as 2)" compared to asymptomatic (coded as 0, base category).
"""

plt.subplots(figsize=(10, 6))
cph.plot()

data["AGE"].describe()

cph.plot_partial_effects_on_outcome(covariates = 'AGE',
                                    values = [5, 10, 20, 30],
                                    cmap = 'coolwarm')

cph.check_assumptions(data, p_value_threshold = 0.05)

from lifelines.statistics import proportional_hazard_test

results = proportional_hazard_test(cph, data, time_transform='rank')
results.print_summary(decimals=3, model="untransformed variables")

"""## Parametric [Accelerated Failure Time Model (AFT)]

[AFT Lifelines package webpage](https://lifelines.readthedocs.io/en/latest/Survival%20Regression.html#accelerated-failure-time-models)
"""

from lifelines import WeibullFitter,\
                      ExponentialFitter,\
                      LogNormalFitter,\
                      LogLogisticFitter


# Instantiate each fitter
wb = WeibullFitter()
ex = ExponentialFitter()
log = LogNormalFitter()
loglogis = LogLogisticFitter()

# Fit to data
for model in [wb, ex, log, loglogis]:
  model.fit(durations = data["SURVIVAL TIME"])
  # Print AIC
  print("The AIC value for", model.__class__.__name__, "is",  model.AIC_)

"""### Fit the weibull fitter and print summary"""

from lifelines import WeibullAFTFitter
weibull_aft = WeibullAFTFitter()
weibull_aft.fit(data, duration_col='SURVIVAL TIME')

weibull_aft.print_summary(3)

"""## Interpretation of the coefficients

* A unit increase in $x_i$ means the average/median survival time changes by a factor of $exp(b_i)$.
* Suppose $b_i$ was positive, then the factor $exp(b_i)$ is greater than 1, which will decelerate the event time since we divide time by the factor ⇿ increase mean/median survival. Hence, it will be a protective effect.
* Likewise, a negative $b_i$ will hasten the event time ⇿ reduce the mean/median survival time.
* This interpretation is opposite of how the sign influences event times in the Cox model!

## Example

* GENDER, which contains [0: Male and 1: Female], has a positive coefficient.
* This means being a female subject compared to male changes mean/median survival time by exp(1.095) = 2,989,  that the risk (hazard) for women is around 2,981 times higher than for men.
"""

print(weibull_aft.median_survival_time_)
print(weibull_aft.mean_survival_time_)

plt.subplots(figsize=(10, 6))
weibull_aft.plot()

plt.subplots(figsize=(10, 6))
weibull_aft.plot_partial_effects_on_outcome('AGE', range(5, 25, 5), cmap='coolwarm')