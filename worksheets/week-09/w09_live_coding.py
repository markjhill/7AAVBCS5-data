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
# # Week 9 — live coding
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# The cells are **deliberately empty** — they get filled in during the lecture.

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

# %% [markdown]
# ## 1. A function

# %%
# calculate_percentage(part, total)


# %%
# print is not return -- show the difference


# %% [markdown]
# ## 2. An if statement

# %%
# Pass or Fail on a grade


# %% [markdown]
# ## 3. A for loop

# %%
# Print each follower count


# %%
# Now COLLECT them instead of printing


# %% [markdown]
# ## 4. A while loop

# %%
# Count down from 5


# %% [markdown]
# ## 5. Putting it together: a folder of texts

# %%
# How many files? Print the first three with their character counts.


# %%
# Write word_count(), then loop over every file collecting a row per speech


# %%
# Turn it into a data frame. Mean words? Speeches per president?


# %%
# Two surprises hide in this data. Find the empty file, and look at the president counts.


# %% [markdown]
# End of live coding.
