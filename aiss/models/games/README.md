# aiss.models.games

Genre-specific models for video games (e.g., action-adventure, shooter, RPG). These classes define typed fields plus human metadata (`model_name`, `description`, `key_trait`) to guide classification and rendering.

## Table of contents

- [Included models](#included-models)
- [Common base](#common-base)
- [Usage](#usage)
- [Add a new game model](#add-a-new-game-model)

## Included models

- `action_adventure_model.py` — Action-Adventure
- `shooter_model.py` — Shooter / FPS
- `role_playing_model.py` — RPG
- `puzzle_strategy_model.py` — Puzzle/Strategy
- `simulation_sandbox_model.py` — Simulation/Sandbox
- `sports_racing_model.py` — Sports/Racing
- `horror_survival_model.py` — Horror/Survival
- `mmo_online_model.py` — MMO/Online

## Common base

`_base.py` contains shared structure and rendering helpers for all game models to keep implementations consistent.

## Usage

Obtain the typed model class from `ModelType` and use it in the parsed flow:

```python
from aiss.models.shared import ModelType

format_cls = ModelType.SHOOTER_GAME.get_model_from_name()
assert format_cls.model_name  # e.g., "Shooter"
```

## Add a new game model

1) Create `your_new_model.py` in this folder.
2) Implement `model_name`, `description`, `key_trait`, and fields to parse/render.
3) Register it in `ModelType` (see `aiss/models/shared.py`).
4) Add tests in `tests/models/games/` and run the suite.

## Navigation

- Up: [Models index](../README.md)
- Up: [aiss](../../README.md)
- Up: [Project root](../../../README.md)
- Peers: [Movies](../movies/README.md) • [Shows](../shows/README.md)
- Related: [OpenAI Direct](../../openai_direct/README.md)
