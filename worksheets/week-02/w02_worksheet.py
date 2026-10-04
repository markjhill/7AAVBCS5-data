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
# # Week 2 — Lists, arrays, dictionaries, and making decisions
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**. The setup cell below fetches the data over the internet,
# so nothing else changes.
#
# ## What you will be able to do by the end
#
# - Store many values in one variable, and get them back out by position
# - Explain why positions start at 0, and why a slice excludes its end
# - Tell a list from an array, and say what `* 2` does to each
# - Calculate min, max, sum, mean, median and standard deviation
# - Look values up by name using a dictionary
# - Write an `if`/`elif`/`else` that makes a decision
#
# ## The contextual dimension in play this week
#
# All five. The lecture's table maps each of the chapter's five dimensions onto a Python type:
# semiotic → `str`, temporal → dates or years, spatial → `float` pairs, social → categories,
# relational → pairs of linked things. When you meet a new dataset, the types tell you which
# dimensions were recorded — and which were not.
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


print("pandas", pd.__version__, "| numpy", np.__version__)

# %% [markdown]
# ## 1. Lists
#
# A list holds many values in order. You make one with square brackets.

# %%
# A worked example.
ages = [18, 21, 30, 24, 22, 22]
ages

# %% [markdown]
# **Task 1.1.** Make a list called `cities` containing four cities you would like to visit.
# Print it.

# %%
# write your code here


# %% [markdown]
# **Task 1.2.** Use `len()` to print how many cities are in your list.

# %%
# write your code here


# %% [markdown]
# ## 2. Positions start at zero
#
# The first item is at position `0`, not `1`. This will catch you at least once.

# %%
# A worked example.
print(ages[0])   # first
print(ages[2])   # third
print(ages[-1])  # last

# %% [markdown]
# **Task 2.1.** Print the **second** city in your `cities` list. Think before you type: which
# number do you need?

# %%
# write your code here


# %% [markdown]
# **Task 2.2.** Print the **last** city in two different ways: once using a positive number, and
# once using `-1`.

# %%
# write your code here


# %% [markdown]
# **Task 2.3.** Run the cell below. You will get an `IndexError` — that is the point of the task.
#
# Why does asking for `ages[6]` fail when the list has six items? Answer in a text cell below.

# %%
# ages has six items. Uncomment the next line and run it.
# print(ages[6])

# %% [markdown]
# ### Slicing
#
# A colon takes a range of positions. **The start is included, the end is not.**

# %%
# A worked example.
print(ages[0:3])   # positions 0, 1, 2
print(ages[:2])    # from the beginning
print(ages[3:])    # to the end

# %% [markdown]
# **Task 2.4.** Print the first **three** cities in your list using a slice.

# %%
# write your code here


# %% [markdown]
# **Task 2.5.** Predict what `ages[1:4]` gives before running it. How many numbers, and which?
# Then check.

# %%
# write your code here


# %% [markdown]
# ### Changing a list

# %%
# A worked example.
fruit = ["apple", "banana"]
fruit.append("cherry")
fruit[0] = "apricot"
print(fruit)

# %% [markdown]
# **Task 2.6.** Add a fifth city to your `cities` list with `.append()`, then change the first
# city to somewhere else. Print the result.

# %%
# write your code here


# %% [markdown]
# ## 3. Lists do not do maths
#
# This is the trap of the week.

# %%
# A worked example. What do you expect? Run it and see.
[18, 21, 30] * 2

# %% [markdown]
# **Task 3.1.** In a text cell below, say what `* 2` actually did, and what you might have
# expected it to do if you had used R before.

# %% [markdown]
# ### Arrays do do maths
#
# A numpy array looks like a list but calculates on every element at once.

# %%
# A worked example.
temperatures_c = np.array([20, 25, 18, 30])
print(temperatures_c * 2)
print((temperatures_c * 9 / 5) + 32)

# %% [markdown]
# **Task 3.2.** Make an array called `ages_array` from your own list of six ages
# `[18, 21, 30, 24, 22, 22]`, then print every age doubled.

# %%
# write your code here


# %% [markdown]
# **Task 3.3.** Print which of those ages are greater than 22. You should get `True`s and
# `False`s, not numbers.

# %%
# write your code here


# %% [markdown]
# **Task 3.4.** Run the cell below. All four values go into the array — what type do they all
# end up as, and why?

# %%
np.array([1, 2, True, "word"])

# %% [markdown]
# ## 4. Describing data
#
# The point of an array: summarising many numbers at once.

# %%
# A worked example.
ages_array = np.array([18, 21, 30, 24, 22, 22])
print("mean  ", ages_array.mean())
print("median", np.median(ages_array))

# %% [markdown]
# **Task 4.1.** Print the minimum, maximum, sum and standard deviation of `ages_array`.
#
# Hint: three of those are methods like `.mean()`. Look at the lecture slide if you need the names.

