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
# # Week 7 — live coding
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**.
#
# The cells are **deliberately empty** — they get filled in during the lecture.

# %% [markdown]
# ## Setup

# %%
# Imports, data_path, load the newspapers list


# %% [markdown]
# ## 1. A bar plot, and making it readable

# %%
# Top five countries, as a frequency table


# %%
# Plot it. What is wrong with the default?


# %%
# Fix it: figsize, rot, colour, title, axis labels, tight_layout


# %% [markdown]
# ## 2. From crosstab to chart

# %%
# Filter to five countries and three frequencies. Build the crosstab.


# %%
# How much of the dataset has a recorded frequency?


# %%
# Stacked -- remember .T


# %%
# Grouped


# %%
# Proportional -- normalize="columns"


# %% [markdown]
# Which chart supports which argument?

# %% [markdown]
# ## 3. Distributions: newspaper lifespans

# %%
# Build the length column. mean, median, min, max.


# %%
# describe() -- what are Q1, Q3, the IQR?


# %%
# How many lasted 0 years? Over 100?


# %% [markdown]
# ## 4. Histograms

# %%
# A basic histogram


# %%
# The same data with 3, 30 and 500 bins


# %%
# Add median and mean lines, with a legend


# %%
# Which title is the outlier?


# %% [markdown]
# ## 5. How easy it is to mislead

# %%
# Two bars, 1020 and 1035. Draw with y from 0, and with y from 1000.


# %% [markdown]
# ## 6. Saving a figure

# %%
# Make a figures folder, save as PNG at 150 dpi and as PDF


# %% [markdown]
# End of live coding.
