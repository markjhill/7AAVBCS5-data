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
# # Week 4 — live coding
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
# Imports and data_path


# %% [markdown]
# ## Exercise 1: quantify the gaps

# %%
# Load the museum data. Build the missing-data summary table.


# %%
# Which column is worst? Which is nearly complete?


# %%
# How many rows survive dropna()? Predict before running.


# %%
# Drop only the rows missing a valuation. How many go?


# %%
# Drop columns rather than rows, with a 50% completeness threshold.


# %% [markdown]
# ## Exercise 2: is the missingness patterned?

# %%
# Cross-tabulate acquisition_method against missing cultural_significance. Counts first.


# %%
# Now as row percentages. What changes?


# %%
# Try the same for original_owner.


# %%
# MCAR, MAR, or MNAR? Defend it.


# %% [markdown]
# ### What imputation would do here

# %%
# Fill acquisition_method with the mode, on a copy. Look at what happened to the counts.


# %% [markdown]
# ## Exercise 3: a survey, not a museum

# %%
# Load the April 2020 lockdown survey. Where are its gaps?


# %%
# Does age predict who skipped the forecast question?


# %%
# Does self-reported compliance?


# %%
# Look at the Gender breakdown -- counts AND percentages. What is the trap?


# %% [markdown]
# ## Exercise 4: changing a data frame

# %%
# Add a "missing indicator" column: was the owner recorded at all?


# %%
# Join the region lookup on, and check the row count did not change.


# %% [markdown]
# ## Exercise 5: your own project data
#
# Bring the dataset you are considering for the report.

# %%
# Load it. Build its missing-data summary.


# %%
# Find one column where the missingness looks patterned.


# %% [markdown]
# Write two sentences for your data overview about what that pattern might mean.
#
# End of live coding.
