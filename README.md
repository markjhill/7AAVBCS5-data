# 7AAVBCS5 — public teaching materials and datasets

Public student materials and datasets for **Social and Cultural Analytics (7AAVBCS5)**,
King's College London.

This repository exists so that students can access the weekly worksheets and the data they need
from one public location. It also lets worksheets load their data over the internet when students
are working in **Google Colab** rather than on their own machine.

The private teaching repository still holds staff-only material such as solutions, assessment
notes, quizzes, speaker notes and release planning. This public repository contains only the files
that students should be able to access directly.

Files are served over raw HTTPS, e.g.:

```
https://raw.githubusercontent.com/markjhill/7AAVBCS5-data/master/museum_data.csv
```

Worksheets do this automatically — students never type a URL.

## Worksheets

Student-facing worksheets and live-coding files are organised by week:

```
worksheets/week-01/
worksheets/week-02/
...
worksheets/week-11/
```

Each weekly folder contains notebook versions (`.ipynb`) where available. Live-coding complete
versions are included, because they are useful for review after class. Worksheet solutions are
intentionally not included here; those are released separately through Moodle when appropriate.

## Lecture slides

Student-facing slides are organised by week:

```
lecture_slides/week-01/slides.html
lecture_slides/week-01/slides.pdf
lecture_slides/week-02/slides.html
lecture_slides/week-02/slides.pdf
...
```

The HTML and PDF files are generated from the private teaching repository's QMD source with speaker
notes stripped. Do not hand-edit slide files here; regenerate them from the private repository so
there is only one source version.

## Data files

| File | Rows × cols | Used in | Source and licence |
|---|---|---|---|
| `fruitData.csv` | 5 × 4 | W2–W3 | Constructed for teaching |
| `bananas_apples.csv` | 5 × 3 | W2–W3 | Constructed for teaching |
| `museum_data.csv` | 150 × 8 | W3–W5 | Constructed for teaching |
| `BritishAndIrishNewspapersTitleList_20191118.csv` | 24,927 × 24 | W5 | British Library, British and Irish Newspapers title list. Bibliographic metadata. |
| `London_Cultural_Infrastructure_2023.csv` | — | W5, W7 | Greater London Authority, London Datastore |
| `london_cultural_venues_2023.csv` | 4,434 × 20 | W3–W8 | Greater London Authority, London Datastore. Cleaned venue-level teaching copy. |
| `london_cultural_infrastructure_2023_borough_counts.csv` | 33 × 6 | W3–W8 | Aggregated from `london_cultural_venues_2023.csv`. |
| `london_cultural_infrastructure_2023_borough_type_counts.csv` | 652 × 4 | W3–W8 | Aggregated from `london_cultural_venues_2023.csv`. |
| `london_borough_profiles_2015.csv` | 33 × 13 | W3–W8 | Borough-level contextual indicators from the GLA ward profiles file. |
| `london_cultural_infrastructure_2023_borough_context.csv` | 33 × 20 | W3–W8 | Borough venue counts joined to contextual indicators. |
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

## Maintenance

The private teaching repository pins this public repository at a specific Git commit, so Moodle
materials and worksheets can point to a known version of the student-facing files. When public
worksheets or data files change, commit those changes here first, then update the pinned reference
from the private repository.
