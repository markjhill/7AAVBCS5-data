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
# # Week 2 — live coding
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**.
#
# The cells are **deliberately empty** — they get filled in during the lecture. Follow along and
# type it yourself; watching is not the same as doing.

# %% [markdown]
# ## 1. Lists

# %%
# Make a list of ages. Print it.


# %%
# How many items? What is the first one? The third? The last?


# %% [markdown]
# ### Positions start at zero

# %%
# ages[0], ages[2], ages[-1]


# %%
# Ask for a position that does not exist, and read the error.


# %% [markdown]
# ### Slicing — the end is excluded

# %%
# ages[0:3], ages[:2], ages[3:]


# %% [markdown]
# ### Changing a list

# %%
# append something, replace something


# %% [markdown]
# ## 2. The trap: lists do not do maths

# %%
# What does ages * 2 do? Predict first.


# %% [markdown]
# ## 3. Arrays do

# %%
# import numpy, make an array, multiply it


# %%
# Convert Celsius to Fahrenheit for a whole array at once


# %%
# Which values are above a threshold?


# %% [markdown]
# ### Arrays force one type

# %%
# Mix a number, a boolean and some text in an array. What happens?


# %% [markdown]
# ## 4. Describing data

# %%
# count, min, max, sum, mean, median, standard deviation


# %% [markdown]
# ## 5. Building text with f-strings

# %%
# Put a variable inside a sentence


# %% [markdown]
# ## 6. Dictionaries

# %%
# Make a dictionary about a student. Look something up by name. Add a key.


# %% [markdown]
# ## 7. Making a decision

# %%
# if / else on a temperature


# %%
# if / elif / else on a mark


# %%
# Combine two conditions with `and`


# %% [markdown]
# ## 8. How not to lose an afternoon

# %%
# Make a variable in this cell.


# %%
# Use it here. Then delete the cell above and run this again — it still works.
# Now Restart and Run All, and watch it break.


# %% [markdown]
# End of live coding.
