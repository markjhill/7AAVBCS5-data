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
# # Week 10 — Text processing with spaCy
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**. On Colab you may also need to run
# `!python -m spacy download en_core_web_sm` once.
#
# ## What you will be able to do by the end
#
# - Annotate a text with spaCy and turn the result into a data frame
# - Distinguish tokens from types, and words from lemmas
# - Remove stop words — and say what that costs you
# - Count word frequencies and read them critically
# - Extract named entities
# - Apply the whole pipeline across a corpus with a loop
#
# ## The contextual dimension in play this week
#
# Chapter §5.3 — **representation**. Every stage of an NLP pipeline is a decision that removes
# something. This week you will remove things on purpose, and then look at what went with them.

# %% [markdown]
# ## Setting up

# %%
import subprocess
import sys
from pathlib import Path


def ensure(package: str) -> None:
    """Install a package if it is missing.

    Nothing happens on your own machine, where the setup instructions already
    installed everything. On Colab, which starts bare each session, this fills
    in whatever is not preinstalled.
    """
    import importlib

    try:
        importlib.import_module(package)
        return
    except ImportError:
        pass

    print(f"Installing {package} (once)...")
    for attempt in (1, 2):
        done = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", package],
            capture_output=True,
            text=True,
        )
        if done.returncode == 0:
            importlib.invalidate_caches()
            return
        if attempt == 1:
            print("  that did not work; trying once more...")
    raise RuntimeError(
        f"Could not install {package}, which this week needs. This is almost always "
        f"a network problem.\n\n"
        f"Run this in a cell of its own, then re-run this one:\n"
        f"    !pip install {package}\n\n"
        f"pip said:\n{done.stderr.strip()[-400:]}"
    )

ensure("spacy")

import pandas as pd
import spacy



