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
# # Week 3 — Data frames and loading data
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**. The setup cell below fetches the data over the internet,
# so nothing else changes.
#
# ## What you will be able to do by the end
#
# - Build a data frame from scratch and inspect one you have loaded
# - Get a single column, several columns, and single values out of a table
# - Explain the difference between `.loc` and `.iloc`, and pick the right one
# - Filter rows by one condition and by several
# - Load a CSV from disk, and save one without an extra index column
# - Recognise the four errors this week will throw at you
#
# ## The contextual dimension in play this week
#
# This is chapter §5.2 — **the dataset and its boundaries**. Every time you load a file you are
# accepting someone's decisions about what counted as an observation and which attributes were
# worth keeping. `info()` is the fastest way to see what those decisions were.
#
# Work through this in the workshop. Ask when you get stuck; that is what the session is for.

# %% [markdown]
# ## Setting up
#
# Run this cell first, every week. It is identical in every worksheet.

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


print("pandas", pd.__version__)
print("this notebook thinks it is in:", Path.cwd())

# %% [markdown]
# ## 1. Building a data frame
#
# A data frame is made from a dictionary: each key is a column name, each value is the list of
# entries in that column.

# %%
# A worked example.
social_media = pd.DataFrame({
    "platform": ["Twitter", "Instagram", "TikTok", "Facebook"],
    "users": [450, 2000, 1000, 3000],
    "founded": [2006, 2010, 2016, 2004],
    "public_company": [False, False, False, True],
})
social_media

# %% [markdown]
# **Task 1.1.** Make a data frame called `shows` describing four television programmes, with
# columns `title`, `year`, `rating` (out of 10) and `animated` (True/False). Print it.
#
# Choose sensible types: `year` and `rating` should be numbers, not text.

# %%
# write your code here


# %% [markdown]
# **Task 1.2.** Print the shape of your data frame, and its column names.
#
# Careful: one of those needs brackets and one does not.

# %%
# write your code here


# %% [markdown]
# **Task 1.3.** Add a column called `years_old` giving each show's age in 2026.

# %%
# write your code here


# %% [markdown]
# ## 2. Inspecting data you did not make
#
# This is what you will actually spend your time doing.

# %%
# Given: load the museum collection data.
museum = pd.read_csv(data_path("museum_data.csv"))
museum.head()

# %% [markdown]
# **Task 2.1.** How many rows and columns does `museum` have? Print the shape.

# %%
# write your code here


# %% [markdown]
# **Task 2.2.** Run `museum.info()`. Look at the **Non-Null Count** column.
#
# Which column has the **fewest** values actually present? Answer in a text cell below — you will
# need this in Week 4.

# %%
# write your code here


# %% [markdown]
# **Task 2.3.** Run `museum.describe()`. Why does it show only one column, when the table has
# eight? Answer in a text cell.

# %%
# write your code here


# %% [markdown]
# ## 3. Getting columns out

# %%
# A worked example.
museum["region"].head()

# %% [markdown]
# **Task 3.1.** Print the first five entries of the `object_type` column.

# %%
# write your code here


# %% [markdown]
# **Task 3.2.** Print a table containing only the `object_type`, `region` and `valuation`
# columns — the first three rows will do.
#
# Hint: you will need two sets of brackets. Think about why.

# %%
# write your code here


# %% [markdown]
# **Task 3.3.** Run the two cells below and compare. What is the difference between one set of
# brackets and two? Answer in a text cell.

# %%
print(type(museum["region"]))

# %%
print(type(museum[["region"]]))

# %% [markdown]
# ## 4. `.loc` and `.iloc`
#
# `.loc` selects by **label**. `.iloc` selects by **position**. Right now the labels happen to be
# 0, 1, 2... so they look the same. They will not stay that way.

# %%
# A worked example.
print(museum.loc[0, "region"])
print(museum.iloc[0, 2])

# %% [markdown]
# **Task 4.1.** Using `.loc`, print the `object_type` of the row labelled `5`.

# %%
# write your code here


# %% [markdown]
# **Task 4.2.** Using `.iloc`, print the first three rows of the table.

# %%
# write your code here


# %% [markdown]
# **Task 4.3.** This is the important one. Run the cell below, which keeps only objects from one
# region and then asks for "the first row" both ways.
#
# Why do `.loc` and `.iloc` disagree now, when they agreed above? Answer in a text cell.

# %%
# Given: a filtered table.
se_asia = museum[museum["region"] == "Southeast Asia"]
print("first label in this table:", se_asia.index[0])
print(".iloc[0] gives the object_type:", se_asia.iloc[0]["object_type"])
# Now uncomment the next line. It may work, or it may raise a KeyError — either way, explain why.
# print(".loc[0] gives:", se_asia.loc[0]["object_type"])

