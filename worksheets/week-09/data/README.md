# Week 9 teaching data

These files run locally with the slides and notebooks. Text is supplied as text:
we tokenise it, choose which words to count, and calculate sentiment in Python.
Original source datasets are unchanged.

## Files used in the lecture and worksheets

| File | Rows | What one row represents |
|---|---:|---|
| `w09_corpus.csv.gz` | 439 | One Wikipedia article: `doc_id`, `title`, `category`, `borough`, heading-stripped `text`. Used for corpus, article and category word comparisons. pandas reads the gzip-compressed CSV directly. |
| `w09_articles.csv` | 3 | Roundhouse, Jazz Cafe or Horniman Museum. Includes article identity, venue links, URL, revision, licence, original and heading-stripped text, and opening sentence. Used in the worksheets. |
| `w09_review_scores.csv` | 468 | One museum review: venue name, star rating, date, translation flag and original wording. Despite the filename, it contains **no sentiment scores**: VADER calculates them in the lecture. |

The lecture corpus contains 166 Museum, 174 Theatre and 99 Music venue articles.
It includes all pages in the current full source corpus: 412 `own`, one
`own;related` and 26 `related`-only pages. An article is not necessarily about one
individual venue. Shared articles appear once, even when linked to several venues.

`category` is a single teaching label assigned from the source's category links:
Museum takes priority, then Theatre, then Music venue. It does not imply that a
venue has only one function. `borough` is the first listed source borough;
multi-site articles can concern several boroughs. These choices matter when
interpreting category or spatial comparisons.

## Supplementary prepared tables

These are retained for further exploration. They are not required by the current
lecture demonstrations and do not imply a collocation task in the worksheet.

| File | Rows | Row unit and scope |
|---|---:|---|
| `w09_article_terms.csv` | 12 | Selected article–lemma counts, with the retained-token denominator for each complete article. |
| `w09_prevalence.csv` | 3 | Selected surface forms and document prevalence among **413 own-match articles**, rather than the full lecture cohort. |
| `w09_collocations.csv` | 27 | Selected adjacent pairs from the same 413-article cohort: frequent pairs, high-PMI pairs and selected candidates. Not exhaustive. |
| `w09_concordances.csv` | 19 | Selected sentences with article identity, revision and licence. `query_kind` distinguishes single surface forms from adjacent pairs. Not all occurrences. |
| `w09_reviews.csv` | 3 | Deliberately selected short museum reviews with venue linkage, date, rating, translation flag and source attribution. Not representative. |

## Sources and attribution

**Articles:** Wikipedia contributors, English Wikipedia, CC BY-SA 4.0. The
current `data/wikipedia/wikipedia_corpus_full.jsonl` and
`venue_wikipedia_matches_full.csv` are the sources; the old run-2 snapshot is
not used. `doc_id = wiki_{pageid}` joins each teaching article to the source
JSONL, which retains URL, revision, venue links and licence. For the three
worksheet articles, these fields also travel in `w09_articles.csv`.

Section-heading lines are removed from the prepared `text`. `text_original` in
the three-article table preserves the complete source text. Wikipedia descriptions
are not visitor evaluations or a representative census of London culture.

**Reviews:** *Global Museum Visitor Reviews Dataset (Textual Insights from Google
Reviews)*, version 2, [DOI 10.5281/zenodo.16752356](https://doi.org/10.5281/zenodo.16752356),
deposit licence CC BY 4.0. The 468 reviews cover five matched London venues in
2023–24: the British Museum, National Gallery, Royal Academy of Arts, Tate Modern
and Victoria and Albert Museum. All have star ratings from 1 to 5. Wording and
spelling are unchanged. Attribution is to the deposit; underlying opinions are
third-party visitor text, not statements by KCL. Translation flags are preserved
without treating them as guarantees of language or originality. These are not a
representative sample of London visitors. IDs in the three-review extract are
teaching text hashes, not source-provided unique review identifiers.

## Counting rules

- **Lecture frequencies and percentages:** `nlp.tokenizer`; alphabetic tokens;
  exclude spaCy stop words; lowercase surface forms (`token.lower_`), **not
  lemmas**. `collection` and `collections` remain separate. Category percentages
  divide by all retained word occurrences in that category, not its articles or
  venues. Longer articles contribute more words.
- **Prepared article–term counts:** alphabetic tokens; exclude spaCy stop words;
  lowercase **lemmas**; names retained. Denominator: retained tokens in the same
  complete article. Opening-sentence exercises use less text and have different counts.
- **Prepared prevalence:** percentage of the 413 own-match articles containing
  a selected lowercase alphabetic surface form. The table supplies the denominator.
- **Prepared collocations:** adjacent alphabetic surface tokens within original
  sentences/documents, lowercased. Punctuation interrupts adjacency. Stop words
  are not removed before extraction, so gaps are not closed. Require at least
  five occurrences in at least three articles. Stop-word components are hidden
  only when selecting displayed candidates, after counting.
- **PMI:** base-2 log of observed pair probability divided by the product of
  left/right marginal probabilities, measured on the same eligible pair slots.
  Association is not a significance test or evidence of cultural meaning by itself.
- **Sentiment:** retain original review wording, case, punctuation and negation.
  Calculate whole-review VADER compound scores and compare with star ratings.
  Do not apply the word-frequency filtering before scoring.

Concordances include an `excerpt` for readable display, with ellipses marking
cuts. `sentence` retains the complete context for interpretation. Source text is
data to inspect, never instructions to execute.

## Reproduction and integrity

`provenance.json` records source hashes, model versions, cohort definitions and
each table's row count, columns and SHA-256 hash. It distinguishes the lecture's
439-article surface-word analysis from the 413-article supplementary summaries.

To rebuild **only the teaching data and provenance**, without rewriting slides
or notebooks, run from the project root in the teaching environment:

```bash
python scripts/build_week09_notebooks.py --data-only
```

The supplementary summaries are reproduced from `weeks/week-09/lecture_examples.json`,
whose source hashes are checked first. If those source files change, recompute
and review the prepared summaries before rebuilding. Data preparation is not an
additional student requirement.
