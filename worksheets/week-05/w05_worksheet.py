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
# # Week 5 — Categories, tables and grouping
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**. The setup cell below fetches the data over the internet,
# so nothing else changes.
#
# ## What you will be able to do by the end
#
# - Convert a text column to a category, and give it an order
# - Count values, sort them, and find the most common
# - Cross-tabulate two variables, and add totals
# - Choose between counts, row percentages and column percentages — and say why
# - Summarise a numeric column by group with `groupby`
# - Notice when a group is too small to draw a conclusion from
#
# ## The contextual dimension in play this week
#
# This is chapter §5.4 — **designing the analysis around an interaction**. A crosstab *is* an
# interaction between two dimensions. This week you will find one where the counts and the
# percentages support opposite conclusions, and you will have to decide which claim the data
# actually licenses.
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
papers = pd.read_csv(data_path("BritishAndIrishNewspapersTitleList_20191118.csv"),
                     low_memory=False)
print("museum:", museum.shape, "| newspapers:", papers.shape)

# %% [markdown]
# ## 1. Categories

# %%
# A worked example.
colours = pd.Series(["red", "blue", "red", "green", "blue"]).astype("category")
print(colours.cat.categories)

# %% [markdown]
# **Task 1.1.** Convert the museum `region` column to a category, storing it in a new variable
# `region_cat`. Print its categories and how many there are.

# %%
# write your code here


# %% [markdown]
# **Task 1.2.** `cultural_significance` has three values: `Domestic`, `Ceremonial`, `Sacred`.
#
# Those are **nominal** — there is no natural order. In a text cell, explain why treating them as
# ordinal would be a mistake.

# %% [markdown]
# ### Giving categories an order

# %%
# A worked example.
scale = pd.CategoricalDtype(["Low", "Medium", "High"], ordered=True)
satisfaction = pd.Series(["Low", "High", "Medium", "Low"]).astype(scale)
print(satisfaction.min(), "<", satisfaction.max())

# %% [markdown]
# **Task 1.3.** Build an ordered category for the museum `value_category` below, so that
# `low < medium < high`. Then print the minimum and maximum.

# %%
# Given: three bands cut from the valuation column.
museum["value_category"] = pd.cut(
    museum["valuation"],
    bins=[0, 15000, 40000, 100000],
    labels=["low", "medium", "high"],
)
print(museum["value_category"].value_counts())

# %%
# write your code here


# %% [markdown]
# **Task 1.4.** Run the cell below. Why does the sort put "High" first, when we would say Low comes
# first? Answer in a text cell.

# %%
plain = pd.Series(["Low", "High", "Medium"])
print(sorted(plain))

# %% [markdown]
# ### The number trap

# %%
# A worked example. Look carefully at what .cat.codes gives you.
nums = pd.Series(["10", "20", "30"]).astype("category")
print("codes:", list(nums.cat.codes))

# %% [markdown]
# **Task 1.5.** Convert `nums` to actual numbers — 10, 20, 30. You will need two conversions.
#
# In a text cell, say what `.cat.codes` gave you instead, and when this trap would bite you in real
# work.

# %%
# write your code here


# %% [markdown]
# ## 2. One-way tables

# %%
# A worked example.
museum["region"].value_counts()

# %% [markdown]
# **Task 2.1.** Produce a frequency table of `object_type`. Which is most common?

# %%
# write your code here


# %% [markdown]
# **Task 2.2.** Now the same table as **percentages**, rounded to one decimal place.

# %%
# write your code here


# %% [markdown]
# **Task 2.3.** Print the frequency table of `acquisition_method` twice: once normally, and once
# including missing values.
#
# How many objects does the first table quietly leave out?

# %%
# write your code here


# %% [markdown]
# **Task 2.4.** Print the single most common `acquisition_method`, and the number of distinct
# regions, using one method each.

# %%
# write your code here


# %% [markdown]
# ## 3. Cross-tabulation

# %%
# A worked example.
pd.crosstab(museum["region"], museum["acquisition_method"])

# %% [markdown]
# **Task 3.1.** Produce the same crosstab with row and column totals.

# %%
# write your code here


# %% [markdown]
# **Task 3.2.** Now as row percentages. Which region has the highest share of colonial-collection
# objects?

# %%
# write your code here


# %% [markdown]
# ## 4. When counts and percentages disagree
#
# This is the important section. The newspapers dataset records whether each title has been
# digitised.

# %%
# Given: a True/False column, and the five main countries only.
papers["digitised"] = papers["online_status"].notna()
main = papers[papers["country_of_publication"].isin(
    ["England", "Scotland", "Wales", "Ireland", "Northern Ireland"])]
print(len(main), "titles from the five main countries")