# %%
# write your code here


# %% [markdown]
# **Task 4.2.** Now some real data. The cell below loads the museum dataset and pulls out the
# `valuation` column as an array. Print its mean and its maximum.

# %%
# Given: this loads the data and pulls out the column for you.
museum = pd.read_csv(data_path("museum_data.csv"))
valuations = museum["valuation"].dropna().to_numpy()
print("how many values:", len(valuations))

# %%
# write your code here


# %% [markdown]
# **Task 4.3.** `dropna()` in the cell above throws away objects with no valuation. There were
# 150 objects in the file — how many valuations did you get?
#
# In a text cell, answer: does the mean you just calculated describe *the collection*, or only
# *the part of the collection someone chose to value*? This is the Week 1 question again.

# %% [markdown]
# ## 5. Building text
#
# An f-string lets you drop values into a sentence.

# %%
# A worked example.
year = 1945
print(f"WW2 ended in {year} when the Allies won.")

# %% [markdown]
# **Task 5.1.** Using an f-string, print a sentence that says how many cities are in your
# `cities` list — with the number filled in automatically, not typed by hand.

# %%
# write your code here


# %% [markdown]
# ## 6. Dictionaries
#
# A list looks things up by position. A dictionary looks them up by name.

# %%
# A worked example.
student = {"name": "Sarah", "age": 21, "enrolled": True}
print(student["name"])

# %% [markdown]
# **Task 6.1.** Make a dictionary called `film` describing a film you like, with keys for
# `title`, `year`, `director` and `animated`. Choose sensible types — `year` should be a number,
# `animated` should be `True` or `False`.

# %%
# write your code here


# %% [markdown]
# **Task 6.2.** Print just the title of your film, then add a new key `runtime` with the length
# in minutes, then print all the keys.

# %%
# write your code here


# %% [markdown]
# ## 7. Making decisions
#
# `if` runs a block of code only when a condition is `True`.

# %%
# A worked example. Change the temperature and run it again.
temperature = 20

if temperature > 10:
    print("go for a run")
else:
    print("stay at home")

# %% [markdown]
# **Task 7.1.** Given a `salary`, print the tax due. If salary is £50,000 or more the rate is
# 30%; below that it is 20%.
#
# To find a percentage: `amount * rate / 100`.

# %%
# Given: your starting value.
salary = 60000

# %%
# write your code here


# When it works, change salary to 30000 above and run both cells again.

# %% [markdown]
# **Task 7.2.** Given a `year`, print which period it falls in. Use `if`, `elif`, `else`:
#
# - Early modern: 1400–1780
# - Late modern: 1781–today
# - Anything earlier: print "Before our period"

# %%
# Given: your starting value.
year = 1560

# %%
# write your code here


# %% [markdown]
# **Task 7.3.** Given a `mark`, print the classification: "First" for 70+, "2:1" for 60–69,
# "2:2" for 50–59, "Fail" below 50.
#
# Test it with 65, then with 80, then with 45.

# %%
# Given: your starting value.
mark = 65

# %%
# write your code here


# %% [markdown]
# **Task 7.4.** Use `and` to print something only when a `year` is between 1400 and 1780.

# %%
# Given: your starting value.
year = 1560

# %%
# write your code here


# %% [markdown]
# ## 8. Describing a dataset with the five dimensions
#
# No code for this one. Think back to the group activity.

# %% [markdown]
# **Task 8.1.** For the dataset your group looked at, write a short paragraph in a text cell
# answering:
#
# - Which of the five dimensions (semiotic, temporal, spatial, social, relational) does it
#   record?
# - Which does it **not** record?
# - Name one question you therefore cannot answer with it.
#
# Keep this. You will do exactly this for your own dataset in the assessment.

# %% [markdown]
# ## Stretch tasks
#
# Only if you have finished everything above.

# %% [markdown]
# **Stretch 1.** `ages_array.std()` gives the *population* standard deviation. R's `sd()` gives
# the *sample* one. Find the sample version by passing `ddof=1`, and print both. How different
# are they, and does the difference grow or shrink with more data?

# %%
# write your code here


# %% [markdown]
# **Stretch 2.** What does `sorted(ages)` give? What about `sorted(cities)`? What does it do to
# text starting with a capital letter?

# %%
# write your code here


# %% [markdown]
# **Stretch 3.** Make a numpy array of five publication years, then subtract the earliest year from
# the whole array. What does the result tell you?

# %%
# write your code here


# %% [markdown]
# ## Before next week
#
# **Restart and Run All** before you close this notebook. If it does not survive that, something
# in it depends on a cell you have since changed or deleted — better to find out now.
#
# The quiz in next week's lecture covers **this week's** material.
#
# End of worksheet.
