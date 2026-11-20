# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Week 9 — text analysis
#
# How do preprocessing decisions change what we can count and interpret in a text?

# %% [markdown]
# ## Setup
#
# Extract the download and keep its `data` folder beside this notebook. In Colab,
# the supplied file locator downloads missing teaching files from GitHub automatically.
# Run the two setup cells, then work through the examples in
# order. Keep the original text and source identifiers alongside derived measures;
# `data/README.md` documents the sources and counting rules.

# %% tags=["provided-setup"]
# PROVIDED ENVIRONMENT CHECK: run before teaching.
from pathlib import Path
import importlib.util
import subprocess
import sys
for package, requirement in (("pandas", "pandas"), ("matplotlib", "matplotlib"), ("spacy", "spacy"),
                             ("scipy", "scipy"), ("vaderSentiment", "vaderSentiment==3.3.2")):
    if importlib.util.find_spec(package) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", requirement])
if importlib.util.find_spec("en_core_web_sm") is None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",
        "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl"])
# Imports, data reads and model loading are shown explicitly in the stops.

# %% tags=["provided-setup"]
# PROVIDED FILE LOCATOR: use local teaching files or download them from GitHub.
from pathlib import Path
from urllib.request import urlopen
def teaching_file(name):
    for parent in (Path.cwd(), *Path.cwd().parents):
        for candidate in (parent / "data" / name,
                          parent / "weeks/week-09/data" / name,
                          parent / "worksheets/week-09/data" / name, parent / name):
            if candidate.is_file():
                return candidate
    url = ("https://raw.githubusercontent.com/markjhill/7AAVBCS5-data/main/"
           "worksheets/week-09/data/" + name)
    print(f"Downloading {name} from the module GitHub repository...")
    with urlopen(url, timeout=60) as response:
        content = response.read()
    target = Path.cwd() / "data" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    return target


# %% [markdown]
# ## Jump to a demonstration
#
# | Stop | Slide | Demonstration | Action |
# |---|---|---|---|
# | 01 | 9 | Introducing spaCy I | prepared |
# | 02 | 10 | Introducing spaCy II | prepared |
# | 03 | 13 | Tokenisation in Python | write-live |
# | 04 | 14 | Inspect one token | prepared |
# | 05 | 15 | Visit each token with a for loop | prepared |
# | 06 | 20 | Pre-processing: punctuation removal | write-live |
# | 07 | 22 | Lower-casing in Python | write-live |
# | 08 | 23 | Pre-processing: stop-word removal | edit-live |
# | 09 | 24 | Pre-processing: spelling standardisation | edit-live |
# | 10 | 26 | Collect token information into rows | prepared |
# | 11 | 27 | Turn the collected rows into a DataFrame | prepared |
# | 12 | 30 | Lemmatisation changes the representation | prepared |
# | 13 | 31 | Now with stopwords removed | prepared |
# | 14 | 33 | Morphological tagging | prepared |
# | 15 | 35 | Part-of-speech (POS) tagging | prepared |
# | 16 | 43 | Technique 1 · Load the data | prepared |
# | 17 | 44 | Technique 2 · Tokenise each article | prepared |
# | 18 | 45 | Technique 2 · One row per token | prepared |
# | 19 | 46 | Technique 2 · Choose the words to count | prepared |
# | 20 | 47 | Technique 3 · Most frequent across the corpus | prepared |
# | 21 | 48 | Technique 4 · Most frequent in one article | prepared |
# | 22 | 49 | Technique 5 · Most frequent by group | prepared |
# | 23 | 50 | Technique 6 · Top words as a proportion | prepared |
# | 24 | 52 | Technique 7 · Score sentiment across the reviews | prepared |
# | 25 | 53 | Technique 8 · Stars vs sentiment score | prepared |

# %% [markdown]
# # Part II: The NLP pipeline

