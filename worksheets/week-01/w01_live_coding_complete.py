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
# # Week 1 — live coding
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**. The setup cell below fetches the data over the internet,
# so nothing else changes.
#
# This is the notebook used in the lecture. The cells are **deliberately empty** — they get filled
# in as we go. Follow along and type it yourself; watching is not the same as doing.
#
# The completed version is released after the lecture.

# %% [markdown]
# ## 1. This is a notebook
#
# Two kinds of cell:
#
# - **Text cells** like this one, written in Markdown
# - **Code cells** like the next one, which run and show their output
#
# Run a cell with **Shift+Enter**.

# %%
print("Hello, Social and Cultural Analytics")

# %% [markdown]
# ### Markdown headings
#
# `#` makes a big heading, `##` a smaller one, `###` smaller again.
#
# You will use text cells to write the commentary in your final report, so it is worth getting
# comfortable with them now.

# %% [markdown]
# ## 2. Python as a calculator

# %%
2 + 5

# %%
# Multiplication happens before addition, as in ordinary arithmetic.
# So this is 3 + 10, not 5 * 5.
3 + 2 * 5

# %% [markdown]
# ### Powers — the trap
#
# In R and Excel, `^` means "to the power of". In Python it does **not**.

# %%
# ** is "to the power of"
2 ** 3

# %%
# ^ is NOT powers in Python. It gives 1 here, with no error at all.
# This is the most common Week 1 mistake for anyone coming from R or Excel.
2 ^ 3

# %% [markdown]
# ## 3. Variables
#
# `=` means "put this value in this box". It does not mean "these are equal".

# %%
a = 3
b = 6
x = a * b
x

# %%
# Two different boxes, because names are case sensitive.
a = 3
A = 2
print(a, A)

# %% [markdown]
# ### Deleting a variable

# %%
c = 10
del c
# Uncomment the next line to see the error. NameError means "I have no box with that name".
# print(c)

# %% [markdown]
# ## 4. Types

# %%
print(type(7))        # int   — a whole number
print(type(7.5))      # float — a number with a decimal point
print(type("London"))  # str   — text, always in quotes
print(type(True))     # bool  — True or False, capitalised, no quotes

# %% [markdown]
# ### Text that looks like a number

# %%
print(7 == 7)     # True
print("7" == 7)   # False — one is text, the other is a number

# %% [markdown]
# ## 5. Comparing things

# %%
print(3 == 4)   # False
print(3 != 4)   # True  — != means "is not equal to"
print(2 <= 2)   # True
print(2 > 3)    # False

# %%
print("London" == "London")     # True
print("Cambridge" == "Oxford")  # False

# %% [markdown]
# ### Comparing text alphabetically
#
# What do you expect here? What actually happens?

# %%
print("a" > "z")   # False — a comes before z
print("z" > "a")   # True
print("A" > "a")   # False — capitals sort BEFORE lower case, which surprises most people
print("A" == "a")  # False — comparison is case sensitive

# %% [markdown]
# ## 6. Where we are going
#
# You are not expected to understand this yet. Run it and look at the result.

# %%
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
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
counts = museum["region"].value_counts()

counts.plot(kind="bar", color="#0A2D50", title="Museum objects by region")
plt.ylabel("objects")
plt.tight_layout()
plt.show()

# %% [markdown]
# **The analytical question:** that chart counts museum objects by region.
#
# What claim about culture would it support? What would it *not* support?
#
# End of live coding.
