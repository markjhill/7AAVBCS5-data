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
# # Week 8 — Scatter plots and correlation
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**.
#
# ## What you will be able to do by the end
#
# - Draw a scatter plot and describe the pattern in it
# - Calculate Pearson and Spearman correlations
# - Say which is appropriate, and why, for a given pair of variables
# - Encode a third variable using size or colour
# - Report a null result honestly
# - Explain why a correlation is not a cause
#
# ## The contextual dimension in play this week
#
# Chapter §5.4–5.5. A correlation is a **detected pattern**. Turning it into a claim about culture
# requires a second dimension and an argument — and this week you will meet a pair of variables where
# the pattern is real and the interpretation is still wide open.

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


dawtry = pd.read_csv(data_path("DawtryEtAl2015.csv"))
print("survey:", dawtry.shape)

# %% [markdown]
# The dataset is from Dawtry, Sutton & Sibley (2015), a study of how people estimate the income
# distribution of their society. Relevant columns:
#
# | Column | Meaning |
# |---|---|
# | `Household_Income` | the respondent's own household income |
# | `Social_Circle_Mean_Income` | mean income of the people they know |
# | `Population_Mean_Income` | their estimate of the national mean |
# | `fairness` | how fair they think society is |
# | `satisfaction` | how satisfied they are with it |
# | `Political_Preference` | left–right self-placement |
# | `redist1` | support for redistribution |

# %% [markdown]
# ## 1. Your first scatter plot

# %%
# A worked example.
fig, ax = plt.subplots(figsize=(7, 3))
ax.scatter(dawtry["Household_Income"], dawtry["Social_Circle_Mean_Income"],
           color="steelblue", s=18)
ax.set_xlabel("Household income")
ax.set_ylabel("Social circle mean income")
plt.tight_layout()
plt.show()

# %% [markdown]
# **Task 1.1.** Draw a scatter plot of `Social_Circle_Mean_Income` (x) against
# `Population_Mean_Income` (y), with axis labels and a title.

# %%
# write your code here


# %% [markdown]
# **Task 1.2.** In a text cell, describe the pattern using the vocabulary from the lecture:
# direction, strength, shape, and any outliers.

# %% [markdown]
# ## 2. Measuring the relationship

# %%
# A worked example.
pair = dawtry[["Household_Income", "Social_Circle_Mean_Income"]].dropna()
print("n =", len(pair))
print("Pearson :", round(pair["Household_Income"].corr(pair["Social_Circle_Mean_Income"]), 3))

# %% [markdown]
# **Task 2.1.** Calculate the Pearson correlation between `Social_Circle_Mean_Income` and
# `Population_Mean_Income`. How strong is it, using the table from the lecture?

# %%
# write your code here


# %% [markdown]
# **Task 2.2.** Now calculate the **Spearman** correlation for the same pair. Are they similar?

# %%
# write your code here


# %% [markdown]
# ## 3. When the two disagree

# %%
# Given: a pair where Pearson and Spearman do not agree.
pair = dawtry[["Household_Income", "fairness"]].dropna()
print("Pearson :", round(pair["Household_Income"].corr(pair["fairness"]), 3))
print("Spearman:", round(pair["Household_Income"].corr(pair["fairness"], method="spearman"), 3))

# %% [markdown]
# **Task 3.1.** Draw a histogram of `Household_Income`, and print its minimum.
#
# In a text cell, explain why Pearson and Spearman disagree here, and which you would report.
#
# (You met this variable in Week 7. The answer is in its distribution.)

# %%
# write your code here


# %% [markdown]
# **Task 3.2.** Recalculate both correlations **excluding** the households reporting under £1,000.
#
# Does the gap between Pearson and Spearman narrow? What does that tell you?

# %%
# write your code here


# %% [markdown]
# ## 4. A real relationship, and a real null

# %%
# A worked example.
s = dawtry[["Political_Preference", "redist1"]].dropna()
print("n =", len(s), "| r =", round(s["Political_Preference"].corr(s["redist1"]), 3))

# %% [markdown]
# **Task 4.1.** Draw the scatter plot for that pair. Does the chart look as strong as the number
# suggests? Why might it not?

