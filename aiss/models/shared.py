from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class TableSchema:
    """Schema descriptor for a table column.

    Fields:
      - name: attribute name on the item (was previously 'attr' in dict schemas)
      - header: column header shown
      - style: optional Rich style for the column
      - no_wrap: don't wrap the column
      - justify: optional justification (e.g., 'center')
      - formatter: optional callable to format values for this column
    """

    name: str
    header: str
    style: Optional[str] = None
    no_wrap: bool = False
    justify: Optional[str] = None
    formatter: Optional[Callable[[Any], str]] = None
