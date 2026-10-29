# claude_direct

Anthropic (Claude) counterparts of the `openai_direct` flows. Each takes
`(model_type_input: ModelTypeInput, client: anthropic.Anthropic, console: Console)`.

- `get_parsed_response` — `client.messages.parse(..., output_format=<format class>)` (structured outputs); renders and returns the parsed model, or `None`.
- `get_json_response` — `client.messages.create` with the format's JSON instructions, then `json.loads` (with a regex fallback) and `render_from_json`.
- `get_text_response` — `client.messages.create`; prints the text in a Rich panel.

Classification uses `aiss.check_model.find_model_from_input_claude`. Wikipedia context helpers are reused from `aiss.openai_direct.wikipedia_tool`.

## Configuration

- `ANTHROPIC_API_KEY` — required (environment or `.env`).
- `ANTHROPIC_MODEL_NAME` — optional, defaults to `claude-sonnet-5-5`.

Safety refusals (`stop_reason == "refusal"`) are reported and the flow returns without rendering.

```pwsh
python main.py "The Godfather" --mode parsed --api claude
```
