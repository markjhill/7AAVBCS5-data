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
doc = nlp("Alice wasn't expecting the White Rabbit's waistcoat-pocket.")
print("spaCy:", [t.text for t in doc])
print("split:", "Alice wasn't expecting the White Rabbit's waistcoat-pocket.".split())

# %% [markdown]
# ## 2. Tokens, lemmas, parts of speech into a data frame

# %%
doc = nlp("The rabbits were running and had run before the Queen painted the roses red.")
tokens = pd.DataFrame([
    {"token": t.text, "lemma": t.lemma_, "pos": t.pos_, "is_stop": t.is_stop}
    for t in doc if t.is_alpha
])
tokens

# %% [markdown]
# ## 3. A whole book

# %%
alice = (data_path("alice.txt")).read_text(encoding="utf-8", errors="replace")
doc = nlp(alice[:200_000])
print(len(doc), "tokens")

words = pd.Series([t.text.lower() for t in doc if t.is_alpha])
print("tokens:", len(words), "| types:", words.nunique())

# %%
print(words.value_counts().head(8).to_string())

# %%
content = pd.Series([t.lemma_.lower() for t in doc if t.is_alpha and not t.is_stop])
print(content.value_counts().head(8).to_string())

# %%
alpha = [t for t in doc if t.is_alpha]
stops = [t for t in alpha if t.is_stop]
print(f"{len(stops):,} of {len(alpha):,} tokens are stop words = {100*len(stops)/len(alpha):.1f}%")
print()
print(pd.Series([t.text.lower() for t in stops]).value_counts().head(10).to_string())

# %%
print([(e.text, e.label_) for e in nlp("President Wilson addressed Congress in 1917.").ents])

# %% [markdown]
# ## 4. Named entities

# %%
people = pd.Series([e.text for e in doc.ents if e.label_ == "PERSON"])
print(people.value_counts().head(6).to_string())

# %% [markdown]
# ## 5. The whole corpus

# %%
files = sorted((data_path("SUA")).glob("*.txt"))
rows = []
for path in files[:10]:
    text = path.read_text(encoding="utf-8", errors="replace")
    president, year = path.stem.split("_")
    if not text.strip():
        rows.append({"file": path.name, "year": int(year), "tokens": 0, "types": 0})
        continue
    d = nlp(text)
    w = [t.text.lower() for t in d if t.is_alpha]
    rows.append({"file": path.name, "year": int(year), "tokens": len(w), "types": len(set(w))})

pd.DataFrame(rows)

# %% [markdown]
# End of live coding.
