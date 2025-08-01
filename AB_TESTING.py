#####################################################
# A/B Test: Comparison of Bidding Methods on Conversion
#####################################################

# Business Problem:
# Facebook recently introduced a new bidding method called "average bidding"
# as an alternative to the existing "maximum bidding" method.
# One of our clients, bombabomba.com, wants to test whether average bidding
# results in more purchases compared to maximum bidding.
# The company has conducted an A/B test for one month.
# The primary success metric is Purchase.
# The goal is to evaluate the results of this A/B test using statistical methods.

#####################################################
# Dataset Description:
#####################################################

# The dataset includes website user behavior such as ad impressions,
# clicks, purchases, and earnings. It has two separate groups:
# Control Group: Maximum Bidding
# Test Group: Average Bidding

# Columns:
# - Impression: Number of ad views
# - Click: Number of ad clicks
# - Purchase: Number of purchases after clicking
# - Earning: Revenue from purchases

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, levene, ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Load datasets
df_control = pd.read_excel("/Users/betulcoklu/PycharmProjects/pythonProject/datasets/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("/Users/betulcoklu/PycharmProjects/pythonProject/datasets/ab_testing.xlsx", sheet_name="Test Group")

df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control, df_test], axis=0, ignore_index=True)

# Quick data check
def check_df(dataframe, head=5):
    print("########## Shape ##########")
    print(dataframe.shape)
    print("########## Types ##########")
    print(dataframe.dtypes)
    print("########## Head ##########")
    print(dataframe.head(head))
    print("########## Tail ##########")
    print(dataframe.tail(head))
    print("########## NA ##########")
    print(dataframe.isnull().sum())
    print("########## Quantiles ##########")
    print(dataframe.select_dtypes(include=["float64", "int64"]).quantile([0, 0.05, 0.5, 0.95, 0.99, 1]).T)

check_df(df)

#####################################################
# Hypothesis Definition
#####################################################

# H0: The average Purchase value for the control group is equal to the test group.
# H1: The average Purchase value for the control group is different from the test group.

# Purchase averages by group
print(df.groupby("group")["Purchase"].mean())

#####################################################
# Assumption Checks
#####################################################

# 1. Normality Assumption (Shapiro-Wilk Test)
stat, p = shapiro(df[df["group"] == "control"]["Purchase"])
print(f"Shapiro Control: Stat={stat:.4f}, p-value={p:.4f}")

stat, p = shapiro(df[df["group"] == "test"]["Purchase"])
print(f"Shapiro Test: Stat={stat:.4f}, p-value={p:.4f}")

# Interpretation: p > 0.05 → Fail to reject H0 → Normal distribution assumption holds

# 2. Homogeneity of Variance (Levene Test)
stat, p = levene(df[df["group"] == "control"]["Purchase"],
                 df[df["group"] == "test"]["Purchase"])
print(f"Levene: Stat={stat:.4f}, p-value={p:.4f}")

# Interpretation: p > 0.05 → Fail to reject H0 → Variance homogeneity assumption holds

#####################################################
# Hypothesis Testing
#####################################################

# Since both assumptions are met, we perform a two-sample independent t-test.
stat, p = ttest_ind(df[df["group"] == "control"]["Purchase"],
                    df[df["group"] == "test"]["Purchase"],
                    equal_var=True)
print(f"T-Test: Stat={stat:.4f}, p-value={p:.4f}")

# Interpretation:
# p > 0.05 → Fail to reject H0 → No statistically significant difference between groups.

#####################################################
# Conclusion
#####################################################

# We used an independent two-sample t-test to compare the purchase averages of the two groups.
# Both normality and variance homogeneity assumptions were satisfied.
# The resulting p-value showed no statistically significant difference in purchase averages.
# Therefore, we recommend that bombabomba.com continues using the current method (Maximum Bidding),
# or consider testing further with more data before switching to Average Bidding.



# Visualization: Average Purchase by Group

group_means = df.groupby("group")["Purchase"].mean().reset_index()

sns.barplot(x="group", y="Purchase", data=group_means)
plt.title("Average Purchase by Group")
plt.xlabel("Group")
plt.ylabel("Average Purchase")
plt.tight_layout()
plt.savefig("plots/average_purchase.png")
plt.show()