# %% [markdown]
# ## 01. Introducing spaCy I
#
# **Slide 9 · prepared**
#
# **spaCy is a Python library for working with human language.** It identifies
# words and punctuation, and supplies information about them for text analysis.
#
# spaCy provides the tools. We also load an **English language package** containing
# language rules and models trained on example texts. We can use these without
# training a model ourselves.
#
# `import spacy` makes the library available. `spacy.load("en_core_web_sm")` loads
# an installed English package: `en` = English, `core` = general linguistic features,
# `web` = written web texts, `sm` = small. [Package details](https://spacy.io/models/en#en_core_web_sm).
#
# We call the loaded processor `nlp`. `nlp(weather_text)` analyses our sentence;
# `weather_doc` holds the text and results together. `type()` shows that this is a
# spaCy `Doc`, rather than a string; `len()` counts its tokens, including punctuation.

# %% part="Part II: The NLP pipeline" slide_number=9 slide_title="Introducing spaCy I" source_label="live-01" tags=["prepared"]
import spacy
nlp = spacy.load("en_core_web_sm")
weather_text = ("This morning there were clouds in the sky. However, the weather improved in the afternoon!")
weather_doc = nlp(weather_text)
print(type(weather_text))
print(type(weather_doc))
print(len(weather_doc))

# %% [markdown]
# ## 02. Introducing spaCy II
#
# **Slide 10 · prepared**
#
# What's in a spaCy object? Lots!

# %% part="Part II: The NLP pipeline" slide_number=10 slide_title="Introducing spaCy II" source_label="live-02" tags=["prepared"]
import pandas as pd
weather_df = pd.DataFrame(weather_doc.to_json()["tokens"])
weather_df

# %% [markdown]
# ## 03. Tokenisation in Python
#
# **Slide 13 · write-live**
#
# spaCy has already tokenised our text. Here we inspect its token boundaries
# and count occurrences and distinct forms in the short example.
#
# spaCy treats `!` as a token. `len(token_doc)` counts occurrences; `pd.Series(token_texts).nunique()` counts distinct text forms, including punctuation.
#
# **Note**: we're using a for loop here! More on these shortly.

# %% part="Part II: The NLP pipeline" slide_number=13 slide_title="Tokenisation in Python" source_label="live-03" tags=["write-live"]
import pandas as pd
text = "I go where I want to go!" # Note the ! and what it does to our counts
token_doc = nlp(text)
token_texts = []
for token in token_doc:
    token_texts.append(token.text)
print(token_texts)
print("Tokens:", len(token_doc))
print("Types:", pd.Series(token_texts).nunique())

# %% [markdown]
# ## 04. Inspect one token
#
# **Slide 14 · prepared**
#
# Each indexed item in a spaCy object (`Doc`) is a `Token`, along with a huge number of  attributes attached to it.
#
# `weather_doc[0]` selects the first token; `weather_doc[-1]` selects the last.
# `text` gives its text. The other attributes return `True` or `False`:
# letters only, digits only, number-like, punctuation, or membership of a stop list.
# More attributes include `lower_`, `is_space`, `like_url` and `like_email`:
# [spaCy Token reference](https://spacy.io/api/token#attributes).

# %% part="Part II: The NLP pipeline" slide_number=14 slide_title="Inspect one token" source_label="live-04" tags=["prepared"]
token = weather_doc[0]
print(type(token))
print("Text:", token.text)
print("Alphabetic:", token.is_alpha)
print("Digits:", token.is_digit)
print("Number-like:", token.like_num)
print("Punctuation:", token.is_punct)
print("Stopword:", token.is_stop)

# %% [markdown]
# ## 05. Visit each token with a for loop
#
# **Slide 15 · prepared**
#
# What is we want to look at more than one token? This is where loops can be useful.
#
# Instead of writing a separate index for every position a `for` loop repeats the indented instruction for each item in the document.
#
# `for token in weather_doc:` takes one token at a time from weather_doc and assigns it to `token`. The colon starts the loop body. Indentation puts `print(token.text)` inside the loop, so it runs once for each token. `token` is a variable name we choose.

# %% part="Part II: The NLP pipeline" slide_number=15 slide_title="Visit each token with a for loop" source_label="live-05" tags=["prepared"]
for token in weather_doc:
    print(token.text)

