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
# # Week 3 — live coding
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
# Import pandas, and set up data_path


# %% [markdown]
# ## 1. Creating a data frame
#
# Build a table of four television programmes: `title`, `year`, `rating`, `streaming_platform`,
# `watched_again`.

# %%
# Build the dictionary of columns, then the data frame


# %%
# Explore it: info(), head(), describe()


# %%
# Add a years_old column


# %%
# Find the shows rated above 7


# %% [markdown]
# ## 2. Exploring the museum data

# %%
# Load it. How many objects? What columns?


# %%
# Build the overview table: type, present, missing, missing_%, distinct


# %%
# The most valuable object


# %%
# The oldest acquisition


# %%
# Objects from one region only


# %% [markdown]
# ### Making a category

# %%
# Add a value_category column: high / medium / low


# %% [markdown]
# ## 3. `.loc` and `.iloc` — where it matters

# %%
# On the full table they agree


# %%
# Filter, then compare them again. What happened to the index?


# %% [markdown]
# ## 4. Files
#
# `fruitData.csv`

# %%
# Where are we? What files can we see?


# %%
# Load fruitData.csv and look at it


# %%
# How many of each colour? How many of each shape?


# %%
# Add a column, make a subset, save it with index=False


# %%
# Read it back and check the columns are what you expect


# %% [markdown]
# ## 5. Debugging with AI
#
# Break something on purpose, then take the error apart.

# %%
# Ask for a column that does not exist. Read the KeyError.


# %%
# Use `and` where `&` is needed. Read the ValueError.


# %% [markdown]
# End of live coding.
