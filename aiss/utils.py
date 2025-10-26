"""Utilities for rendering model data to the console.

This module centralizes how Pydantic models or JSON-derived dicts are
rendered to the terminal using Rich. It exposes two primary helpers:
`render_table_from_schema` and `render_from_json`.

"""

import json
from typing import List, Union

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .models.shared import TableSchema

# MARK: Generic number helpers


def _coerce_numeric(value):
    """Coerce a value into a float, handling common string inputs."""

    if value is None:
        raise ValueError("Value is None")
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("Empty string")
        cleaned = stripped.replace(",", "")
        if cleaned.lower() == "present":
            raise ValueError("present sentinel")
        return float(cleaned)
    raise TypeError(f"Unsupported type: {type(value)!r}")


# MARK: Formatters
def format_money(v, currency: str = "$") -> str:
    """
    Format a numeric value as a human-friendly money string with
    thousands separators and an optional currency symbol.

    :param v: Numeric value (int/float/str) or None
    :param currency: Currency symbol to prefix (default: "$")
    :return: Formatted money string or '-' for falsy/invalid values
    """
    try:
        number = _coerce_numeric(v)
    except Exception:
        if v is None:
            return "-"
        if isinstance(v, str) and v.strip() == "":
            return "-"
        try:
            return f"{currency}{str(v)}"
        except Exception:
            return str(v)

    rounded = int(number)
    return f"{currency}{rounded:,}"


def format_year(v) -> str:
    """
    Format a year-like value into a human-friendly string.

    Returns '-' for falsy values, otherwise returns the integer form as a string.
    """
    try:
        if v is None:
            return "-"
        if isinstance(v, str):
            stripped = v.strip()
            if not stripped:
                return "-"
            if stripped.lower() == "present":
                return "Present"
            v = stripped

        try:
            year_value = int(float(v))
        except Exception:
            return str(v)

        if year_value <= 0:
            return "-"
        if year_value >= 9999:
            return "Present"
        return str(year_value)
    except Exception:
        return str(v)


def format_number(v) -> str:
    """Format large integers with thousands separators."""

    try:
        number = _coerce_numeric(v)
    except Exception:
        return str(v)

    rounded = round(number)
    if abs(number - rounded) < 1e-6:
        return f"{int(rounded):,}"
    return f"{number:,.2f}".rstrip("0").rstrip(".")


def format_decimal(v, digits: int = 1) -> str:
    """Format a numeric value to a fixed number of decimal places."""

    try:
        number = _coerce_numeric(v)
    except Exception:
        return str(v)

    formatted = f"{number:.{digits}f}"
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")
    return formatted


def format_percentage(v) -> str:
    """Format a ratio or percentage value gracefully."""

    try:
        number = _coerce_numeric(v)
    except Exception:
        return str(v)

    if abs(number) <= 1:
        number *= 100

    formatted = f"{number:.1f}".rstrip("0").rstrip(".")
    return f"{formatted}%"


def format_runtime_minutes(v) -> str:
    """Format a runtime in minutes with a suffix."""

    try:
        minutes = int(round(_coerce_numeric(v)))
    except Exception:
        return str(v)

    if minutes <= 0:
        return "-"
    return f"{minutes:,} min"