# %% [markdown]
# ## 06. Pre-processing: punctuation removal
#
# **Slide 20 · write-live**
#
# Remove punctuation when it does not carry information needed for the research
# question or method. spaCy has already identified punctuation tokens with
# `token.is_punct`; we can choose which tokens to retain.
#
# Punctuation can mark sentence boundaries, emphasis, and style. Keep it when those features matter (e.g., preserving apostrophes avoids erasing them from contractions such as "can't").
#
#
# `for every_token_in_weather_doc in weather_doc:` visits one token at a time. The colon and indentation mark the instructions to repeat. `if not token.is_punct:` keeps tokens whose punctuation flag is `False`. `.append(token.text)` adds their text to the list; the unindented `print()` runs once, after the loop.

# %% part="Part II: The NLP pipeline" slide_number=20 slide_title="Pre-processing: punctuation removal" source_label="live-06" tags=["write-live"]
print(weather_doc)
print("")
print(f"Is the 8th token, '{weather_doc[7]}', punctuation? {weather_doc[7].is_punct}")
print(f"Is the 9th token, '{weather_doc[8]}', punctuation? {weather_doc[8].is_punct}")
print("")
words_without_punctuation = []
for every_token_in_weather_doc in weather_doc:   
    if not every_token_in_weather_doc.is_punct:
        words_without_punctuation.append(every_token_in_weather_doc.text)
print(words_without_punctuation)

# %% [markdown]
# ## 07. Lower-casing in Python
#
# **Slide 22 · write-live**
#
# `token.lower_` supplies a lowercase form alongside the original token text.
#
# The first token is `This`; its lowercase form is `this`. The original text
# remains available. Use the lowercase form when combining case serves the question.
#
#
# `weather_doc[0]` selects the first token. `.text` gives its original form;
# `.lower_` gives its lowercase form. These are attributes, so we do not add `()`.

# %% part="Part II: The NLP pipeline" slide_number=22 slide_title="Lower-casing in Python" source_label="live-07" tags=["write-live"]
token = weather_doc[0]
print(token.text)
print(token.lower_)

# %% [markdown]
# ## 08. Pre-processing: stop-word removal
#
# **Slide 23 · edit-live**
#
# Stop-words are very common words, often function words. These include things like "and", "the", "this", "that", "a", etc.. They are **by far** the most common words in most (every?) language.
#
# We often remove them so that we can focus a _thematic_ words. However, this could also also remove stylistic and grammatical evidence if important.
#
# `token.is_stop` checks membership of spaCy's English stop list. `not` reverses
# the test; `and` requires both tests to pass. This keeps tokens flagged as neither
# stopwords nor punctuation. Tokenisation has already happened inside `nlp()`.

# %% part="Part II: The NLP pipeline" slide_number=23 slide_title="Pre-processing: stop-word removal" source_label="live-08" tags=["edit-live"]
content_words = []
for token in weather_doc:
    if not token.is_stop and not token.is_punct:
        content_words.append(token.text)
print(content_words)

# %% [markdown]
# ## 09. Pre-processing: spelling standardisation
#
# **Slide 24 · edit-live**
#
# Variant spellings, typos, and elongated forms can, again, divide or inflate counts across different written forms: for example, `colour` and its mispelled variation `color`.
#
# Domain-specific dictionaries and tools can help. Historical spelling, dialect
# and informal language may be evidence, so preserve the original and justify the rule.

# %% part="Part II: The NLP pipeline" slide_number=24 slide_title="Pre-processing: spelling standardisation" source_label="live-09" tags=["edit-live"]
import re
variant_text = "colour and color"
standardised = re.sub(r"\bcolor\b", "colour", variant_text)
print(standardised)

# %% [markdown]
# ## 10. Collect token information into rows
#
# **Slide 26 · prepared**
#
# Start with an empty list. For each token, create one dictionary and append it
# to the list. Keep every token for now, including punctuation and stopwords.
#
# `[]` creates an empty list. A dictionary pairs each column name with a value.
# `weather_rows.append(row)` adds that dictionary to the list. Both indented
# statements repeat; the unindented `print()` calls run after the loop finishes.

