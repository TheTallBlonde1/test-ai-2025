# aiss.models.shows

Typed models for television and streaming shows by genre/category. These guide prompts, classification, and rendering for the parsed and JSON flows.

## Table of contents

- [Included models](#included-models)
- [Common base](#common-base)
- [Usage](#usage)
- [Add a new show model](#add-a-new-show-model)

## Included models

- `drama_model.py` — Drama
- `comedy_model.py` — Comedy
- `thriller_model.py` — Thriller
- `action_fantasy_model.py` — Action/Adventure/Fantasy
- `science_fiction_model.py` — Science Fiction
- `documentary_model.py` — Documentary/Factual
- `family_kids_model.py` — Family/Animation/Kids
- `news_model.py` — News/Informational
- `reality_model.py` — Reality/Competition/Lifestyle
- `sports_model.py` — Sports

## Common base

`_base.py` provides shared types and renderers for show formats.

## Usage

```python
from aiss.models.shared import ModelType

format_cls = ModelType.DRAMA.get_model_from_name()
print(format_cls.model_name)
```

## Add a new show model

1) Create a new `*_model.py` with the required attributes and fields.
2) Wire it into `ModelType` mapping in `shared.py`.
3) Add tests in `tests/models/shows/`.

## Navigation

- Up: [Models index](../README.md)
- Up: [aiss](../../README.md)
- Up: [Project root](../../../README.md)
- Peers: [Games](../games/README.md) • [Movies](../movies/README.md)
- Related: [OpenAI Direct](../../openai_direct/README.md)