def load_english():
    """Load spaCy's small English model, downloading it first if necessary.

    The model is a separate download from spaCy itself -- about 12 MB -- and a
    missing model is the commonest reason this week fails to run.
    """
    import importlib

    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        pass

    print("Downloading the English language model (once, about 12 MB)...")
    for attempt in (1, 2):
        done = subprocess.run(
            [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
            capture_output=True,
            text=True,
        )
        if done.returncode == 0:
            importlib.invalidate_caches()
            return spacy.load("en_core_web_sm")
        if attempt == 1:
            print("  that did not work; trying once more...")
    raise RuntimeError(
        "Could not download spaCy's English model, which this week needs. This is "
        "almost always a network problem.\n\n"
        "Run this in a cell of its own, then re-run this one:\n"
        "    !python -m spacy download en_core_web_sm\n\n"
        f"spaCy said:\n{done.stderr.strip()[-400:]}"
    )


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


nlp = load_english()
print("spaCy model loaded:", nlp.meta["name"], nlp.meta["version"])

# %% [markdown]
# ## 1. Annotating a sentence

# %%
# A worked example.
doc = nlp("Alice wasn't expecting the White Rabbit's waistcoat-pocket.")
print([t.text for t in doc])

# %% [markdown]
# **Task 1.1.** In a text cell, say what spaCy did with `wasn't` and `Rabbit's`, and how that differs
# from what `text.split()` would have done.
#
# Check by running `.split()` on the same sentence.

# %%
# write your code here


# %% [markdown]
# **Task 1.2.** For the sentence below, print each token with its lemma and part of speech, in three
# neat columns.

# %%
# Given.
sentence = "The rabbits were running and had run before the Queen painted the roses red."

# %%
# write your code here


# %% [markdown]
# **Task 1.3.** Build a data frame from that sentence with columns `token`, `lemma`, `pos` and
# `is_stop`, keeping only alphabetic tokens.

# %%
# write your code here


# %% [markdown]
# ## 2. A whole book

# %%
# Given: load Alice, and annotate the first 200,000 characters.
alice = (data_path("alice.txt")).read_text(encoding="utf-8", errors="replace")
doc = nlp(alice[:200_000])
print(len(doc), "tokens annotated")

# %% [markdown]
# **Task 2.1.** Make a Series of every alphabetic token, lower-cased. Print how many **tokens** there
# are, and how many **types** (distinct words).

# %%
# write your code here


# %% [markdown]
# **Task 2.2.** Print the ten most common words, **without** removing stop words.
#
# In a text cell, say whether this tells you anything about the book.

# %%
# write your code here


# %% [markdown]
# **Task 2.3.** Now do it again, keeping only non-stop-word lemmas. Print the top ten.
#
# What changed, and is the result more useful?

# %%
# write your code here


# %% [markdown]
# ## 3. What stop-word removal costs
#
# The lecture said every pipeline stage throws something away. Now measure it.

# %% [markdown]
# **Task 3.1.** How many tokens does spaCy consider stop words? Print the count and the percentage of
# all alphabetic tokens.

# %%
# write your code here


# %% [markdown]
# **Task 3.2.** Print the 20 most common **stop words** in the book.
#
# Look at the list carefully. In a text cell, name **two** research questions you could no longer
# answer once these are removed.
#
# Hint: look for pronouns, and for anything that negates.

# %%
# write your code here


# %% [markdown]
# ## 4. Parts of speech

# %%
# A worked example.
pd.Series([t.pos_ for t in doc]).value_counts().head(8)

# %% [markdown]
# **Task 4.1.** Print the ten most common **verbs** in the book, by lemma.
#
# Hint: filter on `t.pos_ == "VERB"`.

# %%
# write your code here


# %% [markdown]
# **Task 4.2.** Now the ten most common **adjectives**.
#
# In a text cell: does this list feel like it describes *Alice in Wonderland*? What would you compare
# it against to find out?

# %%
# write your code here


# %% [markdown]
# ## 5. Named entities

# %%
# A worked example.
print([(e.text, e.label_) for e in nlp("President Wilson addressed Congress in 1917.").ents])

# %% [markdown]
# **Task 5.1.** Print the counts of each entity **label** in Alice. Use `spacy.explain()` on the top
# three to find out what they mean.

# %%
# write your code here


# %% [markdown]
# **Task 5.2.** Print the ten most frequent `PERSON` entities.
#
# In a text cell: are these all people? What does that tell you about applying a model trained on
# modern news text to a Victorian children's book?

# %%
# write your code here


# %% [markdown]
# ## 6. The whole corpus
#
# The Week 9 pattern, applied to text.

# %%
# Given: the State of the Union corpus.
SUA = data_path("SUA")
files = sorted(SUA.glob("*.txt"))
print(len(files), "speeches")

# %% [markdown]
# **Task 6.1.** Loop over the **first 15** speeches. For each one, annotate it with spaCy and collect
# a row with: `file`, `president`, `year`, `tokens`, `types`.
#
# Then build a data frame called `corpus`.
#
# Two warnings. Annotating is slow, so 15 is enough. And remember what you found in Week 9 about one
# of these files.

# %%
# write your code here


# %% [markdown]
# **Task 6.2.** Print `corpus`, sorted by year. Does anything look wrong?

# %%
# write your code here


# %% [markdown]
# **Task 6.3.** Add a `type_token_ratio` column — types divided by tokens — and print it.
#
# In a text cell: what might a higher ratio mean? And why is comparing this ratio between documents
# of very different lengths a bad idea?

# %%
# write your code here


# %% [markdown]
# ## 7. Bonus workshop: your dataset

# %% [markdown]
# **Task 7.1.** If your project uses text, run spaCy on a small sample of your own data and create
# one frequency table, POS table or entity table. If your project does not use text, use Alice.

# %%
# write your code here


# %% [markdown]
# **Task 7.2.** In a text cell, write the paragraph you would put in your report's method section
# describing your text pre-processing.
#
# It should state: what you removed, why, and **what analysis that makes impossible**.
#
# If you are not using text in your project, write it for the Alice analysis above.

# %% [markdown]
# ## Stretch tasks

# %% [markdown]
# **Stretch 1.** `nlp.pipe()` annotates many texts far faster than calling `nlp()` in a loop. Rewrite
# Task 6.1 using it, and time both.

# %%
# write your code here


# %% [markdown]
# **Stretch 2.** Find the ten most common words that immediately follow the word "alice" in the book.
#
# Hint: loop over the tokens by index and look at `doc[i + 1]`.

# %%
# write your code here


# %% [markdown]
# **Stretch 3.** spaCy assigns each token a `.morph` — the full morphological analysis. Print the
# morphology of every verb in one sentence.
#
# The R module used UDPipe, which made a sharp distinction between morphological tagging and
# part-of-speech tagging. Looking at this output, what is the difference?

# %%
# write your code here


# %% [markdown]
# ## Before next week
#
# **Restart and Run All** before you close this notebook.
#
# Next week is the last: topic modelling and sentiment analysis.
#
# The quiz in next week's lecture covers **this week's** material, and is the **last one**.
#
# End of worksheet.
