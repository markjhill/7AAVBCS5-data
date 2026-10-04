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
# # Week 4 — Missing data
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**. The setup cell below fetches the data over the internet,
# so nothing else changes.
#
# ## What you will be able to do by the end
#
# - Find and count missing values, and say what proportion of a column they are
# - Explain why pandas hides gaps rather than complaining about them
# - Choose between deleting, filling and keeping — and justify the choice
# - Test whether missingness is *patterned*, and name the pattern
# - Add and remove columns and rows, and join one table to another
#
# ## The contextual dimension in play this week
#
# This is chapter §5.2 at its sharpest. A gap in a dataset is not an absence of information — it is
# information about the people who made the dataset. This week you will find a case where the
# missingness is the most interesting thing in the file.
#
# Work through this in the workshop. Ask when you get stuck; that is what the session is for.

# %% [markdown]
# ## Setting up

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


museum = pd.read_csv(data_path("museum_data.csv"))
print("museum:", museum.shape)

# %% [markdown]
# ## 1. Finding the gaps

# %%
# A worked example.
ages = pd.Series([23, 45, np.nan, 31])
print(ages.isna())
print("missing:", ages.isna().sum())

# %% [markdown]
# **Task 1.1.** Run the cell below. Why is the answer `False`, and what should you use instead?
# Answer in a text cell.

# %%
print(np.nan == np.nan)

# %% [markdown]
# **Task 1.2.** For the `museum` table, print how many values are missing in **each** column.
#
# Hint: `.isna()` gives a table of True/False. What does `.sum()` do to that?

# %%
# write your code here


# %% [markdown]
# **Task 1.3.** Now build a proper summary **table** with two columns, `missing` and `missing_%`,
# one row per column of `museum`.
#
# This is the same trick as last week: a summary is itself a data frame.

# %%
# write your code here


# %% [markdown]
# **Task 1.4.** Which column is missing the most? Which is nearly complete? Answer in a text cell.

# %% [markdown]
# ## 2. Why pandas is more dangerous than R here

# %%
# A worked example. Compare these two.
ages = pd.Series([23, 45, np.nan, 31])
print("pandas .sum():", ages.sum())
print("numpy  .sum():", np.array([23, 45, np.nan, 31]).sum())

# %% [markdown]
# **Task 2.1.** pandas skipped the missing value and gave you a number. In R, `sum()` would have
# returned `NA` and forced you to notice.
#
# In a text cell: why is pandas' behaviour more dangerous, even though it is more convenient?

# %% [markdown]
# **Task 2.2.** Print the mean valuation of the museum objects, **and** the number of objects that
# figure is actually based on.
#
# Any statistic you report should come with its denominator.

# %%
# write your code here


# %% [markdown]
# ## 3. Strategy 1: deletion

# %%
# A worked example.
print("rows to start with:", len(museum))
print("rows with no gaps at all:", len(museum.dropna()))

# %% [markdown]
# **Task 3.1.** That result should have surprised you. In a text cell, explain what `dropna()` did
# and why it left you with what it did.

# %% [markdown]
# **Task 3.2.** Now delete deliberately. Make a table called `valued` that drops only the rows with
# no `valuation`, and print how many rows it has.
#
# Hint: `dropna()` takes a `subset=` argument.

# %%
# write your code here


# %% [markdown]
# **Task 3.3.** In a text cell, say when `valued` would be a reasonable table to work with, and
# when it would not.

# %% [markdown]
# ## 4. Strategy 2: filling in

# %%
# A worked example. Note the .copy() -- never modify the original.
filled = museum.copy()
filled["valuation"] = filled["valuation"].fillna(filled["valuation"].median())
print("missing before:", museum["valuation"].isna().sum())
print("missing after: ", filled["valuation"].isna().sum())

# %% [markdown]
# **Task 4.1.** Fill the missing `acquisition_method` values with the most common value in that
# column, on a **copy** of the table. Print the value counts before and after.
#
# Hint: `.mode()` gives the most common value, but returns a small table — you want `.mode()[0]`.

# %%
# write your code here


# %% [markdown]
# **Task 4.2.** You have just invented 43 acquisition methods that nobody recorded.
#
# In a text cell, argue **against** what you just did. What claim would it now be wrong to make
# from this table?

# %% [markdown]
# ## 5. Is the missingness patterned?
#
# This is the part that matters.

# %%
# A worked example: counts.
pd.crosstab(museum["acquisition_method"], museum["cultural_significance"].isna())

# %% [markdown]
# **Task 5.1.** Those are raw counts, and the three groups are different sizes, so they are hard to
# compare. Run it again as **row percentages**.
#
# Hint: `pd.crosstab(..., normalize="index")`, then multiply by 100 and `.round(1)`.

