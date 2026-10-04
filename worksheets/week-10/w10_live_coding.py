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
# # Week 10 — live coding
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# The cells are **deliberately empty**.

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

# %% [markdown]
# ## 1. Annotate a sentence

# %%
# Tokenise a sentence with spaCy. Compare with .split().


# %% [markdown]
# ## 2. Tokens, lemmas, parts of speech into a data frame

# %%
# Build a data frame of token, lemma, pos, is_stop


# %% [markdown]
# ## 3. A whole book

# %%
# Load alice.txt, annotate the first 200,000 characters


# %%
# Tokens and types


# %%
# Top words WITHOUT removing stop words


# %%
# Top lemmas WITH stop words removed


# %%
# How much did we just remove? And what was in it?


# %% [markdown]
# ## 4. Named entities

# %%
# Entities in a test sentence, then the top PERSON entities in Alice


# %% [markdown]
# ## 5. The whole corpus

# %%
# Loop over the first 10 speeches, collecting tokens and types


# %% [markdown]
# End of live coding.
