from typing import List, Union
import json
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from aiss.models.shared import TableSchema


def render_table_from_schema(title: str, schema: List[Union[dict, TableSchema]], items: list, console: Console) -> None:
    """Render a Rich Table from a schema and list of objects.

    schema: list of dicts with keys:
        - header: column name shown in the table
        - attr: attribute name to read from each item (getattr)
        - style: (optional) rich style for the column
        - justify: (optional) justification for the column
        - no_wrap: (optional) no_wrap boolean
        - formatter: (optional) callable or format-spec string to format the value

    Example:
        schema = [
            {"header": "Name", "attr": "character", "style": "magenta", "no_wrap": True},
            {"header": "Actor", "attr": "actor", "style": "cyan"},
        ]
    """
    table = Table(title=title, show_lines=True)
    # add columns
    for col in schema:
        # allow either dict-based schema (legacy) or TableSchema dataclass
        if isinstance(col, TableSchema):
            header = col.header
            style = col.style
            justify = col.justify
            no_wrap = col.no_wrap
        else:
            header = col.get("header")
            style = col.get("style")
            justify = col.get("justify")
            no_wrap = col.get("no_wrap", False)

        if justify:
            table.add_column(header, style=style, justify=justify, no_wrap=no_wrap)
        else:
            table.add_column(header, style=style, no_wrap=no_wrap)

    # add rows
    for it in items:
        row = []
        for col in schema:
            if isinstance(col, TableSchema):
                attr = col.name
                formatter = col.formatter
            else:
                attr = col.get("attr")
                formatter = col.get("formatter")

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
    """Render a JSON-shaped ShowInfo (dict or JSON string) to the provided Rich Console.

    Expected keys (best-effort):
      - show_summary (str)
      - characters (list[dict])
      - broadcast_info (list[dict])
      - production_companies (list[dict])

    This function tolerates missing keys and formats years like the models do.
    """

    def _format_year(v) -> str:
        try:
            return str(int(v)) if v else "-"
        except Exception:
            return str(v)

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
