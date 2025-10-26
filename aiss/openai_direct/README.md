# aiss.openai_direct

Implementations for the three OpenAI response flows and the Wikipedia topic context tool.

## Table of contents

- [Overview](#overview)
- [Modules](#modules)
- [Wikipedia tool](#wikipedia-tool)
- [Usage](#usage)
- [Error handling](#error-handling)

## Overview

These helpers take a detected `ModelTypeResult`, build an appropriate prompt (optionally augmented with Wikipedia context), and call the OpenAI Responses API to retrieve either typed objects, JSON output, or plain text.

## Modules

- `openai_parsed.py`
  - `get_parsed_response(model_type_result, client, console, text_format=None)`
  - Uses `client.responses.parse` to get a typed object and calls its `.render(console)` method.
- `openai_json.py`
  - `get_json_response(model_type_result, client, console, text_format=None)`
  - Retrieves text and parses JSON (with a fallback regex extraction), then renders via `render_from_json`.
- `openai_text.py`
  - `get_text_response(model_type_result, client, console, text_format=None)`
  - Retrieves plain text output and writes it to the console.

All three accept an optional `text_format` to override the format class that would otherwise be derived from `model_type_result.model_type`.

## Wikipedia tool

- `wikipedia_tool.py`
  - `build_wikipedia_topic_context(text_format, model_type_result)` returns `(wikipedia_summary, context_hint)` or an empty string when the topic is empty.
  - `augment_prompt_with_wikipedia_context(base_prompt, wikipedia_summary, context)` appends context + summary to a prompt.
  - `augment_instructions_with_tool_hint(instructions, wikipedia_summary, context)` appends guidance into system instructions.

## Usage

```python
from aiss.openai_direct.openai_parsed import get_parsed_response
from aiss.models.shared import ModelTypeResult, ModelType
from openai import OpenAI
from rich.console import Console

client = OpenAI()
console = Console()
result = ModelTypeResult(model_type=ModelType.DRAMA, description="A dramatic TV series", formatted_name="Breaking Bad")
get_parsed_response(result, client, console)
```

## Error handling

- JSON flow tolerates non-JSON wrappers by extracting JSON via regex
- Wikipedia errors are caught and logged, and processing continues without context
- Parsed flow checks for a missing `output_parsed`

## Navigation

- Up: [aiss](../README.md)
- Up: [Project root](../../README.md)
- Related: [Models](../models/README.md)
