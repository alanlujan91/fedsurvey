---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: "1.3"
      jupytext_version: 1.16.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
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

```python
filtered_df.columns
```

```python
glm = smf.glm(
    "hequity ~ hhsex_lbl + age + edcl_lbl + married_lbl + lf_lbl + racecl4_lbl + year"
    "+ finmill  + incomemill",
    data=filtered_df,
    freq_weights=filtered_df["wgt"],
    family=sm.families.Binomial(),
)

res = glm.fit()

print(res.summary2())
```

```python
glm = smf.glm(
    "hequity ~ hhsex_lbl + age + edcl_lbl + married_lbl + lf_lbl + racecl4_lbl + year"
    "+ finincome",
    data=filtered_df,
    family=sm.families.Binomial(),
    freq_weights=filtered_df["wgt"],
)
res = glm.fit()
print(res.summary2())
```

```python
conditional_df = filtered_df[filtered_df["hequity"] > 0]
```

```python
glm = smf.glm(
    "equityfin ~ hhsex_lbl + age + edcl_lbl + married_lbl + lf_lbl + racecl4_lbl + year"
    "+ finmill  + incomemill",
    data=conditional_df,
    family=sm.families.Binomial(),
    freq_weights=conditional_df["wgt"],
)
res = glm.fit()
print(res.summary2())
```

```python
glm = smf.glm(
    "equityfin ~ hhsex_lbl + age + edcl_lbl + married_lbl + lf_lbl + racecl4_lbl + year"
    "+ finincome",
    data=conditional_df,
    family=sm.families.Binomial(),
    freq_weights=conditional_df["wgt"],
)
res = glm.fit()
print(res.summary2())
```
