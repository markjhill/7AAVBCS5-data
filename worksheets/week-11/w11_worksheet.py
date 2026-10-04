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
# # Week 11 — Topic modelling and sentiment analysis
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# **Working in Colab?** Download this file from KEATS, then in Colab choose
# **File → Upload notebook**.
#
# ## What you will be able to do by the end
#
# - Build a document–term matrix and explain what it discards
# - Run LDA, read its topics, and improve them by changing pre-processing
# - Express documents as mixtures of topics
# - Apply lexicon-based sentiment scoring at the right unit of analysis
# - Recognise a method that runs, returns a number, and is wrong
#
# ## The contextual dimension in play this week
#
# Chapter §5.3 and §5.5. Both methods this week produce a **point estimate** from a text — a topic
# proportion, a sentiment score. The whole difficulty is what that estimate is a measurement *of*.

# %% [markdown]
# ## Setting up

# %%
import re
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

ensure("vaderSentiment")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


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


# Load the corpus, skipping the empty 1790 file (Week 9).
docs, names, years, presidents = [], [], [], []
for path in sorted((data_path("SUA")).glob("*.txt")):
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        continue
    president, year = path.stem.split("_")
    docs.append(text)
    names.append(path.stem)
    presidents.append(president)
    years.append(int(year))

print(len(docs), "speeches loaded")

# %% [markdown]
# ## 1. The document–term matrix

# %%
# A worked example.
vec = CountVectorizer(stop_words="english", min_df=10, max_df=0.9)
dtm = vec.fit_transform(docs)
print(f"{dtm.shape[0]} documents x {dtm.shape[1]} terms")

# %% [markdown]
# **Task 1.1.** Print the sparsity of the matrix — the percentage of cells that are zero.
#
# Hint: `dtm.nnz` is the number of non-zero entries.

# %%
# write your code here


# %% [markdown]
# **Task 1.2.** Print the 15 most frequent terms across the whole corpus.
#
# Hint: `dtm.sum(axis=0)` totals each column; `vec.get_feature_names_out()` gives the terms.

# %%
# write your code here


# %% [markdown]
# **Task 1.3.** In a text cell: the DTM discards word order entirely. Name one research question
# about political speech that this makes impossible to answer.

# %% [markdown]
# ## 2. Topic modelling

# %%
# A worked example.
lda = LatentDirichletAllocation(n_components=5, random_state=0, max_iter=10)
lda.fit(dtm)

terms = vec.get_feature_names_out()
for k, component in enumerate(lda.components_):
    top = [terms[i] for i in component.argsort()[-8:][::-1]]
    print(f"topic {k}: " + ", ".join(top))

# %% [markdown]
# **Task 2.1.** Look hard at those topics. In a text cell, list **two** things wrong with them.
#
# One is a pre-processing failure. The other is about what the model has actually separated.

# %% [markdown]
# **Task 2.2.** Fix the pre-processing failure. Rebuild the DTM excluding tokens that are numbers,
# then rerun LDA and print the topics again.
#
# Hint: `CountVectorizer(token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b", ...)`

# %%
# write your code here


# %% [markdown]
# **Task 2.3.** Did the topics improve? Answer in a text cell, and say what "improve" means here —
# who decides?

# %% [markdown]
# **Task 2.4.** Run LDA again with `random_state=42` instead of `0`, everything else the same.
#
# Are the topics identical? What does that tell you, and what must you therefore do in your report?

# %%
# write your code here


# %% [markdown]
# ## 3. Documents as mixtures

# %%
# A worked example.
doc_topics = pd.DataFrame(
    lda.transform(dtm), index=names,
    columns=[f"topic_{i}" for i in range(5)]
).round(3)
doc_topics.head()

# %% [markdown]
# **Task 3.1.** Confirm that each row sums to 1 (or very close).

# %%
# write your code here


# %% [markdown]
# **Task 3.2.** For one topic of your choice, print the five speeches where it is strongest. Do they
# have anything in common — a period, a president?

# %%
# write your code here


# %% [markdown]
# **Task 3.3.** Add the `year` to `doc_topics` and plot one topic's proportion against year.
#
# In a text cell, describe what you see, and be careful to distinguish what the chart shows from what
# you think it means.

# %%
# write your code here


# %% [markdown]
# ## 4. Sentiment — and a trap

# %%
# A worked example on short text.
analyser = SentimentIntensityAnalyzer()
for s in ["This is a wonderful and hopeful day.", "I am happy", "I am not happy"]:
    print(f"{s:38} {analyser.polarity_scores(s)['compound']:+.4f}")

