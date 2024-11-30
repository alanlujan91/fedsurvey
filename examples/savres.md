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
    display_name: scf-tools
    language: python
    name: python3
---

```python
import pandas as pd
from statsmodels.stats.weightstats import DescrStatsW
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
```

```python
scf_data = pd.read_stata("../src/fedsurvey/scf/data/scf_processed.dta")

scf_data["retired"] = scf_data["age"] >= 71
```

```python
scf_data["age"].unique()
```

```python
def weighted_mean(data, var, weights):
    stats = DescrStatsW(data[var], weights=data[weights])
    return stats.mean


def to_percent(y, position):
    return f"{100 * y:.2f}%"


formatter = FuncFormatter(to_percent)
```

```python
scf_data.groupby(["year", "edcl_lbl"]).apply(
    weighted_mean, "savres1", "wgt"
).unstack().plot()
plt.title("Reason for saving: can't save")
plt.gca().yaxis.set_major_formatter(formatter)
```

```python
scf_data.groupby(["year", "edcl_lbl"]).apply(
    weighted_mean, "savres2", "wgt"
).unstack().plot()
plt.title("Reason for saving: education")
plt.gca().yaxis.set_major_formatter(formatter)
```

```python
scf_data.groupby(["year", "edcl_lbl"]).apply(
    weighted_mean, "savres3", "wgt"
).unstack().plot()
plt.title("Reason for saving: family")
plt.gca().yaxis.set_major_formatter(formatter)
```

```python
scf_data.groupby(["year", "edcl_lbl"]).apply(
    weighted_mean, "savres4", "wgt"
).unstack().plot()
plt.title("Reason for saving: home")
plt.gca().yaxis.set_major_formatter(formatter)
```

```python
scf_data.groupby(["year", "edcl_lbl"]).apply(
    weighted_mean, "savres5", "wgt"
).unstack().plot()
plt.title("Reason for saving: purchases")
plt.gca().yaxis.set_major_formatter(formatter)
```

```python
scf_data.groupby(["year", "edcl_lbl"]).apply(
    weighted_mean, "savres6", "wgt"
).unstack().plot()
plt.title("Reason for saving: retirement")
plt.gca().yaxis.set_major_formatter(formatter)
```

```python
scf_data.groupby(["year", "edcl_lbl"]).apply(
    weighted_mean, "savres7", "wgt"
).unstack().plot()
plt.title("Reason for saving: liquidity/the future")
plt.gca().yaxis.set_major_formatter(formatter)
```

```python
scf_data.groupby(["year", "edcl_lbl"]).apply(
    weighted_mean, "savres8", "wgt"
).unstack().plot()
plt.title("Reason for saving: investment")
plt.gca().yaxis.set_major_formatter(formatter)
```

```python
scf_data.groupby(["year", "edcl_lbl"]).apply(
    weighted_mean, "savres9", "wgt"
).unstack().plot()
plt.title("Reason for saving: no particular reason")
plt.gca().yaxis.set_major_formatter(formatter)
```

```python
scf_data.groupby(["edcl_lbl", "retired"]).apply(
    weighted_mean, "savres3", "wgt"
)  # family
```

```python
scf_data.groupby(["edcl_lbl"]).apply(weighted_mean, "savres6", "wgt")  # retirement
```

```python
scf_data.groupby(["edcl_lbl"]).apply(weighted_mean, "savres7", "wgt")  # the future
```

```python
scf_data.groupby(["edcl_lbl"]).apply(weighted_mean, "savres5", "wgt")  # purchases
```

```python
scf_data.groupby(["edcl_lbl"]).apply(weighted_mean, "savres1", "wgt")  # can't save
```

```python
all_reasons = []

reasons = [
    "Can't save",
    "Education",
    "Family",
    "Home",
    "Purchases",
    "Retirement",
    "Liquidity/the future",
    "Investment",
    "No particular reason",
]

for i in range(1, 10):
    temp = (
        scf_data.groupby(
            [
                "edcl_lbl",
            ]
        )
        .apply(weighted_mean, f"savres{i}", "wgt")
        .reset_index()
    )
    temp["Reasons for Saving"] = reasons[i - 1]
    all_reasons.append(temp)

all_reasons = pd.concat(all_reasons)
pivot = all_reasons.pivot_table(
    index=[
        "edcl_lbl",
    ],
    columns="Reasons for Saving",
    values=0,
)
```

```python
# New code to format as percentages
pivot = pivot.applymap(lambda x: f"{x:.2%}")

pivot
```

```python
pivot.to_html("table1.tex")
```

```python
scf_data = scf_data[scf_data["retired"] == True]
```

```python
all_reasons = []

reasons = [
    "Can't save",
    "Education",
    "Family",
    "Home",
    "Purchases",
    "Retirement",
    "Liquidity/the future",
    "Investment",
    "No particular reason",
]

for i in range(1, 10):
    temp = (
        scf_data.groupby(
            [
                "edcl_lbl",
            ]
        )
        .apply(weighted_mean, f"savres{i}", "wgt")
        .reset_index()
    )
    temp["Reasons for Saving"] = reasons[i - 1]
    all_reasons.append(temp)

all_reasons = pd.concat(all_reasons)
pivot = all_reasons.pivot_table(
    index=[
        "edcl_lbl",
    ],
    columns="Reasons for Saving",
    values=0,
)
```

```python
# New code to format as percentages
pivot = pivot.applymap(lambda x: f"{x:.2%}")

pivot
```

```python
pivot.to_html("table2.tex")
```
