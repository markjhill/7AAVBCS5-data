# Week 9: spaCy worksheet

Use the module Python environment. Extract the download into the module folder,
merging its `weeks` folder. Keep `weeks/week-09/data` beside the notebooks.

## Start here: the main worksheet

Open `w09_worksheet.ipynb`. It begins with importing spaCy, loading the English
package and creating a Doc from a short string. No personal file is needed at
the beginning.

Sections 1–5 introduce:

1. Create a Doc and inspect its type.
2. Visit individual tokens and read lexical flags.
3. Read lemmas and part-of-speech labels.
4. Inspect named entities and their labels.
5. Build token and entity DataFrames, then use pandas to select and count.

The code is divided into short cells. Run each example, inspect its result,
and complete the small task before continuing. Lists are built with plain
loops; the DataFrame is created afterwards. The introductory exercises do not require lambda expressions,
comprehensions or general-purpose file loaders. The later prepared category
example reuses the lecture corpus-processing cell.

Section 6 uses
the full Horniman Museum and Jazz Cafe articles to compare noun vocabulary,
including percentages with a stated denominator. Prepared examples at the end
of section 6 compare Museum, Theatre and Music venue categories with a word table
and a percentage plot, using the lecture corpus. Section 7 applies the same
steps to one text of your own, using separate CSV and TXT examples.

## Practice afterwards

Open `w09_practice_worksheet.ipynb` after the main worksheet. Six London exercises
cover tokens, linguistic annotations, entities, tables, a different article
comparison, and inspecting a named organisation in context. It has its own setup.

`w09_loops_and_conditionals_worksheet.ipynb` remains available for additional
syntax practice. The two `*_solutions.ipynb` files are separate completed references
and are excluded from the student download.

## Lecture live coding

`w09_live_coding.ipynb` follows the current slides, with stops 01–25 in slide order.
The lecture notebook is unchanged by the worksheet revision. Its completed
reference remains `w09_live_coding_complete.ipynb`.

## Files and Colab

The introductory examples need no files. For section 6 and the practice notebook,
keep the supplied data files, especially `w09_articles.csv`, with the notebook.
The file locator supports the module folder and files uploaded beside a notebook
in Colab. Source URLs, revision IDs and licensing are retained with the article rows.
The larger corpus and review data remain in the download for the lecture.

In Colab, open or upload the notebook. The supplied file locator downloads missing
teaching data from the module's GitHub repository and keeps a local copy for reuse.
If spaCy or its English
model is missing, run these once in separate setup cells before the worksheet:

```python
%pip install spacy
```

```python
!python -m spacy download en_core_web_sm
```

For the local module environment, follow the module installation instructions.
The model is loaded locally; the exercises do not request live Wikipedia pages.

## Further reading

The main guide is the University of Helsinki's Applied Language Technology MOOC:
[Processing texts using spaCy](https://applied-language-technology.mooc.fi/html/notebooks/part_ii/03_basic_nlp.html)
and [Managing textual data using pandas](https://applied-language-technology.mooc.fi/html/notebooks/part_ii/06_managing_data.html).
The official [spaCy course, Chapter 1](https://course.spacy.io/en/chapter1/)
provides supplementary explanations of Docs, Tokens, lexical attributes and annotations.
