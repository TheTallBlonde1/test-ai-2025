# aiss.models.movies

Typed models for movie formats and genres. Used by detection and all three response flows to drive prompts, parsing, and rendering.

## Table of contents

- [Included models](#included-models)
- [Common base](#common-base)
- [Usage](#usage)
- [Add a new movie model](#add-a-new-movie-model)

## Included models

- `action_adventure_model.py` — Action/Adventure
- `comedy_model.py` — Comedy
- `drama_model.py` — Drama
- `fantasy_science_fiction_model.py` — Fantasy/Sci-Fi
- `horror_model.py` — Horror
- `romance_model.py` — Romance
- `thriller_mystery_crime_model.py` — Thriller/Mystery/Crime
- `documentary_biographical_model.py` — Documentary/Biographical

## Common base

`_base.py` houses shared fields and rendering helpers to keep model implementations consistent and testable.

## Usage

```python
from aiss.models.shared import ModelType

format_cls = ModelType.DRAMA_MOVIE.get_model_from_name()
print(format_cls.description)
```

## Add a new movie model

1) Add a new `*_model.py` file with `model_name`, `description`, and `key_trait`.
2) Register the new type in `ModelType` within `shared.py`.
3) Write tests (see `tests/models/movies/`) and run them.

## Navigation

- Up: [Models index](../README.md)
- Up: [aiss](../../README.md)
- Up: [Project root](../../../README.md)
- Peers: [Games](../games/README.md) • [Shows](../shows/README.md)
- Related: [OpenAI Direct](../../openai_direct/README.md)
