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
# # Week 11 — live coding
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# The cells are **deliberately empty**.

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


analyser = SentimentIntensityAnalyzer()

docs, names, years = [], [], []
for path in sorted((data_path("SUA")).glob("*.txt")):
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.strip():
        docs.append(text)
        names.append(path.stem)
        years.append(int(path.stem.split("_")[1]))

print(len(docs), "speeches")

# %% [markdown]
# ## 1. A document-term matrix

# %%
# Build it with CountVectorizer. How sparse is it?


# %% [markdown]
# ## 2. LDA -- first attempt

# %%
# Five topics. Print the top words of each.


# %%
# What is wrong with these topics? Two things.


# %% [markdown]
# ## 3. Fix the pre-processing

# %%
# Exclude numeric tokens, rebuild, rerun


# %%
# Now try a different random_state. Same topics?


# %% [markdown]
# ## 4. Sentiment on a whole document

# %%
# Short sentences first -- including a negated one


# %%
# Now three whole speeches. What is wrong?


# %% [markdown]
# ## 5. Sentiment by sentence

# %%
# Write sentence_sentiment(), apply it to every speech


# %%
# Which are the least positive? Does that match anything you know?


# %% [markdown]
# ## 6. Sentiment over time

# %%
# Plot it, and correlate with year. Give two explanations.


# %% [markdown]
# End of live coding.
