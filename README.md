# test-ai-2025

Modern Python toolkit that classifies entertainment topics (shows, movies, games) and queries OpenAI to produce rich, structured outputs. It supports three flows out of the box: parsed (typed models), JSON (schema-first), and plain text, optionally augmented with Wikipedia context for higher fidelity.

## Table of contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech stack](#tech-stack)
- [Requirements](#requirements)
- [Environment setup](#environment-setup)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
	- [CLI](#cli)
	- [Python API](#python-api)
- [Project structure](#project-structure)
- [Testing](#testing)
- [Linting and formatting](#linting-and-formatting)
- [Contributing](#contributing)
- [License](#license)

## Overview

Given a piece of input text (e.g., a movie title or a description of a TV show), the system:

1) Detects the best-fitting model type (e.g., drama show, action-adventure movie, shooter game).
2) Queries OpenAI using one of three flows: parsed models, JSON, or plain text.
3) Renders results to the console with Rich, optionally incorporating Wikipedia context for improved prompts.

The project is thoroughly tested and built for extension—add new formats by dropping model files into the appropriate package.

## Features

- Model detection via OpenAI Responses with a structured schema
- Three answer modes: parsed (typed), JSON, and text
- Wikipedia-powered topic context for better results
- Colorful console UX via Rich with progress feedback
- Clear, extensible model registry and typed helpers
- High test coverage and fast feedback loop

## Architecture

- Core entry points live under `aiss/`:
	- `run_the_query`: Orchestrates detection + chosen response flow
	- `check_model.find_model_from_input`: Asks OpenAI to select the model type
	- `openai_direct/*`: Implements the three response modes and Wikipedia tool
	- `models/*`: Typed model descriptors for shows, movies, and games

See package READMEs for deep dives:

- [aiss/](aiss/README.md)
- [aiss/models/](aiss/models/README.md)
- [aiss/models/games/](aiss/models/games/README.md)
- [aiss/models/movies/](aiss/models/movies/README.md)
- [aiss/models/shows/](aiss/models/shows/README.md)
- [aiss/openai_direct/](aiss/openai_direct/README.md)

## Tech stack

- Python 3.14+
- OpenAI Python SDK
- Rich (terminal rendering)
- python-dotenv (environment loading)
- Wikipedia (topic summaries)
- Pytest, Ruff, Coverage (dev)

## Requirements

- Python 3.14+
- An OpenAI API key available in your environment or a `.env` file

## Environment setup

Windows PowerShell example:

```pwsh
# Create and activate a virtual environment (optional but recommended)
py -3.14 -m venv .venv
.venv/Scripts/Activate.ps1

# Upgrade pip and install the project with dev tools
python -m pip install --upgrade pip
pip install -e .[dev]
```

## Installation

Install the package (without dev extras):

```pwsh
pip install -e .
```

## Configuration

Provide your OpenAI credentials via environment variables or a `.env` file in the repo root:

```
OPENAI_API_KEY=sk-...
```

The code uses `python-dotenv` to load `.env` automatically.

## Usage

### CLI

Run the demo CLI to classify and query a topic:

```pwsh
python main.py "Breaking Bad" --mode parsed
python main.py "The Matrix" --mode json
python main.py "Doom Eternal" --mode text
```

Modes: `parsed`, `json`, `text`.

### Python API

```python
from aiss import run_the_query, ResultType

run_the_query("Match of the Day shown on Saturdays on BBC One in the UK", ResultType.PARSED)
run_the_query("The Matrix", ResultType.JSON)
run_the_query("Doom Eternal", ResultType.TEXT)
```

## Project structure

```
test-ai-2025/
├─ aiss/
│  ├─ models/            # Typed model registry and categories
│  ├─ openai_direct/     # Response flows + Wikipedia tool
│  ├─ run_queries.py     # Orchestrates detect + query
│  ├─ check_model.py     # Model detection using OpenAI
│  └─ utils.py           # Shared utilities
├─ tests/                # Comprehensive unit tests
├─ main.py               # Simple CLI entrypoint
├─ pyproject.toml        # Project metadata & deps
└─ README.md             # You’re here
```

## Testing

```pwsh
.venv/Scripts/python.exe -m pytest
```

## Linting and formatting

```pwsh
ruff check . --fix
```

## Contributing

- Open an issue describing the change you’d like to make
- Create a feature branch and include tests
- Keep the public API stable unless versioning is updated

## License

License information is not specified yet. Add a LICENSE file to clarify usage terms.