# %%
# write your code here


# %% [markdown]
# **Task 4.2.** Now calculate the correlation between `age` and `Household_Income`.
#
# In a text cell, write the sentence you would put in a report about this result. Be careful not to
# write "there is no relationship" when what you mean is "we found none in this sample".

# %%
# write your code here


# %% [markdown]
# ## 5. Anscombe's quartet
#
# Four datasets, nearly identical statistics.

# %%
# Given: the quartet.
x1 = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
x4 = [8] * 8 + [19, 8, 8]
sets = {
    "I":   (x1, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    "II":  (x1, [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    "III": (x1, [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    "IV":  (x4, [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 5.56, 12.50, 7.91, 6.89]),
}

# %% [markdown]
# **Task 5.1.** For each of the four sets, print the mean of x, the mean of y and the Pearson
# correlation, each rounded to 2 or 3 decimal places.

# %%
# write your code here


# %% [markdown]
# **Task 5.2.** Now plot all four as scatter plots side by side.
#
# In a text cell, describe what is actually going on in each, and say what the quartet is an argument
# for.

# %%
# write your code here


# %% [markdown]
# ## 6. A third variable

# %%
# A worked example: size encodes age.
sub = dawtry[["Household_Income", "Social_Circle_Mean_Income", "age"]].dropna()
fig, ax = plt.subplots(figsize=(7, 3))
ax.scatter(sub["Household_Income"], sub["Social_Circle_Mean_Income"],
           s=sub["age"] / 2, alpha=0.5, color="steelblue")
ax.set_xlabel("Household income")
ax.set_ylabel("Social circle mean income")
plt.tight_layout()
plt.show()

# %% [markdown]
# **Task 6.1.** Redraw the `Household_Income` vs `fairness` scatter plot, colouring the points by
# `gender`, with a legend.
#
# Hint: loop over `sub.groupby("gender")` and call `ax.scatter` once per group.

# %%
# write your code here


# %% [markdown]
# **Task 6.2.** In a text cell: does the relationship look different within the groups than it does
# overall? This is how you would look for Simpson's Paradox.

# %% [markdown]
# ## 7. Correlation and cause
#
# No code.

# %% [markdown]
# **Task 7.1.** You have found that people with higher incomes estimate higher average incomes for
# the population as a whole (r = 0.475 between own income and social circle income).
#
# In a text cell, write:
#
# - One causal story that would explain this
# - **A different** causal story that would explain it equally well
# - One confounder that could produce it with no causal link at all
# - What evidence would let you choose between them

# %% [markdown]
# ## 8. Bonus workshop: your dataset
#
# Optional. If your own dataset has at least two numeric columns, use it. If not, use `dawtry`.

# %% [markdown]
# **Task 8.1.** Choose two numeric variables in your dataset that might plausibly be related.
#
# Draw a scatter plot, then calculate Pearson and Spearman correlations.

# %%
# write your code here


# %% [markdown]
# **Task 8.2.** In a text cell, write the report sentence:
#
# - Which correlation would you report, and why?
# - Is the relationship strong enough to matter?
# - What causal claim are you **not** making?

# %% [markdown]
# ## Stretch tasks

# %% [markdown]
# **Stretch 1.** `dawtry.corr(numeric_only=True)` gives a correlation matrix of every numeric column.
# Compute it, then find the strongest correlation that is **not** a variable with itself.
#
# Careful: with 37 columns you are computing hundreds of correlations. What is the risk?

# %%
# write your code here


# %% [markdown]
# **Stretch 2.** Add a trend line to your Task 1.1 scatter plot using `numpy.polyfit` with degree 1.
#
# Then, in a text cell, say why a trend line can be misleading on a curved relationship.

# %%
# write your code here


# %% [markdown]
# **Stretch 3.** Load the newspapers dataset and try to correlate `first_date_held` with
# `last_date_held`.
#
# It will not work. Find out why by looking at the values in `last_date_held`.
#
# Then do it properly with `publication_date_one` and `publication_date_two`. The correlation is
# very high — but is it interesting?

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
