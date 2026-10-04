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
# # Week 5 — live coding
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
# ## Exercise 1: categorical data

# %%
# Which columns are text rather than numbers?


# %%
# Convert country_of_publication to a category. How many categories?


# %%
# How much of place_of_publication is missing?


# %%
# Some country values are compounds -- England|Wales. How many, covering how many titles?


# %%
# Filter to the five main countries, and say so.


# %% [markdown]
# ## Exercise 2: tables and cross-tabulation

# %%
# One-way frequency table of country


# %%
# The mode, and the number of distinct countries


# %%
# The same table as percentages


# %% [markdown]
# ### Two-way: is digitisation even?

# %%
# Make the digitised column. Crosstab country against it, with totals.


# %%
# What do the counts seem to show? Predict before the next cell.


# %%
# Now as row percentages. What changed?


# %%
# Now as column percentages. What different question does this answer?


# %%
# Turn a table into a data frame


# %% [markdown]
# ## Exercise 3: grouping

# %%
# Median first_date_held by country, with counts


# %%
# Group by country AND digitised. Compare the medians within each country.


# %% [markdown]
# What did we find, and what does it mean for anyone studying digitised newspapers?
#
# End of live coding.