# MARK: Table Renderer
def render_table_from_schema(title: str, schema: List[TableSchema], items: list, console: Console) -> None:
    """
    Render a Rich Table from a schema and list of objects.

    :param title: Title used for the Rich Table
    :type title: str

    :param schema: Column schema as a list of dicts (legacy) or TableSchema
        dataclass instances.
    :type schema: List[Union[dict, TableSchema]]

    :param items: Iterable of items to render. Each item may be a dict or an
        object with attributes matching the schema.name values.
    :type items: list

    :param console: Rich Console to print the table to
    :type console: Console

    :return: None
    :rtype: None
    """
    table = Table(title=title, show_lines=True)
    # add columns
    for col in schema:
        # allow either dict-based schema (legacy) or TableSchema dataclass

        header = col.header
        style = col.style
        justify = col.justify
        no_wrap = col.no_wrap

        if justify:
            table.add_column(header, style=style, justify=justify, no_wrap=no_wrap)
        else:
            table.add_column(header, style=style, no_wrap=no_wrap)

    # add rows
    for it in items:
        row = []
        for col in schema:
            attr = col.name
            formatter = col.formatter

            # support items that are either objects (getattr) or dicts
            if attr:
                if isinstance(it, dict):
                    val = it.get(attr)
                else:
                    val = getattr(it, attr, None)
            else:
                val = None

            if val is None:
                rendered = "-"
            else:
                # handle common container types
                if isinstance(val, (list, tuple)) and not isinstance(val, str):
                    # join simple elements, otherwise str() each
                    try:
                        rendered = ", ".join(str(x) for x in val)
                    except Exception:
                        rendered = str(val)
                else:
                    rendered = val

                if formatter:
                    try:
                        if callable(formatter):
                            rendered = formatter(val)
                        elif isinstance(formatter, str):
                            # treat as format spec
                            rendered = format(val, formatter)
                        else:
                            # unknown formatter type; fall back to str()
                            rendered = str(rendered)
                    except Exception:
                        # on any formatting failure, fall back to str()
                        rendered = str(val)

            row.append(str(rendered))

        table.add_row(*row)

    console.print(table)


def render_from_json(data: Union[dict, str], console: Console) -> None:
    """
    Render a JSON-shaped ShowInfo (dict or JSON string) to the provided
    Rich Console.

    This helper is forgiving: it accepts either a parsed dict or a raw JSON
    string, pretty-prints the raw JSON and then renders summary panels and
    tables for characters, broadcast info and production companies.

    :param data: JSON-shaped data as a dict or a JSON string
    :type data: Union[dict, str]

    :param console: Rich Console instance used for output
    :type console: Console

    :return: None
    :rtype: None
    """

    # Use the shared year formatter
    _format_year = format_year

    # If a raw JSON string was passed, parse it first.
    parsed = data
    if isinstance(data, str):
        try:
            parsed = json.loads(data)
        except Exception:
            # If parsing fails, show the raw text and return.
            console.print(Panel(data, title="Raw JSON (invalid)", expand=False, style="red"))
            return

    # Print the pretty JSON first for inspection
    try:
        console.print(Panel(json.dumps(parsed, indent=2, ensure_ascii=False), title="Raw JSON", expand=False, style="blue"))
    except Exception:
        # Fall back to a simple string representation
        console.print(Panel(str(parsed), title="Raw JSON", expand=False, style="blue"))

    summary_text = parsed.get("show_summary") if isinstance(parsed, dict) else None
    summary_text = summary_text or (parsed.get("summary") if isinstance(parsed, dict) else None) or "(no summary returned)"
    console.print(Panel(summary_text, title="Summary", expand=False, style="green"))

    # Characters
    characters = parsed.get("characters") or []
    if characters:
        char_schema = [
            TableSchema(name="character", header="Name", style="magenta", no_wrap=True),
            TableSchema(name="actor", header="Actor", style="cyan"),
            TableSchema(name="relationship", header="Relationship", style="yellow"),
            TableSchema(name="year_joined", header="Year Joined", justify="center", formatter=_format_year),
            TableSchema(name="description", header="Description"),
        ]

        render_table_from_schema("Characters", char_schema, characters, console)
    else:
        console.print("[yellow]No character info returned.[/yellow]")

    # Broadcast info
    broadcast = parsed.get("broadcast_info") or []
    if broadcast:
        broadcast_schema = [
            TableSchema(name="network", header="Network", style="magenta"),
            TableSchema(name="country", header="Country", style="cyan"),
            TableSchema(name="start_year", header="Start Year", justify="center", formatter=_format_year),
            TableSchema(name="end_year", header="End Year", justify="center", formatter=_format_year),
        ]

        render_table_from_schema("Broadcast Info", broadcast_schema, broadcast, console)

    # Production companies
    companies = parsed.get("production_companies") or []
    if companies:
        company_schema = [
            TableSchema(name="name", header="Name", style="magenta"),
            TableSchema(name="founded_year", header="Founded Year", justify="center", formatter=_format_year),
            TableSchema(name="start_year", header="Start Year", justify="center", formatter=_format_year),
            TableSchema(name="end_year", header="End Year", justify="center", formatter=_format_year),
            TableSchema(name="country", header="Country", style="cyan"),
        ]

        render_table_from_schema("Production Companies", company_schema, companies, console)
