# 7AAVBCS5 — teaching datasets

Datasets for **Social and Cultural Analytics (7AAVBCS5)**, King's College London.

This repository exists so that worksheets can load their data over the internet when students are
working in **Google Colab** rather than on their own machine. The teaching material itself lives
in a separate private repository; this holds only the data files.

Files are served over raw HTTPS, e.g.:

```
https://raw.githubusercontent.com/markjhill/7AAVBCS5-data/master/museum_data.csv
```

Worksheets do this automatically — students never type a URL.

## Contents

| File | Rows × cols | Used in | Source and licence |
|---|---|---|---|
| `fruitData.csv` | 5 × 4 | W2–W3 | Constructed for teaching |
| `bananas_apples.csv` | 5 × 3 | W2–W3 | Constructed for teaching |
| `museum_data.csv` | 150 × 8 | W3–W5 | Constructed for teaching |
| `BritishAndIrishNewspapersTitleList_20191118.csv` | 24,927 × 24 | W5 | British Library, British and Irish Newspapers title list. Bibliographic metadata. |
| `London_Cultural_Infrastructure_2023.csv` | — | W5, W7 | Greater London Authority, London Datastore |
| `DawtryEtAl2015.csv` | 305 × 37 | W5, W8 | Dawtry, Sutton & Sibley (2015). Attribute in any published use. |
| `alice.txt` | — | W9–W10 | *Alice's Adventures in Wonderland*, Project Gutenberg. Public domain. |
| `SUA/` | 228 files | W10–W11 | US State of the Union addresses, 1790–2018. Public domain. |
| `LothianDiaries/` | 21 files, 1,035 utterances | W10–W11 | The Lothian Diary Project, University of Edinburgh. Depositors' anonymised public release — see `LothianDiaries/README.md`. |
| `ncv-data-2020-Apr-1.csv` | 1,000 × 7 | W4–W5 | UK government Covid-19 attitudes survey. Public, anonymised. |

All CSVs are UTF-8. The newspapers list was originally cp1252 and has been re-encoded, so no
worksheet needs an `encoding=` argument.

## Human-subjects data published here

Two datasets in this repository are about people rather than objects or texts. Both are already
published openly by their originators, and both are redistributed here **with attribution** so that
Colab can reach them:

- **`LothianDiaries/`** — the Lothian Diary Project's own anonymised public release of Covid-19
  lockdown diary transcripts, University of Edinburgh. Full citation, DOI, papers and licence note
  in [`LothianDiaries/README.md`](LothianDiaries/README.md). Cite the DataShare deposit
  (<https://doi.org/10.7488/ds/3009>), not this repository. Note that speakers introduce themselves
  by **first name** — that is how the depositors published it, but it still matters for any
  named-entity work.
- **`ncv-data-2020-Apr-1.csv`** — UK government Covid-19 attitudes survey microdata (age, gender,
  self-rated knowledge, lockdown compliance, perceived chance of infection). Public and anonymised.
  ⚠️ **The exact source URL still needs adding here** so the attribution is complete.

Everything in this repository is world-readable and effectively permanent. Before adding any further
dataset about people, confirm it is already openly published by its originator; if it is not, it
belongs on KEATS behind authentication instead.

## Rebuilding

Generated from the module's Moodle backup by `scripts/convert_datasets.py` in the main repository.
Do not hand-edit; regenerate instead.