# %% part="Part II: The NLP pipeline" slide_number=26 slide_title="Collect token information into rows" source_label="live-10" tags=["prepared"]
weather_rows = []
for token in weather_doc:
    row = {
        "text": token.text,
        "is_alpha": token.is_alpha,
        "is_digit": token.is_digit,
        "is_punct": token.is_punct,
        "is_stop": token.is_stop,
    }
    weather_rows.append(row)

print("Rows collected:", len(weather_rows))
print(weather_rows[0])

# %% [markdown]
# ## 11. Turn the collected rows into a DataFrame
#
# **Slide 27 · prepared**
#
# The loop has finished. pandas can now turn our list of dictionaries into a
# familiar table: one row per token and one column per attribute we selected.
#
# `pd.DataFrame(weather_rows)` uses the list as its input. Dictionary keys become
# column names and their values fill the rows. `.head(6)` selects the first six
# rows for display; it does not shorten the saved DataFrame.
# `display(...)` shows the resulting table in the notebook or slides.

# %% part="Part II: The NLP pipeline" slide_number=27 slide_title="Turn the collected rows into a DataFrame" source_label="live-11" tags=["prepared"]
import pandas as pd
weather_tokens = pd.DataFrame(weather_rows)
display(weather_tokens.head(6))

# %% [markdown]
# ## 12. Lemmatisation changes the representation
#
# **Slide 30 · prepared**
#
# **Original:** “This morning there were clouds in the sky but the weather improved in the afternoon.”
#
# `token.lemma_` gives spaCy's proposed base form as text. The loop displays each
# original token beside its lemma. These results were produced when we ran
# `nlp(weather_text)`; accessing them does not change the original sentence.

# %% part="Part II: The NLP pipeline" slide_number=30 slide_title="Lemmatisation changes the representation" source_label="live-12" tags=["prepared"]
for token in weather_doc:
    print(token.text, "=", token.lemma_)

# %% [markdown]
# ## 13. Now with stopwords removed
#
# **Slide 31 · prepared**
#
# **Original:**
#
# “This morning there were clouds in the sky but the weather improved in the afternoon.”
#
# **Combine the lemma and stopword information:**
#
# **Is there still meaning?** 
#
# Combining lemmas and a stop-word filter keeps selected vocabulary while
# removing tense, grammatical links, and the contrast marked by `but`.
#
# I think many of us would struggle to decipher this.
#
#
# ![](images/odp/original-32-1.png){height=210 fig-alt="A bag labelled words, retained from the original lecture"}

# %% part="Part II: The NLP pipeline" slide_number=31 slide_title="Now with stopwords removed" source_label="live-13" tags=["prepared"]
lemmas = []
for token in weather_doc:
    if not token.is_stop and not token.is_punct:
        lemmas.append(token.lemma_)
print(lemmas)

# %% [markdown]
# ## 14. Morphological tagging
#
# **Slide 33 · prepared**
#
# Morphological annotation describes grammatical features such as tense, number, gender, case, or degree. It records information beyond the surface form.
#
# - `walked` → verb, past tense
# - `dogs` → noun, plural
# - `better` → adjective, comparative (in an appropriate sentence)
#
# Inspect two forms in our actual weather sentence:
#
# `morph` contains the pipeline's _predicted_ features - this comes from the model we loaded at the start.

# %% part="Part II: The NLP pipeline" slide_number=33 slide_title="Morphological tagging" source_label="live-14" tags=["prepared"]
print(weather_doc[3].text, "is", weather_doc[3].morph)
print(weather_doc[4].text, "is", weather_doc[4].morph)

# %% [markdown]
# ## 15. Part-of-speech (POS) tagging
#
# **Slide 35 · prepared**
#
# Assign a token its grammatical category according to its use in the sentence.
# The same form can have different functions. E.g., `run` in “a 5k run” and “I run daily”.
#
# POS needs the sentence to construct context. It doesn't assign an isolated word a permanent category.

# %% part="Part II: The NLP pipeline" slide_number=35 slide_title="Part-of-speech (POS) tagging" source_label="live-15" tags=["prepared"]
noun_doc = nlp("I bought a book.")
verb_doc = nlp("I will book a ticket.")

