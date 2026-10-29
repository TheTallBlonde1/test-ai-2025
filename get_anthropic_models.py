"""List the Anthropic models available to the configured ANTHROPIC_API_KEY.

Usage:
    python get_anthropic_models.py
"""

import os
import sys

from anthropic import Anthropic, APIError
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from aiss.claude_direct._common import DEFAULT_CLAUDE_MODEL, get_model_name

load_dotenv()


def main() -> int:
    console = Console()
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]ANTHROPIC_API_KEY is not set (environment or .env).[/red]")
        return 1

    try:
        models = list(Anthropic().models.list())
    except APIError as exc:
        console.print(f"[red]Failed to list models: {exc}[/red]")
        return 1

    selected = get_model_name()
    table = Table(title="Available Anthropic models")
    table.add_column("ID")
    table.add_column("Display name")
    table.add_column("Created")
    table.add_column("Selected")
    for model in models:
        table.add_row(
            model.id,
            model.display_name,
            model.created_at.date().isoformat(),
            "[green]✓[/green]" if model.id == selected else "",
        )
    console.print(table)

    if selected not in {m.id for m in models}:
        console.print(f"[yellow]Configured model '{selected}' is not in this list (default: {DEFAULT_CLAUDE_MODEL}).[/yellow]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
