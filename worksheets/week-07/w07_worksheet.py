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
# # Week 7 — Bar plots, distributions and histograms
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**. The setup cell below fetches the data over the internet,
# so nothing else changes.
#
# ## What you will be able to do by the end
#
# - Draw a bar plot from a frequency table, and make its labels readable
# - Choose between stacked, grouped and proportional bars, and say why
# - Describe a distribution's centre, spread, shape and outliers
# - Draw a histogram, choose a sensible number of bins, and add reference lines
# - Save a figure at publication quality
# - Spot a chart that is misleading you
#
# ## The contextual dimension in play this week
#
# Chapter §5.3 — **representing dimensions and constructing variables**. A bin width, an axis limit
# and a choice between counts and proportions are all analytical decisions that change what a reader
# concludes. This week you make several of them on purpose.
#
# Work through this in the workshop. Ask when you get stuck; that is what the session is for.

# %% [markdown]
# ## Setting up

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


news = pd.read_csv(data_path("BritishAndIrishNewspapersTitleList_20191118.csv"),
                   low_memory=False)
museum = pd.read_csv(data_path("museum_data.csv"))
print("newspapers:", news.shape, "| museum:", museum.shape)

# %% [markdown]
# ## 1. Your first bar plot

# %%
# A worked example.
countries_top = news["country_of_publication"].value_counts().head(5)
countries_top.plot(kind="bar")
plt.show()

# %% [markdown]
# **Task 1.1.** Draw a bar plot of the museum `object_type` counts.

# %%
# write your code here


# %% [markdown]
# **Task 1.2.** The labels on your plot are probably rotated or cramped. Redraw it with the labels
# horizontal, using `rot=0`, and give it a title and a y-axis label.
#
# Use the `fig, ax = plt.subplots(figsize=(7, 3))` pattern so you can control the size.

# %%
# write your code here


# %% [markdown]
# **Task 1.3.** Redraw it once more in a single colour of your choosing, with
# `plt.tight_layout()` before `plt.show()`.
#
# In a text cell, say what `tight_layout()` changed.

# %%
# write your code here


# %% [markdown]
# ## 2. Two variables at once

# %%
# Given: the crosstab from the lecture.
top5 = ["England", "Scotland", "Ireland", "Wales", "Northern Ireland"]
subset = news[news["country_of_publication"].isin(top5)
              & news["current_publication_frequency"].isin(["Weekly", "Daily", "Monthly"])]
countries_pf = pd.crosstab(subset["current_publication_frequency"],
                           subset["country_of_publication"])
countries_pf

# %% [markdown]
# **Task 2.1.** Draw this as a **stacked** bar chart, one bar per country.
#
# Hint: you will need `.T` to swap rows and columns, because pandas draws one bar per *row*.

# %%
# write your code here


# %% [markdown]
# **Task 2.2.** Now draw it **grouped** instead of stacked. Which is easier to read, and for what
# question?

# %%
# write your code here


# %% [markdown]
# **Task 2.3.** Now draw it as **proportions**, so every bar reaches 1.0.
#
# You will need `normalize="columns"` on the crosstab — the same argument as Week 5.

# %%
# write your code here


# %% [markdown]
# **Task 2.4.** In a text cell, answer: which of your three charts would you use to argue that
# "weekly publication dominated everywhere", and which to argue that "England published far more
# newspapers than anywhere else"?
#
# Both claims are true. That is the point.

# %% [markdown]
# **Task 2.5.** `current_publication_frequency` is missing for most of the dataset. Print how many
# titles it is missing for, and what percentage that is.
#
# In a text cell, say what caveat your three charts therefore need.

# %%
# write your code here


# %% [markdown]
# ## 3. Describing a distribution

# %%
# Given: newspaper lifespans, as in the lecture.
pub = news.dropna(subset=["publication_date_one", "publication_date_two"]).copy()
pub["length"] = pub["publication_date_two"] - pub["publication_date_one"]
print(len(pub), "titles have both dates")

# %% [markdown]
# **Task 3.1.** Print the mean, median, minimum and maximum lifespan.

# %%
# write your code here


# %% [markdown]
# **Task 3.2.** The mean is much larger than the median. In a text cell, say what that tells you
# about the shape of the distribution, and why it happens here.

# %% [markdown]
# **Task 3.3.** Print the full `describe()` output. What are Q1 and Q3, and what is the IQR?

# %%
# write your code here


# %% [markdown]
# **Task 3.4.** How many titles lasted **0 years**? How many lasted a year or less? How many lasted
# more than 100 years?

# %%
# write your code here


# %% [markdown]
# ## 4. Histograms

