---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.4
  kernelspec:
    display_name: hetretrwg
    language: python
    name: python3
---

# Racial Wealth Gap


```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from utilities import wmedian_lineplot, wmean_lineplot, weighted_relplot


sns.set_theme(context="paper")
sns.set_palette("gray")
```

```python
df = pd.read_stata("../data/scf_processed.dta")
df.head()
```

```python
filtered_df = df[
    (df["racecl4_lbl"] != "Other or Multiple race")
    & df["age"].between(21, 80)
    & (df["networth"] > 0)
    & (df["asset"] > 0)
    & (df["fin"] > 0)
    & (df["income"])
    & (df["equityfin"]).between(0, 1)
]
```

# The Racial Financial Wealth Gap



## Weighted Average Household Financial Assets by Race and Year


```python
# | label: racial-wealth-gap

lineplot = wmedian_lineplot(
    data=filtered_df,
    x="year",
    y="fin",
    weights="wgt",
    style="racecl4_lbl",
    # errorbar=True,
)

lineplot.set_title("Average Household Financial Assets by Race and Year")
lineplot.set_ylabel("Financial Assets (in $1,000s)")
lineplot.set_xlabel("Year")
lineplot.legend(title="Race")
```

```python
lineplot = wmean_lineplot(
    data=filtered_df,
    x="year",
    y="fin",
    weights="wgt",
    style="racecl4_lbl",
    # errorbar=True,
)

lineplot.set_title("Average Household Financial Assets by Race and Year")
lineplot.set_ylabel("Financial Assets (in $1,000s)")
lineplot.set_xlabel("Year")
lineplot.legend(title="Race")
```

## Weighted Average Household Financial Assets by Education, Race, and Year


```python
lineplot = weighted_relplot(
    data=filtered_df,
    x="year",
    y="fin",
    col="edcl_lbl",
    weights="wgt",
    style="racecl4_lbl",
)
```

## Weighted Average Household Normalized Financial Assets by Race and Year


```python
plt.title("Average Household Normalized Financial Assets by Race and Year")
plt.ylabel("Financial Assets (in $1,000s)")
plt.xlabel("Year")

lineplot = wmean_lineplot(
    data=filtered_df,
    x="year",
    y="finincome",
    weights="wgt",
    style="racecl4_lbl",
)

plt.legend(title="Race")
```

## Weighted Average Household Normalized Financial Assets by Education, Race, and Year


```python
lineplot = weighted_relplot(
    data=filtered_df,
    x="year",
    y="finincome",
    col="edcl_lbl",
    weights="wgt",
    style="racecl4_lbl",
)
```

# Life Cycle Racial Financial Wealth Gap



## Weighted Average Household Financial Assets by Race and Age Group


```python
lineplot = wmean_lineplot(
    data=filtered_df,
    x="age_lbl",
    y="fin",
    weights="wgt",
    style="racecl4_lbl",
)
```

## Weighted Average Household Financial Assets by Education, Race, and Age Group


```python
lineplot = weighted_relplot(
    data=filtered_df,
    x="age_lbl",
    y="fin",
    col="edcl_lbl",
    weights="wgt",
    style="racecl4_lbl",
)
```

## Weighted Average Household Normalized Financial Assets by Race and Age Group


```python
lineplot = wmean_lineplot(
    data=filtered_df,
    x="age_lbl",
    y="finincome",
    weights="wgt",
    style="racecl4_lbl",
)
```

## Weighted Average Household Normalized Financial Assets by Education, Race, and Age Group


```python
lineplot = weighted_relplot(
    data=filtered_df,
    x="age_lbl",
    y="finincome",
    col="edcl_lbl",
    weights="wgt",
    style="racecl4_lbl",
)
```

# Life Cycle Racial Participation Gap



## Weighted Household Participation by Race and Age Group


```python
lineplot = wmean_lineplot(
    data=filtered_df,
    x="age_lbl",
    y="hequity",
    weights="wgt",
    style="racecl4_lbl",
)
```

## Weighted Household Participation by Education, Race, and Age Group


```python
lineplot = weighted_relplot(
    data=filtered_df,
    x="age_lbl",
    y="hequity",
    col="edcl_lbl",
    weights="wgt",
    style="racecl4_lbl",
)
```

```python
lineplot = wmean_lineplot(
    data=filtered_df,
    x="findeciles",
    y="hequity",
    weights="wgt",
    style="racecl4_lbl",
)

plt.legend(title="Race")
```

```python
lineplot = weighted_relplot(
    data=filtered_df,
    x="findeciles",
    y="hequity",
    col="edcl_lbl",
    weights="wgt",
    style="racecl4_lbl",
)
```

```python
# | label: racial-wealth-gap
plt.title("Average Household Financial Assets by Race and Year")
plt.ylabel("Financial Assets (in $1,000s)")
plt.xlabel("Year")

lineplot = wmean_lineplot(
    data=filtered_df,
    x="findeciles",
    y="equity",
    weights="wgt",
    style="racecl4_lbl",
)

plt.legend(title="Race")
```

```python
conditional_df = filtered_df[filtered_df["hequity"] == 1]
```

```python
lineplot = wmean_lineplot(
    data=conditional_df,
    x="age_lbl",
    y="equityfin",
    weights="wgt",
    style="racecl4_lbl",
)
```

```python
lineplot = weighted_relplot(
    data=conditional_df,
    x="age_lbl",
    y="equityfin",
    col="edcl_lbl",
    weights="wgt",
    style="racecl4_lbl",
)
```

```python

```

```python

```