# %% [markdown]
# ## 5. Filtering rows

# %%
# A worked example. Look at the mask on its own first.
mask = museum["valuation"] > 20000
print(mask.head())
print("how many are True:", mask.sum())

# %%
# And then use it.
expensive = museum[museum["valuation"] > 20000]
print(expensive.shape)

# %% [markdown]
# **Task 5.1.** Make a table called `cheap` containing only objects with a valuation below 15000.
# Print how many rows it has.

# %%
# write your code here


# %% [markdown]
# **Task 5.2.** Make a table of objects that are from `"West Africa"` **and** valued above 20000.
#
# Remember: `&` not `and`, and every condition needs its own brackets.

# %%
# write your code here


# %% [markdown]
# **Task 5.3.** Do the same thing again using `.query()`. Which do you find easier to read?

# %%
# write your code here


# %% [markdown]
# **Task 5.4.** Run the cell below. It uses `and` instead of `&`, so it will fail.
#
# Read the error. Then write the corrected version underneath.

# %%
# Uncomment to see the error, then fix it below.
# museum[(museum["region"] == "West Africa") and (museum["valuation"] > 20000)]

# %%
# write your code here


# %% [markdown]
# ## 6. Finding the extremes

# %%
# A worked example.
print(museum["valuation"].idxmax())
museum.loc[museum["valuation"].idxmax()]

# %% [markdown]
# **Task 6.1.** Find and print the whole row for the **least** valuable object.
#
# Hint: there is a method for this whose name is the opposite of `idxmax`.

# %%
# write your code here


# %% [markdown]
# ## 7. Reading and writing files

# %%
# A worked example: a much bigger file.
papers = pd.read_csv(data_path("BritishAndIrishNewspapersTitleList_20191118.csv"))
print(papers.shape)
papers[["publication_title", "place_of_publication", "first_date_held"]].head()

# %% [markdown]
# **Task 7.1.** Load `fruitData.csv` into a data frame called `fruit` and print the whole thing —
# it is small enough.

# %%
# write your code here


# %% [markdown]
# **Task 7.2.** Now load `bananas_apples.csv` into a data frame called `bananas` and print it.
#
# There is an extra column that should not be there. What is it called, and where do you think it
# came from? Answer in a text cell.

# %%
# write your code here


# %% [markdown]
# **Task 7.3.** Add a column to `fruit` called `is_round` which is `True` when the fruit's
# `Shape` is `"round"`.
#
# Then print how many of the five fruits are round.

# %%
# write your code here


# %% [markdown]
# **Task 7.4.** Save your modified `fruit` table as `fruit_with_flag.csv` **without** an index
# column. Then load it back in and check it has the columns you expect and no extras.

# %%
# write your code here


# %% [markdown]
# ## 8. Boundaries of a dataset
#
# No code. This is the thinking that the data overview will need.

# %% [markdown]
# **Task 8.1.** Look again at `papers` — the British and Irish Newspapers title list. Run
# `papers.info()` if it helps.
#
# In a text cell, answer:
#
# - What is **one row**? What is the unit of observation?
# - Name two columns that record the **spatial** dimension, and one that records the **temporal**.
# - The column `online_status` is present for only about 2,000 of the 24,927 titles. What does that
#   missingness tell you — is it a flaw in the data, or is it *itself* a finding?
#
# Keep this answer. We come back to this dataset in Week 5.

# %% [markdown]
# ## Stretch tasks
#
# Only if you have finished everything above.

# %% [markdown]
# **Stretch 1.** `museum["region"].value_counts()` counts how many objects come from each region.
# Try it. Which region has the most? Which has the fewest?

# %%
# write your code here


# %% [markdown]
# **Stretch 2.** `museum.sort_values("valuation", ascending=False)` sorts the table. Print the top
# five most valuable objects, showing only `object_type`, `region` and `valuation`.
#
# Then check: has the *index* changed order too? What does that mean for `.iloc[0]` versus
# `.loc[0]`?

# %%
# write your code here


# %% [markdown]
# **Stretch 3.** `papers["place_of_publication"]` contains place names. How many *different*
# places appear? How many titles have no place recorded at all?
#
# Hint: `.nunique()` and `.isna().sum()`

# %%
# write your code here


# %% [markdown]
# ## Before next week
#
# **Restart and Run All** before you close this notebook.
#
# Start looking for a dataset for your project. The data overview is due in **Week 8**, and Task
# 8.1 above is a rehearsal for it.
#
# The quiz in next week's lecture covers **this week's** material.
#
# End of worksheet.
