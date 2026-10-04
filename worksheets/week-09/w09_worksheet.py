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
# # Week 9 — Functions, conditionals and loops
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**.
#
# ## What you will be able to do by the end
#
# - Write a function that takes arguments and returns a value
# - Explain the difference between printing and returning
# - Write a `for` loop over a list, a range, and a folder of files
# - Collect results in a list rather than printing them
# - Write a `while` loop, and stop it running forever
# - Build a data frame one row at a time
#
# ## The contextual dimension in play this week
#
# The machinery for next week. A collection of documents is not a column, so pandas cannot vectorise
# over it — this is where loops finally earn their place.
#
# The corpus you will use is 228 US State of the Union addresses, 1790–1920. It is a **semiotic**
# collection with a **temporal** dimension attached to each item by its filename.

# %% [markdown]
# ## Setting up

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


SUA = data_path("SUA")
print(SUA, "exists:", SUA.is_dir())

# %% [markdown]
# ## 1. Writing functions

# %%
# A worked example.
def calculate_engagement(likes, retweets):
    return likes + retweets


print(calculate_engagement(100, 50))

# %% [markdown]
# **Task 1.1.** Write a function `calculate_percentage(part, total)` that returns what percentage
# `part` is of `total`. Test it with `(25, 100)`.

# %%
# write your code here


# %% [markdown]
# **Task 1.2.** Run the cell below. Why does it print `None`?

# %%
def add_bad(a, b):
    a + b


print(add_bad(2, 3))

# %% [markdown]
# **Task 1.3.** Write two functions: `get_tax(salary, rate)` which **returns** the tax, and
# `print_tax(salary, rate)` which **prints** it.
#
# Then show that you can use the result of the first in a further calculation but not the second.

# %%
# write your code here


# %% [markdown]
# **Task 1.4.** Write a function `word_count(text)` that returns how many words are in a piece of
# text. Give it a docstring.
#
# Hint: `text.split()` breaks text into a list of words.

# %%
# write your code here


# %% [markdown]
# ## 2. For loops

# %%
# A worked example.
cities = ["London", "Manchester", "Rome", "Lima"]
for city in cities:
    print(f"I want to go to {city}")

# %% [markdown]
# **Task 2.1.** Given the list below, write a loop that prints each follower count.

# %%
# Given.
followers = [1000, 2500, 500, 3200, 1500]

# %%
# write your code here


# %% [markdown]
# **Task 2.2.** Now do it again, but instead of printing, **collect** the values doubled into a new
# list called `doubled`. Print the list afterwards.

# %%
# write your code here


# %% [markdown]
# **Task 2.3.** Write a loop that goes through `years` below and collects only those after 1900 into
# a list called `modern`.

# %%
# Given.
years = [1800, 1900, 1950, 2000, 2020]

# %%
# write your code here


# %% [markdown]
# ## 3. While loops

# %% [markdown]
# **Task 3.1.** Write a while loop that starts at `countdown = 5`, prints each number, and stops at
# 0.

# %%
# write your code here


# %% [markdown]
# **Task 3.2.** In a text cell, say what happens if you forget to change `countdown` inside the
# loop, and how you would stop it in a notebook.

# %% [markdown]
# ## 4. Looping over files
#
# This is what the rest of the module needs.

# %%
# A worked example: list the first few files.
files = sorted(SUA.glob("*.txt"))
print(len(files), "files")
for path in files[:3]:
    print(path.name)

# %% [markdown]
# **Task 4.1.** Write a loop that prints the name and character count of the first five files.
#
# Hint: `path.read_text(encoding="utf-8", errors="replace")` gives you the text.

# %%
# write your code here


# %% [markdown]
# **Task 4.2.** Now do it for **all** the files, collecting the results into a list of dictionaries,
# then turn that into a data frame called `speeches` with columns `file` and `characters`.
#
# This is the pattern you will use every week from now on: empty list → append inside the loop →
# data frame afterwards.

# %%
# write your code here


# %% [markdown]
# **Task 4.3.** Print the shape of `speeches`, then the five longest speeches.

# %%
# write your code here


# %% [markdown]
# **Task 4.4.** One file has **zero** characters. Find it.
#
# In a text cell, say what this means for any analysis that loops over these files, and what you
# would do about it.

# %%
# write your code here


# %% [markdown]
# ## 5. Getting information out of filenames

# %%
# A worked example. The filenames are "President_Year.txt".
name = "Adams_1797.txt"
president, year = name.replace(".txt", "").split("_")
print(president, year)

# %% [markdown]
# **Task 5.1.** Extend your loop from 4.2 so the data frame also has `president` and `year` columns.
# Make sure `year` is a **number**, not text.

# %%
# write your code here


# %% [markdown]
# **Task 5.2.** Using the tools from Week 5, print the number of speeches per president, and the
# five presidents with the most.

# %%
# write your code here


# %% [markdown]
# **Task 5.3.** Using Week 7's tools, plot the length of each speech against its year.
#
# In a text cell, describe what you see. Have speeches got longer or shorter?

# %%
# write your code here


# %% [markdown]
# ## 6. Combining a function with a loop

# %% [markdown]
# **Task 6.1.** Use your `word_count` function from Task 1.4 inside your loop, so the data frame
# also has a `words` column.
#
# Then print the mean number of words per speech.

# %%
# write your code here


# %% [markdown]
# **Task 6.2.** In a text cell: why is it better to have `word_count` as a function than to write
# `len(text.split())` inside the loop?

# %% [markdown]
# ## 7. Bonus workshop: your dataset
#
# Optional. Use your own dataset if this week's tools fit it. If your project uses many text files,
# this is the moment to try the Week 9 pattern on them. If it uses one CSV, use a function on one
# column instead.

# %% [markdown]
# **Task 7.1.** Write one small function that would help your project.
#
# Examples: count words in a text field, classify a year into periods, flag a category as relevant,
# or extract information from a filename.

# %%
# write your code here


# %% [markdown]
# **Task 7.2.** Use your function on either:
#
# - every file in a folder, collecting a data frame of results, or
# - every value in one column, creating a new column.
#
# In a text cell, explain why a function or loop was useful here, and why you should **not** loop
# over a data frame when a pandas operation would do the same job.

# %%
# write your code here


# %% [markdown]
# ## Stretch tasks

# %% [markdown]
# **Stretch 1.** Write a function `longest_word(text)` that returns the longest word in a piece of
# text. Run it on `alice.txt`.
#
# Is the answer a real word? What does that tell you about splitting on whitespace?

# %%
# write your code here


# %% [markdown]
# **Stretch 2.** Python has a shorter way of writing a collect-loop, called a list comprehension:
#
# ```python
# modern = [y for y in years if y > 1900]
# ```
#
# Rewrite your Task 2.3 answer this way, and check it gives the same result.
#
# Then, in a text cell, say when you think the loop is clearer than the comprehension.

# %%
# write your code here


# %% [markdown]
# **Stretch 3.** Loops are slow on data frames. Time these two ways of flagging expensive museum
# objects, using `%%timeit` or `time.perf_counter()`:
#
# 1. A `for` loop over the rows
# 2. `museum["valuation"] > 20000`
#
# Which is faster, and by roughly how much?

# %%
# write your code here


# %% [markdown]
# ## Before next week
#
# **Restart and Run All** before you close this notebook.
#
# Next week is text analysis, and it is built entirely on the pattern in Task 4.2.
#
# The quiz in next week's lecture covers **this week's** material.
#
# End of worksheet.