# %%
# A worked example.
fig, ax = plt.subplots(figsize=(7, 3))
pub["length"].plot(kind="hist", ax=ax, bins=30, color="steelblue", edgecolor="white")
ax.set_xlabel("Years in publication")
plt.tight_layout()
plt.show()

# %% [markdown]
# **Task 4.1.** Draw the same histogram three times, with 3 bins, 30 bins and 500 bins.
#
# In a text cell: which is most honest? Is that a fair question?

# %%
# write your code here


# %% [markdown]
# **Task 4.2.** Draw the histogram with 50 bins and add two vertical lines — one at the median and
# one at the mean — in different colours, with a legend.
#
# Hint: `ax.axvline(value, color=..., linestyle="--", label=...)` then `ax.legend()`.

# %%
# write your code here


# %% [markdown]
# **Task 4.3.** In a text cell, describe this distribution using the four headings from the lecture:
# centre, spread, shape, outliers.
#
# For the outlier, find out **which title** it is.

# %%
# write your code here


# %% [markdown]
# ## 5. Four distributions, four shapes
#
# Not every distribution is right-skewed. Here are three more.

# %%
# Given: load two more datasets.
dawtry = pd.read_csv(data_path("DawtryEtAl2015.csv"))
ncv = pd.read_csv(data_path("ncv-data-2020-Apr-1.csv"))

# %% [markdown]
# **Task 5.1.** Draw a histogram of `ncv["Age"]`, then print its mean and median.
#
# Is this distribution skewed? How can you tell from the two numbers alone?

# %%
# write your code here


# %% [markdown]
# **Task 5.2.** Draw a histogram of `museum["valuation"]`, then print its mean and median.
#
# The mean is *below* the median here. In a text cell, say what that means, and how it differs from
# the newspaper lifespans.

# %%
# write your code here


# %% [markdown]
# **Task 5.3.** Draw a histogram of `dawtry["Household_Income"]`, then print its `describe()`.
#
# Look hard at the **minimum**. In a text cell, say what you think has happened, and what you would
# do about it.

# %%
# write your code here


# %% [markdown]
# ## 6. Being misled
#
# The lecture showed charts that mislead on purpose. Now make one.

# %%
# Given: two years of made-up figures, barely different.
example = pd.Series([1020, 1035], index=["2024", "2025"])
print(example)

# %% [markdown]
# **Task 6.1.** Draw this as a bar chart twice: once with the y-axis starting at 0, and once with
# `ax.set_ylim(1000, 1040)`.
#
# In a text cell, describe the impression each gives.

# %%
# write your code here


# %% [markdown]
# **Task 6.2.** In a text cell, write the rule you will follow in your own report about bar-chart
# axes, and when you would break it.

# %% [markdown]
# ## 7. Saving a figure properly

# %% [markdown]
# **Task 7.1.** Make a `figures` folder, then save your best histogram from Task 4.2 as both a PNG
# at 150 dpi and a PDF. Use `bbox_inches="tight"`.
#
# Then check the files exist and look at the PNG.

# %%
# write your code here


# %% [markdown]
# ## 8. Bonus workshop: your dataset

# %% [markdown]
# **Task 8.1.** Using your own project dataset, produce **one** chart you might actually put in your
# report. Then write, in a text cell:
#
# - Why this chart type, for this data type?
# - What decisions did you make (bins, axis limits, counts vs proportions, colour)?
# - What would a reader wrongly conclude if they only glanced at it?
#
# The third question is the one that matters. Chapter §5.3.

# %%
# write your code here


# %% [markdown]
# **Task 8.2.** Save the chart as a PNG with `bbox_inches="tight"`, then check that the file exists.

# %%
# write your code here

# %% [markdown]
# ## Stretch tasks

# %% [markdown]
# **Stretch 1.** A histogram of a heavily skewed variable is mostly empty space. Draw the newspaper
# lifespans again with `ax.set_xlim(0, 50)` and then with a log-scaled y-axis
# (`ax.set_yscale("log")`).
#
# Which is more informative, and what does each hide?

# %%
# write your code here


# %% [markdown]
# **Stretch 2.** Draw a **horizontal** bar chart (`kind="barh"`) of the top 15 places of publication.
# Why is horizontal better than vertical when there are many long category names?

# %%
# write your code here


# %% [markdown]
# **Stretch 3.** matplotlib's default colours are not colour-blind safe. Run
# `plt.style.use("tableau-colorblind10")` and redraw your grouped bar chart from Task 2.2.
#
# Keep this in mind for your report — roughly 1 in 12 men has some form of colour vision deficiency.

# %%
# write your code here


# %% [markdown]
# ## Before next week
#
# **Restart and Run All** before you close this notebook.
#
# **The data overview is due next week — Monday 16 November.**
#
# The quiz in next week's lecture covers **this week's** material.
#
# End of worksheet.
