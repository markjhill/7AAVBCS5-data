# The Lothian Diary Project — transcripts

21 transcribed audio/video diaries (1,035 utterances) recorded by residents of Edinburgh and the
Lothians during the first Covid-19 lockdown in 2020.

These are the depositors' own **anonymised public release**. They are redistributed here for teaching
on 7AAVBCS5 with attribution; the authoritative copy is the Edinburgh DataShare deposit below, and
you should cite that, not this repository.

## Source

- **Collection:** The Lothian Diary Project, University of Edinburgh
- **Repository:** <https://datashare.ed.ac.uk/collections/4fa77e28-8c6f-42f7-8bf6-317ba700ac52/search>
- **Persistent handle:** <https://hdl.handle.net/10283/3830>
- **DOI:** <https://doi.org/10.7488/ds/3009>
- **Dataset 1 record:** <https://www.research.ed.ac.uk/en/datasets/lothian-diaries-dataset-1-may-september-2020>

**Project team:** Hall-Lew, Lauren; Cowie, Claire; McNulty, Stephen; Markl, Nina; Liu, Sarah; Lai,
Catherine; Llewellyn, Clare; Alex, Beatrice; Fang, Nini; Elliott Slosarova, Zuzana; Klingler, Anita.

## Papers to cite

The project's data paper, which is also on the module reading list:

> Hall-Lew, L. et al. "The Lothian Diary Project: Investigating the Impact of the COVID-19 Pandemic
> on Edinburgh and Lothian Residents." *Journal of Open Humanities Data*.
> <https://doi.org/10.5334/johd.25>

On place and the city in the recordings:

> "Imagining the city in lockdown: Place in the COVID-19 self-recordings of the Lothian Diary
> Project." *Frontiers in Artificial Intelligence*. <https://doi.org/10.3389/frai.2022.945643>

## Licence

Edinburgh DataShare deposits carry an end-user licence supplied with the record. **Check the licence
file on the DataShare record before reusing this data outside the module**, and cite the deposit in
any work that uses it.

## File format

Tab-separated, one row per utterance, despite the `.txt` extension:

```python
import pandas as pd
diary = pd.read_csv(data_path("LothianDiaries/LothianDiaries_11_Transcript.txt"), sep="\t")
```

| Column | Meaning |
|---|---|
| `File` | diary identifier, matches the filename |
| `Speaker` | speaker id — one per diary in this subset |
| `Start`, `End` | seconds from the start of the recording |
| `Transcription` | the transcribed speech |

## Things to know before analysing it

- **Speakers introduce themselves by first name.** These are in the depositors' public anonymised
  release, but they are still real first names — so a named-entity pass will pick up PERSON entities
  that are participants, not public figures. Worth saying out loud if this is used in Week 10.
- **The transcription is of speech**, so it contains hesitation markers (`(uh)`, `(um)`, `em`),
  false starts, and occasional typos from transcription (`thing s(um)`). Anything that assumes clean
  written prose will behave oddly.
- **`Start` and `End` are seconds**, which makes utterance duration and speech rate available —
  the temporal dimension of the Bloomsbury framework, on a corpus that is otherwise about place.
- 21 diaries is a small sample. It supports description, not generalisation to Edinburgh.
