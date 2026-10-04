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
# # Week 1 — Getting started with Python
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**. The setup cell below fetches the data over the internet,
# so nothing else changes.
#
# ## What you will be able to do by the end
#
# - Run code in a notebook, and write notes around it
# - Use Python for arithmetic, and avoid the one operator that catches everybody
# - Store values in variables and understand why names are case sensitive
# - Tell Python's four basic types apart, and explain why `"7"` is not `7`
# - Compare values, and read an error message without panicking
#
# ## The contextual dimension in play this week
#
# None yet — this week is about the tools. But keep the lecture's question in mind, because it
# returns every week: **what claim about culture would this measurement support?**
#
# Work through this in the workshop. Ask when you get stuck; that is what the session is for.

# %% [markdown]
# ## Setting up
#
# Run this cell first, every week. It is identical in every worksheet.
#
# It finds the module's `data` folder no matter which folder your notebook was opened from,
# and falls back to downloading the file if you are working in Colab. You do not need to
# understand it yet — but do read the comments, because *where your files are* is the single
# most common thing to go wrong all term.

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


# Check it works before doing anything else.
print("pandas version:", pd.__version__)
print("looking for data in:", data_path("fruitData.csv"))

# %% [markdown]
# ## 1. Notebooks
#
# A notebook is made of **cells**. Text cells (like this one) hold prose. Code cells hold Python.
#
# Run a cell by clicking it and pressing **Shift+Enter**.

# %%
# A worked example — run this.
print("This is a code cell")

# %% [markdown]
# **Task 1.1.** Add a new text cell below this one. Give it a heading using `#`, then write a
# sentence about what you hope to get out of this module.
#
# In Positron: click below this cell, press **B** for a new cell, then **M** to make it a text
# cell. In Colab: use the **+ Text** button.
#
# *There is no code to write for this task — but do actually do it, because you will write your
# whole final report in cells like these.*

# %% [markdown]
# ## 2. Python as a calculator
#
# Python understands `+`, `-`, `*` (multiply) and `/` (divide).

# %%
# A worked example.
2 + 5

# %% [markdown]
# **Task 2.1.** Work out `4 * 8` in the cell below.

# %%
# write your code here


# %% [markdown]
# **Task 2.2.** Before you run it, predict what `3 + 2 * 5` gives. Then run it.
#
# Was your prediction right? What rule is Python following?

# %%
# write your code here


# %% [markdown]
# ### Powers: the one that catches everybody
#
# To raise a number to a power, Python uses `**`.
#
# In R and in Excel, `^` means "to the power of". **In Python it does not.** It means something
# else entirely, and — this is the dangerous part — it does not give you an error. It quietly
# gives you a wrong number.

# %%
# A worked example: 5 to the power of 3.
5 ** 3

# %% [markdown]
# **Task 2.3.** Run `5 ^ 3` below and look at the answer. It is not 125.
#
# Add a comment above your code saying what you should have written instead.

# %%
# write your code here


# %% [markdown]
# ## 3. Variables
#
# A variable is a named box holding a value. You put something in it with `=`.
#
# `=` does **not** mean "these two things are equal". It means "put the value on the right into
# the box named on the left".

# %%
# A worked example.
a = 3
b = 6
x = a * b
x

# %% [markdown]
# **Task 3.1.** Assign the value `7` to a variable called `my_number`. Then multiply it by 3 and
# store the answer in a new variable called `result`. Print `result`.

# %%
# write your code here


# %% [markdown]
# **Task 3.2.** Run the cell below. Why are the two answers different?

# %%
city = "London"
City = "Paris"
print(city)
print(City)

# %% [markdown]
# *Write your answer in a text cell below this one.*

# %% [markdown]
# ### When a variable does not exist
#
# `del` removes a variable.

# %%
# A worked example.
temporary = 99
del temporary

# %% [markdown]
# **Task 3.3.** Try to print `temporary` in the cell below. You will get an error — that is the
# point of the task.
#
# Read the error message. What is the last line of it called, and what do you think it is
# telling you? Write your answer in a text cell underneath.

# %%
# write your code here


# %% [markdown]
# ## 4. Types
#
# Every value in Python has a **type**. `type()` tells you which.
#
# | Type | What it is | Example |
# |---|---|---|
# | `int` | a whole number | `7` |
# | `float` | a number with a decimal point | `7.5` |
# | `str` | text, always in quotes | `"London"` |
# | `bool` | true or false | `True` |

# %%
# A worked example.
print(type(7))
print(type("London"))

# %% [markdown]
# **Task 4.1.** Use `type()` to check the type of `7.5` and of `True`.

# %%
# write your code here


# %% [markdown]
# **Task 4.2.** What is the difference between `2` and `"2"`? Check whether they are equal using
# `==`, then write a sentence explaining the result in a text cell.

# %%
# write your code here


# %% [markdown]
# **Task 4.3.** Assign `True` to a variable called `is_sunny`. Then check whether `is_sunny` is
# equal to `"true"`. Explain the result — there are **two** reasons it is `False`.

# %%
# write your code here


# %% [markdown]
# ## 5. Comparing things
#
# `==` asks "are these equal?". Note the two equals signs — one would mean assignment.
#
# Also available: `!=` (not equal), `>`, `<`, `>=`, `<=`.

# %%
# A worked example.
print(3 == 4)
print(3 != 4)

# %% [markdown]
# **Task 5.1.** Create a variable `x` with value 5 and a variable `y` with value 5. Check whether
# they are equal.

# %%
# write your code here


# %% [markdown]
# **Task 5.2.** Create a variable `city` with the value `"London"`. Check whether it is equal to
# `"Paris"`.

# %%
# write your code here


# %% [markdown]
# **Task 5.3.** Check whether `"London"` is equal to `"london"`. Why is the answer what it is?

# %%
# write your code here


# %% [markdown]
# ## 6. Your first look at real data
#
# You are not expected to understand this code yet. Run it and read the output.

# %%
# A worked example — run it.
museum = pd.read_csv(data_path("museum_data.csv"))
museum.head()

# %% [markdown]
# **Task 6.1.** Run the cell below to count how many objects come from each region.

# %%
museum["region"].value_counts()

# %% [markdown]
# **Task 6.2.** This is the important task of the week, and it needs no code.
#
# That table counts museum objects by region. In a text cell below, answer:
#
# 1. What claim about culture *would* this table support?
# 2. What claim would it **not** support, even though someone might try?
#
# Keep your answer — we return to exactly this question in Week 5.

# %% [markdown]
# ## Stretch tasks
#
# Only if you have finished everything above.

# %% [markdown]
# **Stretch 1.** What does `4 ** 2 - 3` give? Work it out on paper first, then check.

# %%
# write your code here


# %% [markdown]
# **Stretch 2.** Python can compare text alphabetically. Predict, then test:
#
# - Is `"a"` greater than `"z"`?
# - Is `"z"` greater than `"a"`?
# - Is `"A"` greater than `"a"`?
#
# The third one surprises most people. Can you find out why?

# %%
# write your code here


# %% [markdown]
# **Stretch 3.** `/` divides. Try `7 / 2`, then try `7 // 2` and `7 % 2`.
#
# What do the last two do? These come back in Week 9.

# %%
# write your code here


# %% [markdown]
# ## Before next week
#
# The **practice quiz** on KEATS does not count towards your mark. Sit it anyway — it exists so
# the software is familiar before the real ones start.
#
# The quiz in the Week 2 lecture covers **this week's** material. Work back through anything above that you
# could not do without help.
#
# End of worksheet.