print(noun_doc[3].text, noun_doc[3].pos_)
print(verb_doc[2].text, verb_doc[2].pos_)

# %% [markdown]
# # Part III: Counting words

# %% [markdown]
# ## 16. Technique 1 · Load the data
#
# **Slide 43 · prepared**
#
# Load a table of texts from a file. Your own data loads the same way — a column of a
# CSV, or a text file.
#
# `read_csv` loads any CSV; swap the path for your own file. Each row here is one
# Wikipedia article, with its text, category and borough.

# %% part="Part III: Counting words" slide_number=43 slide_title="Technique 1 \u00b7 Load the data" source_label="live-16" tags=["prepared"]
import pandas as pd
corpus = pd.read_csv(teaching_file("w09_corpus.csv.gz"))
display(corpus[["title", "category", "borough"]].head())
print("First article begins:", corpus["text"].iloc[0][:150])
# your own data loads the same way:
# corpus = pd.read_csv("my_reviews.csv")               # a CSV with a text column
# text   = open("my_notes.txt", encoding="utf-8").read()   # a single text file

# %% [markdown]
# ## 17. Technique 2 · Tokenise each article
#
# **Slide 44 · prepared**
#
# Repeat the tokenisation for every article. Keep each article's tokens in a list.
#
# `nlp.tokenizer(text)` splits one text into tokens. `list(doc)` puts its tokens in
# a list; `.append()` adds that list to `article_tokens`.

# %% part="Part III: Counting words" slide_number=44 slide_title="Technique 2 \u00b7 Tokenise each article" source_label="live-17" tags=["prepared"]
article_tokens = []
for text in corpus["text"]:
    doc = nlp.tokenizer(text)
    article_tokens.append(list(doc))
corpus["token"] = article_tokens
display(corpus[["title", "token"]].head(2))

# %% [markdown]
# ## 18. Technique 2 · One row per token
#
# **Slide 45 · prepared**
#
# Unpack the lists so we can count tokens in a familiar table.
#
# `.explode("token")` turns each item in a token list into a separate row.
# The article's title and category are repeated alongside each token.

# %% part="Part III: Counting words" slide_number=45 slide_title="Technique 2 \u00b7 One row per token" source_label="live-18" tags=["prepared"]
words = corpus.explode("token")
display(words[["title", "category", "token"]].head(6))

# %% [markdown]
# ## 19. Technique 2 · Choose the words to count
#
# **Slide 46 · prepared**
#
# Keep alphabetic tokens that are not stop words. Count lowercase word forms.
#
# `keep` collects a True/False decision for each row. `words[keep]` selects the
# True rows. `token.lower_` supplies the lowercase form, not a lemma.

# %% part="Part III: Counting words" slide_number=46 slide_title="Technique 2 \u00b7 Choose the words to count" source_label="live-19" tags=["prepared"]
keep = []
word_text = []
for token in words["token"]:
    keep.append(token.is_alpha and not token.is_stop)
    word_text.append(token.lower_)
words["word"] = word_text
words = words[keep]
display(words[["title", "category", "word"]].head(6))

# %% [markdown]
# ## 20. Technique 3 · Most frequent across the corpus
#
# **Slide 47 · prepared**
#
# Count the word column with `value_counts` — the same verb as counting one text.
#
# `value_counts()` on the whole word column counts every word in the corpus.

# %% part="Part III: Counting words" slide_number=47 slide_title="Technique 3 \u00b7 Most frequent across the corpus" source_label="live-20" tags=["prepared"]
import matplotlib.pyplot as plt
top = words["word"].value_counts().head(10).sort_values()
fig, ax = plt.subplots(figsize=(7, 3), layout="constrained")
ax.barh(top.index, top.values)
ax.set_xlabel("Occurrences across 439 articles")
plt.show()

# %% [markdown]
# ## 21. Technique 4 · Most frequent in one article
#
# **Slide 48 · prepared**
#
# Filter the same table to one article.
#
# Filter the word table to one article's rows, then `value_counts`.

