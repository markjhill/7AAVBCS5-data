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
# # Week 9 — live coding
#
# **Social and Cultural Analytics (7AAVBCS5)**
#
# The cells are **deliberately empty** — they get filled in during the lecture.

# %%
import subprocess
from pathlib import Path

import pandas as pd


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


SUA = data_path("SUA")

# %% [markdown]
# ## 1. A function

# %%
def calculate_percentage(part, total):
    """Return part as a percentage of total."""
    return part / total * 100


print(calculate_percentage(25, 100))

# %%
def add_bad(a, b):
    a + b


def add_good(a, b):
    return a + b


print("no return:", add_bad(2, 3))
print("with return:", add_good(2, 3))

# %% [markdown]
# ## 2. An if statement

# %%
grade = 62

if grade >= 50:
    print("Pass")
else:
    print("Fail")

# %% [markdown]
# ## 3. A for loop

# %%
followers = [1000, 2500, 500, 3200, 1500]

for count in followers:
    print(count)

# %%
doubled = []
for count in followers:
    doubled.append(count * 2)

print(doubled)

# %% [markdown]
# ## 4. A while loop

# %%
countdown = 5
while countdown > 0:
    print(countdown)
    countdown = countdown - 1

print("Lift off")

# %% [markdown]
# ## 5. Putting it together: a folder of texts

# %%
files = sorted(SUA.glob("*.txt"))
print(len(files), "State of the Union addresses")

for path in files[:3]:
    text = path.read_text(encoding="utf-8", errors="replace")
    print(f"{path.name:26} {len(text):>8,} characters")

# %%
def word_count(text):
    """Count whitespace-separated words."""
    return len(text.split())


rows = []
for path in files:
    text = path.read_text(encoding="utf-8", errors="replace")
    president, year = path.stem.split("_")
    rows.append({
        "file": path.name,
        "president": president,
        "year": int(year),
        "characters": len(text),
        "words": word_count(text),
    })

speeches = pd.DataFrame(rows)
print(speeches.shape)
speeches.head()

# %%
print("mean words:", round(speeches["words"].mean()))
print()
print(speeches["president"].value_counts().head(5).to_string())

# %%
print(speeches[speeches["characters"] == 0])

# %% [markdown]
# End of live coding.
