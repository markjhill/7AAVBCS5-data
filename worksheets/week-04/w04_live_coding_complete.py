# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Week 4 — live coding (completed)
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# The filled-in version of what we typed in the lecture.

# %% [markdown]
# ## Setup

# %%
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

# The module's data lives in a separate public repository so that this notebook
# works both on your own machine and on Colab.
DATA_REPO = "https://github.com/markjhill/7AAVBCS5-data.git"


def data_path(name: str) -> Path:
    """Return a usable path to a file or folder in the module's data folder.

    A notebook's "current folder" is wherever it was opened from, which differs
    between Positron and Colab and is the usual cause of FileNotFoundError. So
    rather than assuming, we search upwards for a `data` folder. If there isn't
    one -- which means we are on Colab -- the public data repository is
    downloaded once and used instead.

    Works for single files ("museum_data.csv") and for folders ("SUA").
    """
    here = Path.cwd()
    for candidate in (here, *here.parents):
        for local in (candidate / "data" / name, candidate / name):
            if local.exists():
                return local

    downloaded = Path("7AAVBCS5-data")
    if not downloaded.is_dir():
        print("No local data folder found -- downloading the module data (once)...")
        subprocess.run(
            ["git", "clone", "--depth", "1", DATA_REPO, str(downloaded)],
            check=True,
        )
    for target in (downloaded / "data" / name, downloaded / name):
        if target.exists():
            return target
    raise FileNotFoundError(f"{name!r} is not in the module data.")


# %% [markdown]
# ## Exercise 1: quantify the gaps

# %%
museum = pd.read_csv(data_path("museum_data.csv"))

missing_summary = pd.DataFrame({
    "missing": museum.isna().sum(),
    "missing_%": (museum.isna().mean() * 100).round(2),
})
missing_summary

# %% [markdown]
# Worst: `original_owner`, 134 of 150 — **89.33%**. Then `cultural_significance` at exactly half,
# and `acquisition_method` at 28.67%.
#
# Nearly complete: `valuation`, missing only 4.

# %%
print("rows to start with     :", len(museum))
print("rows with no gaps at all:", len(museum.dropna()))

# %% [markdown]
# **Zero.** Every one of the 150 objects is missing something, so the "simplest" strategy destroys
# the entire dataset.
#
# R's `na.omit()` does the same thing. This is why you check what deletion removes before using it.

# %%
print("drop only rows with no valuation:", len(museum.dropna(subset=["valuation"])))

# %%
# Drop columns instead, keeping only those at least 50% complete.
reduced = museum.dropna(axis=1, thresh=int(0.5 * len(museum)))
print(reduced.shape[1], "columns survive:", list(reduced.columns))

# %% [markdown]
# `original_owner` goes. `cultural_significance` has exactly 75 non-missing values and so just
# survives a 75-value threshold — which shows how arbitrary any threshold is.

# %% [markdown]
# ## Exercise 2: is the missingness patterned?

# %%
pd.crosstab(museum["acquisition_method"], museum["cultural_significance"].isna())

# %% [markdown]
# Counts alone look almost even — 24 missing for Colonial Collection against 21 for Purchase. You
# would conclude there was nothing here.

# %%
(pd.crosstab(museum["acquisition_method"],
             museum["cultural_significance"].isna(),
             normalize="index") * 100).round(1)

# %% [markdown]
# As proportions of each group it reverses:
#
# - **Colonial Collection: 82.8% missing**
# - Donation: 45.5%
# - **Purchase: 37.5%**
#
# The counts were similar only because there are roughly twice as many purchases. `normalize="index"`
# is R's `prop.table(..., 1)`.

# %%
(pd.crosstab(museum["acquisition_method"],
             museum["original_owner"].isna(),
             normalize="index") * 100).round(1)

# %% [markdown]
# `original_owner` is uniformly terrible — 82.8%, 95.5%, 87.5%. Not patterned, so it supports a
# weaker claim: this museum did not systematically record provenance for anything.
#
# **`cultural_significance` is MNAR.** Not merely related to an observed variable, but related to
# what the missing value *would have been*: the meaning went unrecorded because of how the object was
# acquired.

