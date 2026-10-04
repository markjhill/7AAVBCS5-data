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
# # Week 5 — live coding (completed)
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# The filled-in version of what we typed in the lecture.

# %%
import subprocess
from pathlib import Path

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


papers = pd.read_csv(data_path("BritishAndIrishNewspapersTitleList_20191118.csv"),
                     low_memory=False)
print(papers.shape)

# %% [markdown]
# ## Exercise 1: categorical data

# %%
# Which columns are text rather than numbers?
print(papers.dtypes.value_counts())
print()
print([c for c in papers.columns if papers[c].dtype == "object" or str(papers[c].dtype) == "str"][:8])

# %%
country = papers["country_of_publication"].astype("category")
print(len(country.cat.categories), "categories")
print(country.value_counts(dropna=False).head(8).to_string())

# %% [markdown]
# Two things to notice immediately.
#
# First, `place_of_publication` is missing for the great majority of titles:

# %%
print("place missing for", papers["place_of_publication"].isna().sum(),
      "of", len(papers), "titles",
      f"({papers['place_of_publication'].isna().mean() * 100:.1f}%)")

# %% [markdown]
# Second, some country values are **compounds** — `England|Wales` and 25 others:

# %%
compound = papers["country_of_publication"].dropna()
compound = compound[compound.str.contains("|", regex=False)]
print(compound.nunique(), "compound values covering", len(compound), "titles")
print(compound.value_counts().head(5).to_string())

# %% [markdown]
# Is `England|Wales` one category or two? There is no right answer, only a documented one. We will
# exclude them and say so.

# %%
main = papers[papers["country_of_publication"].isin(
    ["England", "Scotland", "Wales", "Ireland", "Northern Ireland"])].copy()
print(len(main), "titles in the five main countries")

# %% [markdown]
# ## Exercise 2: tables and cross-tabulation

# %%
print(main["country_of_publication"].value_counts())

# %% [markdown]
# `value_counts()` already sorts, most common first — R needed
# `sort(table(x), decreasing = TRUE)`.

# %%
print("the mode:", main["country_of_publication"].value_counts().idxmax())
print("distinct countries:", main["country_of_publication"].nunique())

# %%
print((main["country_of_publication"].value_counts(normalize=True) * 100).round(1))

# %% [markdown]
# ### Two-way: is digitisation even?

# %%
main["digitised"] = main["online_status"].notna()
pd.crosstab(main["country_of_publication"], main["digitised"], margins=True)

# %% [markdown]
# Read the counts and ask what they show. The obvious answer is "England dominates" — 1,625 digitised
# titles against Wales's 57.
#
# That is almost content-free, because England has twenty times as many titles to begin with. The
# table is mostly measuring the size of England.

# %%
(pd.crosstab(main["country_of_publication"], main["digitised"],
             normalize="index") * 100).round(1)

# %% [markdown]
# As a share of each country's **own** holdings, the order reverses:
#
# | | % digitised |
# |---|---|
# | **Ireland** | **14.4** |
# | Northern Ireland | 11.6 |
# | Scotland | 10.4 |
# | England | 7.9 |
# | **Wales** | **5.6** |
#
# Ireland is the most digitised; Wales the least; England fourth of five. The overall rate is 8.4%.
#
# Both tables are true. The counts measure **volume**, the percentages measure **rate**, and only the
# second answers "has digitisation been even?"

# %%
# The other margin answers a different question again.
(pd.crosstab(main["country_of_publication"], main["digitised"],
             normalize="columns") * 100).round(1)

# %% [markdown]
# - "What share of **Welsh titles** are digitised?" → 5.6%
# - "What share of **digitised titles** are Welsh?" → 2.8%
#
# Confusing those two is the commonest way a crosstab gets misread.

# %%
# Tables are data frames.
counts = main["country_of_publication"].value_counts().reset_index()
counts.columns = ["country", "titles"]
counts

# %% [markdown]
# ## Exercise 3: grouping

# %%
main.groupby("country_of_publication")["first_date_held"].agg(["count", "median"])

# %% [markdown]
# Ireland's holdings begin earliest — median 1874 against England's 1935.
#
# Always keep `count`. A median over a handful of titles is not a finding.

# %%
main.groupby(["country_of_publication", "digitised"])["first_date_held"].agg(["count", "median"])

# %% [markdown]
# ### The finding
#
# **Digitised titles are older, in every single country:**
#
# | Country | digitised | not digitised | gap |
# |---|---|---|---|
# | England | 1852 | 1935 | 83 years |
# | Ireland | 1848 | 1874 | 26 |
# | Northern Ireland | 1853 | 1935 | 82 |
# | Scotland | 1865.5 | 1899 | 33.5 |
# | Wales | 1869 | 1918 | 49 |
#
# No exceptions, which makes it far more convincing than any single-country result.
#
# Hypotheses, not conclusions: copyright expiry, established scholarly demand for the
# nineteenth-century press, preservation arguments for fragile paper, and the historical scoping of
# the BNA and BURNEY collections.
#
# The methodological point is the one that matters. **Study "British newspapers" using only digitised
# material and you are studying a sample that is systematically older than the population.** That
# selection effect is built into the infrastructure, not into your code — and no amount of careful
# analysis downstream will remove it.
#
# This is chapter §5.4: the interaction between the spatial, temporal and institutional dimensions is
# the finding, not a footnote to it.

# %% [markdown]
# ## What to take away
#
# | Dimensions | Tool |
# |---|---|
# | one category | `value_counts()` |
# | two categories | `pd.crosstab()` |
# | category and a number | `groupby().agg()` |
#
# And: **always ask whether you want counts or percentages, and which margin.** The answer follows
# from your question, not from preference.
#
# End of live coding.