# %% [markdown]
# **Task 4.1.** Cross-tabulate `country_of_publication` against `digitised` as **counts**.
#
# In a text cell, write down what you would conclude from this table alone.

# %%
# write your code here


# %% [markdown]
# **Task 4.2.** Now do it as **row percentages**.
#
# Which country has the highest proportion of its titles digitised? Which the lowest? Is that what
# you expected from Task 4.1?

# %%
# write your code here


# %% [markdown]
# **Task 4.3.** In a text cell, explain why the two tables point in different directions, and which
# one answers the question "has digitisation been even across these countries?"

# %% [markdown]
# **Task 4.4.** Now do it as **column** percentages, and answer a different question: of all the
# digitised titles, what share comes from each country?
#
# In a text cell, state the two different questions the row and column versions answer.

# %%
# write your code here


# %% [markdown]
# ## 5. Grouping a number by a category

# %%
# A worked example.
museum.groupby("region")["valuation"].mean().round(0)

# %% [markdown]
# **Task 5.1.** Produce a table of `count`, `mean` and `median` valuation by `region`.
#
# In a text cell: is there much difference between regions? What does that tell you?

# %%
# write your code here


# %% [markdown]
# **Task 5.2.** Do the same for `first_date_held` by `country_of_publication` in `main`. Include
# `count`.
#
# Which country's holdings begin earliest, on average?

# %%
# write your code here


# %% [markdown]
# **Task 5.3.** The interesting one. Group `main` by **both** `country_of_publication` and
# `digitised`, and print the `count` and `median` of `first_date_held`.

# %%
# write your code here


# %% [markdown]
# **Task 5.4.** Look at your answer to 5.3. Compare the median date for digitised and undigitised
# titles **within** each country.
#
# In a text cell:
#
# - Are digitised titles older or newer than undigitised ones?
# - Does the pattern hold in every country, or only some?
# - Suggest one reason why it might be so.

# %% [markdown]
# ## 6. Categories that are not as tidy as they look

# %%
# Given: the full country column, not just the five main ones.
print(papers["country_of_publication"].value_counts(dropna=False).head(10))

# %% [markdown]
# **Task 6.1.** Some values contain a `|`, like `England|Wales`. Print all the distinct values that
# contain one, and how many titles they cover in total.
#
# Hint: `papers["country_of_publication"].str.contains("|", regex=False)` — and mind the missing
# values.

# %%
# write your code here


# %% [markdown]
# **Task 6.2.** In a text cell: is `England|Wales` one category or two? What would you do about it,
# and what would you lose either way?

# %% [markdown]
# **Task 6.3.** Filter `main` to England only, convert `country_of_publication` to a category, and
# print its categories.
#
# Then remove the unused ones. Why might you sometimes want to keep them?

# %%
# write your code here


# %% [markdown]
# ## 7. Bonus workshop: your dataset

# %% [markdown]
# **Task 7.1.** Using your own project dataset, produce **one** crosstab or `groupby` that is
# relevant to your research question.
#
# Then, in a text cell:
#
# - State the interaction it shows, in the chapter's terms — which two dimensions?
# - Say whether you used counts or percentages, and why
# - Name one thing the table does **not** show
#
# This is the analysis section of the data overview, due in Week 8.

# %%
# write your code here


# %% [markdown]
# **Task 7.2.** Turn the same result into percentages or add a `count`, whichever makes the result
# more honest.
#
# In a text cell, say whether the second version changes the claim you would make.

# %%
# write your code here

# %% [markdown]
# ## Stretch tasks

# %% [markdown]
# **Stretch 1.** A `value_counts()` result is a Series, so `.reset_index()` makes it a data frame.
# Turn the region counts into a two-column table called `region_counts` with sensible column names,
# then save it as a CSV without an index column.

# %%
# write your code here


# %% [markdown]
# **Stretch 2.** `pd.crosstab` can take a `values=` and `aggfunc=` argument, which makes it do what
# `groupby` does. Produce a table of **median** `first_date_held` with countries as rows and
# `digitised` as columns, using `crosstab` rather than `groupby`.

# %%
# write your code here


# %% [markdown]
# **Stretch 3.** In the museum data, is `cultural_significance` recorded evenly across
# `object_type`? Produce the crosstab of `object_type` against whether it is missing, as row
# percentages, and say what you find.
#
# Careful: check the group sizes before you believe any percentage.

# %%
# write your code here


# %% [markdown]
# ## Before next week
#
# **Restart and Run All** before you close this notebook.
#
# Next week is **reading week** — no lecture, no workshop, no quiz. Use it on your dataset.
#
# The quiz in **Week 7** covers this week's material.
#
# End of worksheet.