# %% [markdown]
# ### What imputation would do here

# %%
filled = museum.copy()
print("before:", filled["acquisition_method"].value_counts(dropna=False).to_dict())

filled["acquisition_method"] = filled["acquisition_method"].fillna(
    filled["acquisition_method"].mode()[0]
)
print("after :", filled["acquisition_method"].value_counts(dropna=False).to_dict())

# %% [markdown]
# Purchase goes from 56 to 99. We have just asserted that every unrecorded object was bought — the
# least alarming possibility, and the one least likely to be true, since objects without paperwork
# are *less* likely to be ordinary purchases.
#
# Imputation can be fine for a numeric column feeding a model. It is almost never fine for a
# categorical column that *is* the thing you are studying.

# %% [markdown]
# ## Exercise 3: a survey, not a museum

# %%
ncv = pd.read_csv(data_path("ncv-data-2020-Apr-1.csv"))
print(ncv.shape)
print(ncv.isna().sum().to_string())

# %% [markdown]
# Two forecast questions, each missing for about a third of the 1,000 respondents.

# %%
# Does age predict it?
print(ncv.groupby(ncv["Chance.by.end.year"].isna())["Age"].mean().round(1))

# %% [markdown]
# 45.8 against 46.3. No.

# %%
# Does self-reported compliance?
(pd.crosstab(ncv["Comply.lockdown"],
             ncv["Chance.by.end.year"].isna(),
             normalize="index") * 100).round(1)

# %% [markdown]
# Yes. "Completely" 31.7% missing; "About half of the time" 61.3%; "Hardly any of the time" 62.5%.
# Roughly double.
#
# So the people who answered the forecast question are not a random subset — the average forecast
# describes compliers more than it describes the sample. Since the missingness relates to a variable
# we **can** see, this is **MAR**.

# %%
# The Gender breakdown -- and the trap.
print(pd.crosstab(ncv["Gender"], ncv["Chance.by.end.year"].isna()))
print()
print((pd.crosstab(ncv["Gender"], ncv["Chance.by.end.year"].isna(),
                   normalize="index") * 100).round(1))

# %% [markdown]
# `Prefer not to answer` shows **100% missing** — which looks like a dramatic finding until you read
# the counts. **It is one person.** One out of one is 100%.
#
# A percentage without its denominator is worthless, and small groups produce extreme percentages by
# arithmetic rather than by pattern. Always print counts alongside.
#
# The real finding is the boring one: gender does **not** predict the missingness (34.6%, 34.7%,
# 33.3%).

# %% [markdown]
# ## Exercise 4: changing a data frame

# %%
work = museum.copy()
work["owner_recorded"] = work["original_owner"].notna()
print(work["owner_recorded"].value_counts())

# %% [markdown]
# This is the "missing indicator" variable — it turns a gap into something you can analyse.

# %%
region_notes = pd.DataFrame({
    "region": ["West Africa", "Southeast Asia", "South America",
               "Pacific Islands", "North Africa"],
    "continent": ["Africa", "Asia", "South America", "Oceania", "Africa"],
})
merged = museum.merge(region_notes, on="region", how="left")
print("rows before:", len(museum), "| after:", len(merged))
print(merged["continent"].value_counts().to_string())

# %% [markdown]
# Always check the row count after a join. If it went **up**, the lookup table had duplicate keys. If
# a value came out missing, a name did not match — usually spelling or spacing.

# %% [markdown]
# ## What this week was actually about
#
# Every region in this collection is in the Global South. Cultural significance is unrecorded for
# 82.8% of colonial-collection objects against 37.5% of purchases. Provenance is unrecorded almost
# everywhere.
#
# None of that is a data-quality problem to be tidied. It is a record of what the people assembling
# this collection did not ask, could not ask, or did not think worth writing down — and it is
# available to you as evidence, provided you study the missingness instead of filling it in.
#
# That is section 2 of your data overview: what entered the dataset, what did not, and why.
#
# End of live coding.
