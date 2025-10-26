# aiss.models

Typed model registry and helpers that describe the shapes for shows, movies, and games. These models power the parsed and JSON flows and guide prompts for the text flow.

## Table of contents

- [Overview](#overview)
- [Core types](#core-types)
- [Model registry](#model-registry)
- [Packages](#packages)
- [Extending models](#extending-models)

## Overview

The `models` package captures the structure of content across three domains: shows, movies, and games. Each domain includes genre-specific model classes with a human description and a key trait that guide prompts and rendering.

## Core types

- `ModelType` (Enum)
  - Canonical list of model types (e.g., `DRAMA`, `COMEDY`, `ACTION_ADVENTURE_MOVIE`, `SHOOTER_GAME`, etc.)
  - Provides `get_model_from_name()`, `display_label`, and helper listings for instructions
- `ModelTypeResult` (dataclass)
  - Returned from detection; contains `model_type`, `description`, `formatted_name`, and optional `additional_info`
- `TableSchema` (dataclass)
  - Tiny helper used by renderers for tabular output

## Model registry

`ModelType.registry()` maps the string values of the enum to concrete model classes. It is cached and used by detection and rendering flows. Each concrete model class exposes at least:

- `model_name` — human-friendly label
- `description` — what defines this type
- `key_trait` — the single most important attribute for classification

These attributes appear in instruction listings and context building (e.g., Wikipedia hints).

## Packages

- [games](games/README.md)
- [movies](movies/README.md)
- [shows](shows/README.md)

## Extending models

1) Pick a domain (games, movies, shows) and copy an existing model file as a starting point.
2) Implement the required attributes (`model_name`, `description`, `key_trait`) and the data fields you want to capture.
3) Add a new `ModelType` enum member pointing to your class in `shared.py`.
4) Update or add tests under `tests/models/...` and run the suite.

## Navigation

- Up: [aiss](../README.md)
- Up: [Project root](../../README.md)
- Down: [Games](games/README.md) • [Movies](movies/README.md) • [Shows](shows/README.md)
