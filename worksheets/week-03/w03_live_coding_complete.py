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
# # Week 3 — live coding (completed)
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# The filled-in version of what we typed in the lecture, released afterwards so you can check what
# you missed.

# %% [markdown]
# ## Setup

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


print("we are running in:", Path.cwd())

# %% [markdown]
# ## 1. Creating a data frame

# %%
shows = pd.DataFrame({
    "title": ["Fleabag", "Arcane", "Chernobyl", "Bluey"],
    "year": [2016, 2021, 2019, 2018],
    "rating": [8.7, 9.0, 9.3, 9.4],
    "streaming_platform": ["iPlayer", "Netflix", "NOW", "iPlayer"],
    "watched_again": [True, True, False, True],
})
shows

# %% [markdown]
# A dictionary of columns: key is the column name, value is the list of entries.

# %%
shows.info()

# %%
shows.describe()

# %% [markdown]
# Note `describe()` only summarised the numeric columns — `year` and `rating`. R's `summary()`
# described everything. For that here, use `shows.describe(include="all")`.

# %%
shows["years_old"] = 2026 - shows["year"]
shows

# %%
shows[shows["rating"] > 9]

# %% [markdown]
# ## 2. Exploring the museum data

# %%
museum = pd.read_csv(data_path("museum_data.csv"))
print("shape:", museum.shape)
print("columns:", list(museum.columns))
museum.head()

# %% [markdown]
# ### The overview table
#
# A summary is itself a data frame. Build it the same way as any other — a dictionary of columns —
# except the values come from methods on the original table.

# %%
overview = pd.DataFrame({
    "type": museum.dtypes.astype(str),
    "present": museum.notna().sum(),
    "missing": museum.isna().sum(),
    "missing_%": (museum.isna().mean() * 100).round(1),
    "distinct": museum.nunique(),
})
overview

# %% [markdown]
# Read that carefully, because it is the whole point of the exercise:
#
# - `original_owner` is present for **16 of 150** objects — 89.3% missing — and has only **two**
#   distinct values.
# - `cultural_significance` is missing for exactly half.
# - `acquisition_method` is missing for 43.
#
# We come back to what that means at the end.

# %%
# What are those two values in original_owner?
print(museum["original_owner"].value_counts(dropna=False))

# %% [markdown]
# So the column does not record *who* previously owned an object. It records whether the previous
# owner was **identifiable at all** — and for 134 objects, not even that was written down.

# %% [markdown]
# ### The most valuable object

# %%
museum.loc[museum["valuation"].idxmax()]

# %% [markdown]
# ### The oldest acquisition

# %%
museum.loc[museum["acquisition_date"].idxmin()]

# %% [markdown]
# ### Objects from one region

# %%
west_africa = museum[museum["region"] == "West Africa"]
print(west_africa.shape[0], "objects from West Africa")
west_africa.head(3)

# %% [markdown]
# ### Making a category

# %%
# Three bands, using the quartiles we saw in describe().
museum["value_category"] = pd.cut(
    museum["valuation"],
    bins=[0, 15000, 40000, 100000],
    labels=["low", "medium", "high"],
)
print(museum["value_category"].value_counts())

# %% [markdown]
# `pd.cut` turns a number into a band. We use it properly in Week 5; for now just note that a
# category is something you *construct*, not something the data hands you. Where you put the
# boundaries changes what the analysis says.

# %% [markdown]
# ## 3. `.loc` and `.iloc` — where it matters

# %%
# On the full table they agree, because the labels happen to be 0, 1, 2...
print("loc :", museum.loc[0, "object_type"])
print("iloc:", museum.iloc[0, 1])

# %%
# Now filter, and look at what happened to the labels.
se_asia = museum[museum["region"] == "Southeast Asia"]
print("first five labels:", list(se_asia.index[:5]))
print("iloc[0] object_type:", se_asia.iloc[0]["object_type"])

# %% [markdown]
# The labels came with the rows — they were **not** renumbered. So:
#
# - `.iloc[0]` is "the first row of this table", which is what we usually mean.
# - `.loc[0]` is "the row labelled 0", which may not be in this table at all — or worse, may be
#   present but somewhere in the middle, giving a wrong answer with no error.

# %%
# If you want the labels renumbered after filtering:
se_asia_clean = se_asia.reset_index(drop=True)
print("after reset_index:", list(se_asia_clean.index[:5]))

# %% [markdown]
# ## 4. Files

# %%
print("current folder:", Path.cwd())
print("is there a data folder above us?", (Path.cwd().parent.parent / "data").exists())

# %%
fruit = pd.read_csv(data_path("fruitData.csv"))
fruit

# %%
print(fruit["Color"].value_counts())
print()
print(fruit["Shape"].value_counts())

# %%
# Add a column, take a subset, save it.
fruit["is_round"] = fruit["Shape"] == "round"
round_fruit = fruit[fruit["is_round"]]
round_fruit.to_csv("round_fruit.csv", index=False)
print(round_fruit)

# %%
# Read it back and check the columns are what we expect.
check = pd.read_csv("round_fruit.csv")
print(list(check.columns))

# %% [markdown]
# No `Unnamed: 0`, because we passed `index=False`. Compare with a file that was saved *without*
# that argument:

# %%
bananas = pd.read_csv(data_path("bananas_apples.csv"))
print(list(bananas.columns))

# %% [markdown]
# `Unnamed: 0` is a row-number column that got written into the file — in this case from R, without
# `row.names = FALSE`. Always pass `index=False` when you save.

# %% [markdown]
# ## 5. Debugging with AI
#
# Two errors on purpose. Read each one before fixing it.

# %%
# Wrong capitalisation. Uncomment to see the KeyError.
# museum["Region"]

# %% [markdown]
# `KeyError: 'Region'` — there is no such column. Names are case sensitive; it is `region`.
#
# If you paste this into <https://ai.create.kcl.ac.uk/chat>, include what you were trying to do, the
# code, and the full error. Ask it to **explain** the error rather than rewrite your code — you will
# need to recognise it again next week, in a closed quiz.

# %%
# `and` instead of `&`. Uncomment to see the ValueError.
# museum[(museum["region"] == "West Africa") and (museum["valuation"] > 20000)]

# %%
# The version that works.
museum[(museum["region"] == "West Africa") & (museum["valuation"] > 20000)].shape

# %% [markdown]
# ## What the overview table was telling us
#
# Every region in this collection is in the Global South. `acquisition_method` reads
# `Colonial Collection` for 29 objects, with 43 more unrecorded. The oldest acquisition, from 1880,
# is a West African object with no provenance and no cultural significance recorded.
#
# So the missing 89% in `original_owner` is not a data-quality problem to be cleaned up. It is a
# record of how this collection was assembled, and of what the people assembling it did not think
# worth writing down.
#
# **That** is what "the dataset and its boundaries" means, and it is the second section of your data
# overview.
#
# End of live coding.