# %%
# write your code here


# %% [markdown]
# **Task 5.2.** In a text cell, state what the percentages show that the counts did not.

# %% [markdown]
# **Task 5.3.** Do the same for `original_owner` — is it missing evenly across acquisition methods?

# %%
# write your code here


# %% [markdown]
# **Task 5.4.** Using the MCAR / MAR / MNAR vocabulary from the lecture, classify the missingness
# in `cultural_significance`. Defend your answer in a text cell in three or four sentences.

# %% [markdown]
# ## 6. A second dataset
#
# A survey taken in April 2020, during the first UK lockdown. Two questions asked people to
# forecast when restrictions would end.

# %%
# Given: load it and look at the gaps.
ncv = pd.read_csv(data_path("ncv-data-2020-Apr-1.csv"))
print(ncv.shape)
print(ncv.isna().sum().to_string())

# %% [markdown]
# **Task 6.1.** About a third of people did not answer `Chance.by.end.year`. Test whether that
# relates to **age**: print the mean age of those who answered and those who did not.
#
# Hint: `ncv.groupby(ncv["Chance.by.end.year"].isna())["Age"].mean()`

# %%
# write your code here


# %% [markdown]
# **Task 6.2.** Now test whether it relates to `Comply.lockdown` — how much people said they were
# following the rules. Use row percentages.

# %%
# write your code here


# %% [markdown]
# **Task 6.3.** In a text cell: one of those two variables predicts the missingness and one does
# not. Which, and what might explain it?

# %% [markdown]
# **Task 6.4.** Look at the `Gender` breakdown of the same missingness. One category behaves
# completely differently from the others. Which, and why is it interesting?

# %%
# write your code here


# %% [markdown]
# ### A trap worth meeting once

# %%
# Six people answered "Don't know" to Comply.lockdown. This finds none of them.
print(len(ncv[ncv["Comply.lockdown"] == "Don't know"]))

# %% [markdown]
# **Task 6.5.** Print the exact values in `Comply.lockdown` using `.unique()`, and work out why the
# filter above found nothing.
#
# Hint: look very closely at the apostrophe.

# %%
# write your code here


# %% [markdown]
# ## 7. Changing a data frame

# %%
# A worked example: a "missing indicator" column.
work = museum.copy()
work["owner_recorded"] = work["original_owner"].notna()
print(work["owner_recorded"].value_counts())

# %% [markdown]
# **Task 7.1.** On `work`, add a column `significance_recorded` that is `True` where
# `cultural_significance` is present. Then use it to print the percentage of objects whose
# significance was recorded.

# %%
# write your code here


# %% [markdown]
# **Task 7.2.** Remove the `significance_recorded` column again using `.drop()`.

# %%
# write your code here


# %% [markdown]
# **Task 7.3.** Join the region lookup table below onto `museum`, so every object gains a
# `continent` column. Then check the row count has not changed.

# %%
# Given: a small lookup table.
region_notes = pd.DataFrame({
    "region": ["West Africa", "Southeast Asia", "South America",
               "Pacific Islands", "North Africa"],
    "continent": ["Africa", "Asia", "South America", "Oceania", "Africa"],
})
region_notes

# %%
# write your code here


# %% [markdown]
# ## 8. For your data overview
#
# No code.

# %% [markdown]
# **Task 8.1.** Take the dataset you are considering for your project. If you do not have one yet,
# use the newspapers list from last week.
#
# In a text cell, write the paragraph you would put in your data overview about missing data:
#
# - Which columns have gaps, and how big are they (as percentages)?
# - Is any of that missingness patterned? What did you check?
# - What will you do about it, and what will you therefore **not** claim?
#
# This is section 2 of the data overview, due Week 8.

# %% [markdown]
# ## Stretch tasks

# %% [markdown]
# **Stretch 1.** `museum.dropna(axis=1, thresh=75)` drops columns rather than rows. Run it. How
# many columns survive, and which one disappears? What does `thresh` mean here?

# %%
# write your code here


# %% [markdown]
# **Stretch 2.** Load `DawtryEtAl2015.csv`. It has 37 columns. Print only the columns that have any
# missing values at all, with their counts.
#
# Hint: build the summary, then filter it — a summary is a data frame, so you can filter it like one.

# %%
# write your code here


# %% [markdown]
# **Stretch 3.** In the `ncv` data, `Chance.by.end.month` and `Chance.by.end.year` are both mostly
# missing. Are they missing for the **same people**? Cross-tabulate the two missingness patterns
# against each other and say what you find.

# %%
# write your code here


# %% [markdown]
# ## Before next week
#
# **Restart and Run All** before you close this notebook.
#
# The quiz in next week's lecture covers **this week's** material.
#
# End of worksheet.
