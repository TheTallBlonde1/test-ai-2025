# aiss (Application Intelligence Subsystem)

Core orchestration package for model detection and OpenAI query flows.

## Table of contents

- [Overview](#overview)
- [Key modules](#key-modules)
- [Quickstart](#quickstart)
- [API](#api)
- [Configuration](#configuration)
- [Extensibility](#extensibility)
- [Related packages](#related-packages)

## Overview

This package glues together model detection and three query flows (parsed, JSON, text) with a consistent UX. It relies on Rich for terminal output and `python-dotenv` for configuration.

## Key modules

- `run_queries.py`
  - `run_the_query(input_text, result_type)` orchestrates:
    1) Detect model type (`check_model.find_model_from_input`)
    2) Execute the selected response mode
    3) Render progress using Rich
- `check_model.py`
  - Uses OpenAI Responses (parse) to determine the appropriate model type, returning a `ModelTypeResult`.
- `utils.py`
  - Shared helpers used across response flows and tests.

## Quickstart

```python
from aiss import run_the_query, ResultType

run_the_query("The Matrix", ResultType.PARSED)
```

Or via CLI (see root README):

```pwsh
python main.py "Breaking Bad" --mode parsed
```

## API

### run_the_query

Signature:

```
run_the_query(input_text: str, result_type: ResultType | str | None = ResultType.PARSED) -> None
```

- `input_text`: Title or description used for detection and querying
- `result_type`: One of `parsed`, `json`, or `text` (case-insensitive). Defaults to `parsed`.

Behavior:

- Converts string modes to `ResultType`
- Displays a progress bar while detecting the model type and running the selected flow
- Delegates to `openai_direct.get_parsed_response`, `get_json_response`, or `get_text_response`

## Configuration

Place your OpenAI API key in a `.env` file at the repository root or export it in your environment:

```
OPENAI_API_KEY=sk-...
```

`dotenv.load_dotenv()` is called on import where needed.

## Extensibility

To support a new format or category, add model definitions under `aiss/models/` and expose them via `ModelType` (see that package README). The detection step dynamically references the registry.

## Related packages

- [aiss/models](../models/README.md) — model types, registries, and shared helpers
- [aiss/openai_direct](../openai_direct/README.md) — implementations for parsed/JSON/text flows and Wikipedia augmentation

## Navigation

- Up: [Project root](../README.md)
- Peer: [Models](../models/README.md)
- Peer: [OpenAI Direct](../openai_direct/README.md)
