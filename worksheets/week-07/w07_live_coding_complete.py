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
# # Week 7 — live coding
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
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
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


news = pd.read_csv(data_path("BritishAndIrishNewspapersTitleList_20191118.csv"),
                   low_memory=False)
print(news.shape)

# %% [markdown]
# ## 1. A bar plot, and making it readable

# %%
countries_top = news["country_of_publication"].value_counts().head(5)
print(countries_top)

# %%
countries_top.plot(kind="bar")
plt.show()

# %%
fig, ax = plt.subplots(figsize=(7, 3))
countries_top.plot(kind="bar", ax=ax, rot=0, color="steelblue")
ax.set_title("Newspaper Publications by Country")
ax.set_xlabel("Country")
ax.set_ylabel("Number of Newspapers")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 2. From crosstab to chart

# %%
top5 = ["England", "Scotland", "Ireland", "Wales", "Northern Ireland"]
subset = news[news["country_of_publication"].isin(top5)
              & news["current_publication_frequency"].isin(["Weekly", "Daily", "Monthly"])]

countries_pf = pd.crosstab(subset["current_publication_frequency"],
                           subset["country_of_publication"])
countries_pf

# %%
missing = news["current_publication_frequency"].isna().sum()
print(f"frequency missing for {missing} of {len(news)} titles "
      f"({news['current_publication_frequency'].isna().mean() * 100:.1f}%)")

# %%
# Stacked -- note the .T. pandas plots one bar per ROW, so the table has to be transposed.
fig, ax = plt.subplots(figsize=(7, 3))
countries_pf.T.plot(kind="bar", stacked=True, ax=ax, rot=0)
ax.set_title("Stacked: totals per country")
plt.tight_layout()
plt.show()

# %%
# Grouped -- in pandas this is the default; R needed beside = TRUE.
fig, ax = plt.subplots(figsize=(7, 3))
countries_pf.T.plot(kind="bar", ax=ax, rot=0)
ax.set_title("Grouped: every bar starts at zero")
plt.tight_layout()
plt.show()

# %%
# Proportional -- normalize="columns", the same argument as Week 5.
props = pd.crosstab(subset["current_publication_frequency"],
                    subset["country_of_publication"], normalize="columns")
fig, ax = plt.subplots(figsize=(7, 3))
props.T.plot(kind="bar", stacked=True, ax=ax, rot=0)
ax.set_ylabel("proportion")
ax.set_title("Proportional: every bar reaches 1.0")
plt.tight_layout()
plt.show()

# %% [markdown]
# Which chart supports which argument?

# %% [markdown]
# ## 3. Distributions: newspaper lifespans

# %%
pub = news.dropna(subset=["publication_date_one", "publication_date_two"]).copy()
pub["length"] = pub["publication_date_two"] - pub["publication_date_one"]

print("titles with both dates:", len(pub))
print("mean  ", round(pub["length"].mean(), 4))
print("median", pub["length"].median())
print("min   ", pub["length"].min(), " max", pub["length"].max())

# %%
print(pub["length"].describe().round(2).to_string())

# %%
print("lasted 0 years:", (pub["length"] == 0).sum())
print("over 100 years:", (pub["length"] > 100).sum())

# %% [markdown]
# ## 4. Histograms

# %%
fig, ax = plt.subplots(figsize=(7, 3))
pub["length"].plot(kind="hist", ax=ax, bins=30, color="steelblue", edgecolor="white")
ax.set_xlabel("Years in publication")
plt.tight_layout()
plt.show()

# %%
fig, axes = plt.subplots(1, 3, figsize=(11, 2.8))
for ax, bins in zip(axes, [3, 30, 500]):
    pub["length"].plot(kind="hist", ax=ax, bins=bins, color="steelblue")
    ax.set_title(f"{bins} bins", fontsize=9)
    ax.set_ylabel("")
plt.tight_layout()
plt.show()

# %%
fig, ax = plt.subplots(figsize=(7, 3.2))
pub["length"].plot(kind="hist", ax=ax, bins=50, color="steelblue", edgecolor="white")
ax.axvline(pub["length"].median(), color="red", linestyle="--", linewidth=2,
           label=f"median = {pub['length'].median():.0f}")
ax.axvline(pub["length"].mean(), color="blue", linestyle="--", linewidth=2,
           label=f"mean = {pub['length'].mean():.1f}")
ax.set_xlabel("Years in publication")
ax.legend()
plt.tight_layout()
plt.show()

# %%
# Who is the outlier?
print(pub.loc[pub["length"].idxmax(),
              ["publication_title", "publication_date_one",
               "publication_date_two", "length"]].to_string())

# %% [markdown]
# ## 5. How easy it is to mislead

# %%
example = pd.Series([1020, 1035], index=["2024", "2025"])

fig, axes = plt.subplots(1, 2, figsize=(9, 3))
example.plot(kind="bar", ax=axes[0], rot=0, color="steelblue")
axes[0].set_title("y-axis from 0", fontsize=10)

example.plot(kind="bar", ax=axes[1], rot=0, color="steelblue")
axes[1].set_ylim(1000, 1040)
axes[1].set_title("y-axis from 1000", fontsize=10)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 6. Saving a figure

# %%
Path("figures").mkdir(exist_ok=True)

fig, ax = plt.subplots(figsize=(8, 5))
pub["length"].plot(kind="hist", ax=ax, bins=50, color="steelblue", edgecolor="white")
ax.axvline(pub["length"].median(), color="red", linestyle="--", linewidth=2, label="median")
ax.set_title("Distribution of British & Irish newspaper lifespans")
ax.set_xlabel("Years in publication")
ax.set_ylabel("Number of newspapers")
ax.legend()

fig.savefig("figures/newspaper_lifespan_hist.png", dpi=150, bbox_inches="tight")
fig.savefig("figures/newspaper_lifespan_hist.pdf", bbox_inches="tight")
plt.close(fig)

for f in sorted(Path("figures").iterdir()):
    print(f.name, f"{f.stat().st_size / 1024:,.0f} KB")

# %% [markdown]
# End of live coding.
