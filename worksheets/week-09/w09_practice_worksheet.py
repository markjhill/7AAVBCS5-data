# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Week 9 — London spaCy practice
#
# Work on this **after** the main spaCy worksheet. Use the same small
# steps on the supplied London articles, then try a comparison of your own.
#
# Run the setup below. The file locator only finds the supplied CSV;
# the text processing and analysis are the tasks that follow.

# %% tags=["provided-setup"]
import spacy
import pandas as pd
from pathlib import Path
nlp = spacy.load('en_core_web_sm')


# %% tags=["provided-file-setup"]
# PROVIDED FILE LOCATOR: locates supplied CSVs without loading or analysing them.
def teaching_file(name):
    for parent in (Path.cwd(), *Path.cwd().parents):
        for candidate in (parent / "data" / name,
                          parent / "weeks/week-09/data" / name, parent / name):
            if candidate.is_file():
                return candidate
    raise FileNotFoundError(f"Cannot find {name}. Extract the Week 9 download, or upload the supplied data files in Colab.")


# %% tags=["provided-setup"]
articles = pd.read_csv(teaching_file("w09_articles.csv"))
articles[["title", "opening_sentence"]]

# %% [markdown]
# ## P1. From a string to tokens
#
# Select the **Horniman Museum opening sentence**, print it and create
# `practice_doc`. Print the type of the original text and of the Doc.
# Then print each token separately and count the tokens with `len()`.

# %% [markdown]
# **Your turn.** Write the selection and token loop. Which punctuation is counted as a token?

# %% tags=["student-task"]
# Write your code here.

# %% [markdown]
# **Your notes:**

# %% [markdown]
# ## P2. Inspect annotations before filtering
#
# Print each token's text, lemma, POS, stop-word and punctuation flag.
# Name one difference between an original form and its lemma, if one occurs.
# Which words would a stop-word filter remove, and what might that lose?

# %% [markdown]
# **Your turn.** Use a plain loop over `practice_doc`. Do not remove anything yet.

# %% tags=["student-task"]
# Write your code here.

# %% [markdown]
# **Your notes:**

# %% [markdown]
# ## P3. Check named entities
#
# Print entity text and label, then collect those values into a DataFrame
# called `named_entities`. Count its labels. Check the labels against the
# original sentence: is anything surprising?

# %% [markdown]
# **Your turn.** Use one dictionary per entity mention. Explain why this table has a different number of rows from a token table.

# %% tags=["student-task"]
# Write your code here.

# %% [markdown]
# **Your notes:**

# %% [markdown]
# ## P4. Turn token features into a table
#
# Build `practice_tokens` with word, lemma, pos, is_stop and is_punct columns.
# Count the POS labels. Then exclude punctuation and stop words in separate
# pandas selections and count the remaining lemmas.

# %% [markdown]
# **Your turn.** Create the list before the loop and the DataFrame after it. State what one row represents before and after filtering.

# %% tags=["student-task"]
# Write your code here.

# %% [markdown]
# **Your notes:**

# %% [markdown]
# ## P5. Compare a different pair of articles
#
# Compare the full **Roundhouse** and **Jazz Cafe** articles. Build token
# tables with the same word, lemma and pos columns. Compare noun lemmas:
# what words distinguish their accounts? Use percentages of each article's
# noun tokens if you compare numerical concentration.
#
# Adapt section 6 of the main worksheet. Start with the same counting rule
# for both articles and inspect a source passage for one result.

# %% [markdown]
# **Your turn.** Build both tables and compare at least two terms. What might article structure or historical material contribute to the difference?

# %% tags=["student-task"]
# Write your code here.

# %% [markdown]
# **Your notes:**

# %% [markdown]
# ## P6. Investigate a person, organisation or place
#
# Use the full Roundhouse article to build an entity table. Select one label,
# such as ORG or GPE, and count repeated names. Choose one result, find its
# sentence in the original Doc and explain what it refers to.

# %% [markdown]
# **Your turn.** Do repeated names describe the venue itself, a performer, a location or another organisation? Explain why repeated mentions are not a count of distinct institutions.

# %% tags=["student-task"]
# Write your code here.

# %% [markdown]
# **Your notes:**

# %% [markdown]
# ## Further reading and sources
#
# Main guide: Tuomo Hiippala's University of Helsinki materials,
# [Processing texts using spaCy](https://applied-language-technology.mooc.fi/html/notebooks/part_ii/03_basic_nlp.html)
# and [Managing textual data using pandas](https://applied-language-technology.mooc.fi/html/notebooks/part_ii/06_managing_data.html).
# Supplement: Ines Montani's [spaCy course, Chapter 1](https://course.spacy.io/en/chapter1/),
# especially documents/tokens, lexical attributes and predicted annotations.
# These resources explain the ideas in more depth. Their course materials
# are available under CC BY-NC licences; see the linked sites for details.
# The short visitor example and exercises here are newly written.
#
# London article text: Wikipedia contributors, CC BY-SA 4.0. The supplied
# article rows retain their source URLs and revision IDs. See `data/README.md`.
# Alice's visit in the opening example is fictional, not a visitor record.