# %% part="Part III: Counting words" slide_number=48 slide_title="Technique 4 \u00b7 Most frequent in one article" source_label="live-21" tags=["prepared"]
one_article = words[words["title"] == "Roundhouse (venue)"]
top = one_article["word"].value_counts().head(8).sort_values()
fig, ax = plt.subplots(figsize=(7, 2.8), layout="constrained")
ax.barh(top.index, top.values)
ax.set_xlabel("Occurrences in the Roundhouse article")
plt.show()

# %% [markdown]
# ## 22. Technique 5 · Most frequent by group
#
# **Slide 49 · prepared**
#
# Count within museums, theatres and music venues, using the category column.
#
# The category came in with the data, so we just filter and `value_counts` per group.

# %% part="Part III: Counting words" slide_number=49 slide_title="Technique 5 \u00b7 Most frequent by group" source_label="live-22" tags=["prepared"]
pd.DataFrame({
    category: words[words["category"] == category]["word"].value_counts().head(6).index
    for category in ["Museum", "Theatre", "Music venue"]})

# %% [markdown]
# ## 23. Technique 6 · Top words as a proportion
#
# **Slide 50 · prepared**
#
# Counts favour the biggest group. A **share** — `value_counts(normalize=True)` — lets
# us compare groups of different sizes.
#
# `normalize=True` turns counts into shares, so a bigger group no longer looks bigger.

# %% part="Part III: Counting words" slide_number=50 slide_title="Technique 6 \u00b7 Top words as a proportion" source_label="live-23" tags=["prepared"]
rows = []
for category in ["Museum", "Theatre", "Music venue"]:
    share = words[words["category"] == category]["word"].value_counts(normalize=True).head(4) * 100
    for word, percent in share.items():
        rows.append({"category": category, "word": word, "percent": round(percent, 2)})
pd.DataFrame(rows)

# %% [markdown]
# # Part IV: Sentiment in reviews

# %% [markdown]
# ## 24. Technique 7 · Score sentiment across the reviews
#
# **Slide 52 · prepared**
#
# **VADER** scores each text from −1 (negative) to +1 (positive). Apply it to every
# review.
#
# `.apply` runs the scorer on every review. We keep the original text — punctuation and
# capitals change the score.

# %% part="Part IV: Sentiment in reviews" slide_number=52 slide_title="Technique 7 \u00b7 Score sentiment across the reviews" source_label="live-24" tags=["prepared"]
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
scorer = SentimentIntensityAnalyzer()
reviews = pd.read_csv(teaching_file("w09_review_scores.csv"))
reviews["score"] = reviews["review_text"].apply(
    lambda text: scorer.polarity_scores(text)["compound"])
display(reviews[["canonical_name", "rating", "score"]].head(6))

# %% [markdown]
# ## 25. Technique 8 · Stars vs sentiment score
#
# **Slide 53 · prepared**
#
# Do our scores agree with the visitors' stars? Compare the mean score per star, and
# test the correlation.
#
# **The score rises with the rating, but the link is weak (r ≈ 0.22): stars and text sentiment agree only loosely.**
#
#
# `pearsonr` returns the correlation and a p-value — a small p means the link is
# unlikely to be chance, not that it is strong.

# %% part="Part IV: Sentiment in reviews" slide_number=53 slide_title="Technique 8 \u00b7 Stars vs sentiment score" source_label="live-25" tags=["prepared"]
from scipy.stats import pearsonr
mean_by_star = reviews.groupby("rating")["score"].mean()
r, p = pearsonr(reviews["rating"], reviews["score"])
fig, ax = plt.subplots(figsize=(7, 2.8), layout="constrained")
ax.bar(mean_by_star.index.astype(str), mean_by_star.values)
ax.set_xlabel("Star rating")
ax.set_ylabel("Mean VADER score")
ax.set_title(f"Pearson r = {r:.2f}  (p = {p:.1g})")
plt.show()

# %% [markdown]
# # Explain a result
#
# For a result we want to report, identify the source and counting unit, state the
# preprocessing rule and denominator, and explain what the output supports. Retain
# the passages needed to assess that interpretation.