# %% [markdown]
# **Task 4.1.** In a text cell, explain what happened to "I am not happy", and why that matters given
# what you learned about stop words last week.

# %% [markdown]
# **Task 4.2.** Now score three **whole speeches** — the first, middle and last in the corpus — and
# print each compound score.

# %%
# write your code here


# %% [markdown]
# **Task 4.3.** Something is wrong. In a text cell, say what, and why it happens.
#
# Hint: what would a score of 0.9999 mean, and is it plausible that every speech is equally and
# maximally positive?

# %% [markdown]
# ## 5. Choosing the right unit of analysis

# %%
# A worked example: score sentences instead of whole documents.
def sentence_sentiment(text, limit=400):
    """Mean VADER compound score across the sentences of a text."""
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text) if len(s.split()) > 3]
    if not sentences:
        return None
    scores = [analyser.polarity_scores(s)["compound"] for s in sentences[:limit]]
    return sum(scores) / len(scores)


print(round(sentence_sentiment(docs[0]), 4))

# %% [markdown]
# **Task 5.1.** Apply `sentence_sentiment` to every speech, collecting a data frame `sentiment` with
# columns `name`, `president`, `year` and `mean_compound`.
#
# This takes a minute or two. It is the Week 9 loop pattern again.

# %%
# write your code here


# %% [markdown]
# **Task 5.2.** Print the `describe()` of `mean_compound`. Compare the spread to what you got in Task
# 4.2.

# %%
# write your code here


# %% [markdown]
# **Task 5.3.** Print the five **least** positive speeches, and the five most.
#
# In a text cell: do the least positive ones correspond to anything you know about? What does that
# tell you about whether the measure is working?

# %%
# write your code here


# %% [markdown]
# **Task 5.4.** Plot `mean_compound` against `year`, and print the correlation.
#
# In a text cell, give **two** different explanations for the pattern, and say what evidence would
# distinguish them.

# %%
# write your code here


# %% [markdown]
# ## 6. Putting the two together

# %% [markdown]
# **Task 6.1.** Join your `sentiment` data frame to `doc_topics`, then check whether speeches
# dominated by one topic are more or less positive than speeches dominated by another.
#
# Report the correlation between one topic's proportion and `mean_compound`.

# %%
# write your code here


# %% [markdown]
# **Task 6.2.** In a text cell, write the limitations paragraph you would put in a report using this
# analysis. Cover:
#
# - What the topic model did and did not do
# - What VADER measures, and at what unit
# - Which pre-processing decisions could have changed the result
# - One claim you are explicitly **not** making

# %% [markdown]
# ## 7. Bonus workshop: your dataset
#
# Optional. Use this only if your project has a corpus of documents or text fields. If not, use this
# section to write the limitations paragraph for your actual final-report method instead.

# %% [markdown]
# **Task 7.1.** Try one Week 11 method on your own text data: a document-term matrix, a topic model
# or sentence-level sentiment.
#
# Keep the first version small. A few documents or a sample of rows is enough for a workshop test.

# %%
# write your code here


# %% [markdown]
# **Task 7.2.** In a text cell, write what you would need to report for this method to be
# reproducible and honest:
#
# - what you removed or kept
# - what unit of analysis you used
# - any random seed or model setting
# - how you checked whether the output made sense
# - one claim you are **not** making

# %% [markdown]
# ## Stretch tasks

# %% [markdown]
# **Stretch 1.** Rebuild the DTM using spaCy **lemmas** instead of raw tokens, then rerun LDA.
#
# This is slow — use `nlp.pipe()` and disable the parser and NER. Do the topics look different?
#
# You will need spaCy and its English model. Copy the `ensure("spacy")` call and the
# `load_english()` function from the top of last week's worksheet — on Colab they download the
# model for you.

# %%
# write your code here


# %% [markdown]
# **Stretch 2.** Run LDA with 3, 8 and 15 topics. Print the top words for each.
#
# In a text cell: which number would you choose, and on what grounds? Note that this is a research
# decision, not a technical one.

# %%
# write your code here


# %% [markdown]
# **Stretch 3.** VADER gives `pos`, `neu` and `neg` proportions as well as `compound`. Those do not
# saturate on long text.
#
# Score the whole speeches using `pos` minus `neg` instead, and compare the ranking to your
# sentence-level result. Do they agree?

# %%
# write your code here


# %% [markdown]
# ## That's it
#
# **Restart and Run All** before you close this notebook.
#
# The report is due **21 January 2027**, and there is a project clinic in January.
#
# End of worksheet — and of the module.
