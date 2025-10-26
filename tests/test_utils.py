"""
Tests for aiss.utils module.

This module contains comprehensive tests for utility functions including
formatters, table rendering, and JSON deserialization.
"""

import json

import pytest
from rich.console import Console

from aiss.models.shared import TableSchema
from aiss.utils import (
    _coerce_numeric,
    format_decimal,
    format_money,
    format_number,
    format_percentage,
    format_runtime_minutes,
    format_year,
    render_from_json,
    render_table_from_schema,
)


# MARK: Numeric Coercion Tests
class TestCoerceNumeric:
    """Tests for _coerce_numeric helper function."""

    def test_coerce_none_raises(self):
        """
        Test that None raises ValueError.

        :raises ValueError: When value is None
        """
        with pytest.raises(ValueError, match="Value is None"):
            _coerce_numeric(None)

    def test_coerce_int(self):
        """
        Test coercing integer to float.

        :return: Coerced float value
        :rtype: float
        """
        assert _coerce_numeric(42) == 42.0

    def test_coerce_float(self):
        """
        Test coercing float (passthrough).

        :return: Same float value
        :rtype: float
        """
        assert _coerce_numeric(3.14) == 3.14

    def test_coerce_string_number(self):
        """
        Test coercing string representation of number.

        :return: Parsed float value
        :rtype: float
        """
        assert _coerce_numeric("123.45") == 123.45

    def test_coerce_string_with_commas(self):
        """
        Test coercing string with thousands separators.

        :return: Parsed float with commas removed
        :rtype: float
        """
        assert _coerce_numeric("1,234,567.89") == 1234567.89

    def test_coerce_empty_string_raises(self):
        """
        Test that empty string raises ValueError.

        :raises ValueError: When string is empty or whitespace-only
        """
        with pytest.raises(ValueError, match="Empty string"):
            _coerce_numeric("")
        with pytest.raises(ValueError, match="Empty string"):
            _coerce_numeric("   ")

    def test_coerce_present_sentinel_raises(self):
        """
        Test that 'present' string raises ValueError.

        The string 'present' is a sentinel value for ongoing periods.

        :raises ValueError: When value is 'present' (case insensitive)
        """
        with pytest.raises(ValueError, match="present sentinel"):
            _coerce_numeric("present")
        with pytest.raises(ValueError, match="present sentinel"):
            _coerce_numeric("PRESENT")

    def test_coerce_unsupported_type_raises(self):
        """
        Test that unsupported types raise TypeError.

        :raises TypeError: When value is list, dict, or other unsupported type
        """
        with pytest.raises(TypeError, match="Unsupported type"):
            _coerce_numeric([1, 2, 3])
        with pytest.raises(TypeError, match="Unsupported type"):
            _coerce_numeric({"key": "value"})


# MARK: Money Formatting Tests
class TestFormatMoney:
    """Tests for format_money formatter."""

    def test_format_money_integer(self):
        """
        Test formatting integer as money.

        :return: Formatted money string with dollar sign and commas
        :rtype: str
        """
        assert format_money(1000) == "$1,000"

    def test_format_money_float(self):
        """
        Test formatting float as money (rounds to int).

        :return: Formatted money string rounded to nearest dollar
        :rtype: str
        """
        assert format_money(1234.56) == "$1,234"

    def test_format_money_string_number(self):
        """
        Test formatting string number as money.

        :return: Formatted money string
        :rtype: str
        """
        assert format_money("5000") == "$5,000"

    def test_format_money_with_commas(self):
        """
        Test formatting string with commas as money.

        :return: Formatted money string preserving magnitude
        :rtype: str
        """
        assert format_money("1,000,000") == "$1,000,000"

    def test_format_money_custom_currency(self):
        """
        Test custom currency symbol.

        :param currency: Custom currency symbol to use
        :type currency: str

        :return: Formatted money string with custom symbol
        :rtype: str
        """
        assert format_money(1000, currency="€") == "€1,000"

    def test_format_money_none(self):
        """
        Test formatting None returns '-'.

        :return: Dash character for missing value
        :rtype: str
        """
        assert format_money(None) == "-"

    def test_format_money_empty_string(self):
        """
        Test formatting empty string returns '-'.

        :return: Dash character for empty value
        :rtype: str
        """
        assert format_money("") == "-"
        assert format_money("   ") == "-"

    def test_format_money_invalid_string(self):
        """
        Test formatting invalid string returns prefixed string.

        :return: Original string prefixed with currency symbol
        :rtype: str
        """
        result = format_money("invalid")
        assert "$invalid" in result

    def test_format_money_exception_handling(self):
        """Test exception handling for edge cases."""

        # Object that can't be converted but has __str__
        class CustomObj:
            def __str__(self):
                return "custom"

        result = format_money(CustomObj())
        assert "custom" in result


class TestFormatYear:
    """Tests for format_year formatter."""

    def test_format_year_integer(self):
        """Test formatting integer year."""
        assert format_year(2023) == "2023"

    def test_format_year_float(self):
        """Test formatting float year."""
        assert format_year(2023.0) == "2023"

    def test_format_year_string(self):
        """Test formatting string year."""
        assert format_year("2023") == "2023"

    def test_format_year_none(self):
        """Test formatting None returns '-'."""
        assert format_year(None) == "-"

    def test_format_year_empty_string(self):
        """Test formatting empty string returns '-'."""
        assert format_year("") == "-"
        assert format_year("   ") == "-"

    def test_format_year_present(self):
        """Test 'present' string returns 'Present'."""
        assert format_year("present") == "Present"
        assert format_year("PRESENT") == "Present"
        assert format_year("  Present  ") == "Present"

    def test_format_year_zero_or_negative(self):
        """Test zero or negative returns '-'."""
        assert format_year(0) == "-"
        assert format_year(-1) == "-"

    def test_format_year_future_large(self):
        """Test very large year returns 'Present'."""
        assert format_year(9999) == "Present"
        assert format_year(10000) == "Present"

    def test_format_year_invalid_string(self):
        """Test invalid string returns as-is."""
        assert format_year("invalid") == "invalid"

    def test_format_year_exception_handling(self):
        """Test exception handling returns string representation."""

        class CustomObj:
            def __str__(self):
                return "custom_year"

        assert format_year(CustomObj()) == "custom_year"


class TestFormatNumber:
    """Tests for format_number formatter."""

    def test_format_number_integer(self):
        """Test formatting integer with thousands separators."""
        assert format_number(1000) == "1,000"
        assert format_number(1234567) == "1,234,567"

    def test_format_number_float_whole(self):
        """Test formatting float that's effectively whole number."""
        assert format_number(1000.0) == "1,000"

    def test_format_number_float_decimal(self):
        """Test formatting float with significant decimals."""
        assert format_number(1234.56) == "1,234.56"

    def test_format_number_string(self):
        """Test formatting string number."""
        assert format_number("5000") == "5,000"

    def test_format_number_invalid(self):
        """Test invalid input returns string representation."""
        assert format_number("invalid") == "invalid"

    def test_format_number_strips_trailing_zeros(self):
        """Test that trailing zeros after decimal are removed."""
        assert format_number(100.10) == "100.1"
        assert format_number(100.00) == "100"


class TestFormatDecimal:
    """Tests for format_decimal formatter."""

    def test_format_decimal_default_digits(self):
        """Test default 1 decimal place."""
        assert format_decimal(3.14159) == "3.1"

    def test_format_decimal_custom_digits(self):
        """Test custom decimal places."""
        assert format_decimal(3.14159, digits=2) == "3.14"
        assert format_decimal(3.14159, digits=3) == "3.142"

    def test_format_decimal_strips_trailing_zeros(self):
        """Test trailing zeros are removed."""
        assert format_decimal(3.0, digits=2) == "3"
        assert format_decimal(3.10, digits=2) == "3.1"

    def test_format_decimal_string_input(self):
        """Test string number input."""
        assert format_decimal("5.678", digits=1) == "5.7"

    def test_format_decimal_invalid(self):
        """Test invalid input returns string representation."""
        assert format_decimal("invalid") == "invalid"


class TestFormatPercentage:
    """Tests for format_percentage formatter."""

    def test_format_percentage_ratio(self):
        """Test formatting ratio (0-1) as percentage."""
        assert format_percentage(0.5) == "50%"
        assert format_percentage(0.75) == "75%"

    def test_format_percentage_already_percentage(self):
        """Test formatting value already as percentage (>1)."""
        assert format_percentage(50) == "50%"
        assert format_percentage(75.5) == "75.5%"

    def test_format_percentage_strips_trailing_zeros(self):
        """Test trailing zeros after decimal are removed."""
        assert format_percentage(0.5) == "50%"
        assert format_percentage(50.0) == "50%"

    def test_format_percentage_string_input(self):
        """Test string number input."""
        assert format_percentage("0.25") == "25%"

    def test_format_percentage_invalid(self):
        """Test invalid input returns string representation."""
        result = format_percentage("invalid")
        assert result == "invalid"


class TestFormatRuntimeMinutes:
    """Tests for format_runtime_minutes formatter."""

    def test_format_runtime_minutes_integer(self):
        """Test formatting integer minutes."""
        assert format_runtime_minutes(120) == "120 min"

    def test_format_runtime_minutes_float(self):
        """Test formatting float minutes (rounds)."""
        assert format_runtime_minutes(119.6) == "120 min"

    def test_format_runtime_minutes_with_thousands(self):
        """Test formatting large minutes with separators."""
        assert format_runtime_minutes(1500) == "1,500 min"

    def test_format_runtime_minutes_zero_or_negative(self):
        """Test zero or negative returns '-'."""
        assert format_runtime_minutes(0) == "-"
        assert format_runtime_minutes(-10) == "-"

    def test_format_runtime_minutes_string_input(self):
        """Test string number input."""
        assert format_runtime_minutes("90") == "90 min"

    def test_format_runtime_minutes_invalid(self):
        """Test invalid input returns string representation."""
        assert format_runtime_minutes("invalid") == "invalid"


class TestRenderTableFromSchema:
    """Tests for render_table_from_schema function."""

    def test_render_table_basic(self):
        """Test basic table rendering with dict items."""
        console = Console(record=True, width=120)
        schema = [
            TableSchema(name="name", header="Name", style="cyan"),
            TableSchema(name="age", header="Age", justify="right"),
        ]
        items = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]

        render_table_from_schema("Test Table", schema, items, console)

        output = console.export_text()
        assert "Test Table" in output
        assert "Alice" in output
        assert "Bob" in output
        assert "30" in output
        assert "25" in output

    def test_render_table_with_objects(self):
        """Test table rendering with object items."""
        console = Console(record=True, width=120)

        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        schema = [
            TableSchema(name="name", header="Name"),
            TableSchema(name="age", header="Age"),
        ]
        items = [Person("Alice", 30), Person("Bob", 25)]

        render_table_from_schema("People", schema, items, console)

        output = console.export_text()
        assert "People" in output
        assert "Alice" in output
        assert "Bob" in output

    def test_render_table_with_formatter(self):
        """Test table rendering with formatter functions."""
        console = Console(record=True, width=120)
        schema = [
            TableSchema(name="value", header="Value", formatter=format_money),
        ]
        items = [{"value": 1000}, {"value": 2500}]

        render_table_from_schema("Values", schema, items, console)

        output = console.export_text()
        assert "$1,000" in output
        assert "$2,500" in output

    def test_render_table_with_none_values(self):
        """Test table rendering with None values."""
        console = Console(record=True, width=120)
        schema = [
            TableSchema(name="name", header="Name"),
            TableSchema(name="value", header="Value"),
        ]
        items = [{"name": "Test", "value": None}]

        render_table_from_schema("With None", schema, items, console)

        output = console.export_text()
        assert "-" in output

    def test_render_table_with_list_values(self):
        """Test table rendering with list values."""
        console = Console(record=True, width=120)
        schema = [
            TableSchema(name="tags", header="Tags"),
        ]
        items = [{"tags": ["python", "testing", "pytest"]}]

        render_table_from_schema("Tags", schema, items, console)

        output = console.export_text()
        assert "python" in output
        assert "testing" in output
        assert "pytest" in output

    def test_render_table_with_no_wrap(self):
        """Test table rendering with no_wrap option."""
        console = Console(record=True, width=120)
        schema = [
            TableSchema(name="text", header="Text", no_wrap=True),
        ]
        items = [{"text": "Very long text that might wrap"}]

        render_table_from_schema("No Wrap", schema, items, console)

        output = console.export_text()
        assert "Very long text" in output

    def test_render_table_with_missing_attribute(self):
        """Test table rendering when object missing attribute."""
        console = Console(record=True, width=120)

        class Incomplete:
            def __init__(self):
                self.name = "Test"

        schema = [
            TableSchema(name="name", header="Name"),
            TableSchema(name="missing", header="Missing"),
        ]
        items = [Incomplete()]

        render_table_from_schema("Incomplete", schema, items, console)

        output = console.export_text()
        assert "Test" in output
        assert "-" in output  # Missing attribute shows as "-"

    def test_render_table_with_string_formatter_spec(self):
        """Test table rendering with string format spec."""
        console = Console(record=True, width=120)
        schema = [
            TableSchema(name="value", header="Value", formatter=".2f"),
        ]
        items = [{"value": 3.14159}]

        render_table_from_schema("Format Spec", schema, items, console)

        output = console.export_text()
        assert "3.14" in output

    def test_render_table_formatter_exception_handling(self):
        """Test that formatter exceptions fall back to str()."""
        console = Console(record=True, width=120)

        def bad_formatter(val):
            raise ValueError("Bad formatter")

        schema = [
            TableSchema(name="value", header="Value", formatter=bad_formatter),
        ]
        items = [{"value": "test"}]

        render_table_from_schema("Exception", schema, items, console)

        output = console.export_text()
        assert "test" in output

    def test_render_table_with_none_name(self):
        """Test table rendering with None as name (no attribute lookup)."""
        console = Console(record=True, width=120)
        schema = [
            TableSchema(name=None, header="Empty"),
        ]
        items = [{"something": "value"}]

        render_table_from_schema("None Name", schema, items, console)

        output = console.export_text()
        assert "None Name" in output
        assert "-" in output

    def test_render_table_with_unknown_formatter_type(self):
        """Test table rendering with unknown formatter type (not callable, not string)."""
        console = Console(record=True, width=120)
        schema = [
            TableSchema(name="value", header="Value", formatter=123),  # int formatter (invalid)
        ]
        items = [{"value": "test"}]

        render_table_from_schema("Unknown Formatter", schema, items, console)

        output = console.export_text()
        assert "test" in output

    def test_render_table_with_tuple_values(self):
        """Test table rendering with tuple values (like list)."""
        console = Console(record=True, width=120)
        schema = [
            TableSchema(name="items", header="Items"),
        ]
        items = [{"items": ("a", "b", "c")}]

        render_table_from_schema("Tuple", schema, items, console)

        output = console.export_text()
        assert "a" in output
        assert "b" in output
        assert "c" in output

    def test_render_table_with_list_join_exception(self):
        """Test table rendering when list join fails (objects without proper __str__)."""
        console = Console(record=True, width=120)

        class BadStr:
            def __str__(self):
                raise ValueError("Can't stringify")

        schema = [
            TableSchema(name="items", header="Items"),
        ]
        items = [{"items": [BadStr()]}]

        render_table_from_schema("Bad List", schema, items, console)

        output = console.export_text()
        # Should fall back to str(val) of the whole list
        assert "Bad List" in output


class TestRenderFromJson:
    """Tests for render_from_json function."""

    def test_render_from_json_with_dict(self):
        """Test rendering from dict input."""
        console = Console(record=True, width=120)
        data = {
            "show_summary": "A great show",
            "characters": [
                {
                    "character": "Hero",
                    "actor": "Actor Name",
                    "relationship": "Main",
                    "year_joined": "2020",
                    "description": "The hero",
                }
            ],
            "broadcast_info": [{"network": "ABC", "country": "USA", "start_year": "2020", "end_year": "2023"}],
            "production_companies": [{"name": "Company", "founded_year": "2000", "start_year": "2020", "end_year": "2023", "country": "USA"}],
        }

        render_from_json(data, console)

        output = console.export_text()
        assert "A great show" in output
        assert "Hero" in output
        assert "Actor Name" in output
        assert "ABC" in output
        assert "Company" in output

    def test_render_from_json_with_string(self):
        """Test rendering from JSON string input."""
        console = Console(record=True, width=120)
        data = json.dumps(
            {
                "summary": "Test summary",
                "characters": [],
            }
        )

        render_from_json(data, console)

        output = console.export_text()
        assert "Test summary" in output

    def test_render_from_json_invalid_json_string(self):
        """Test rendering invalid JSON string."""
        console = Console(record=True, width=120)
        data = "{ invalid json }"

        render_from_json(data, console)

        output = console.export_text()
        assert "invalid json" in output
        assert "invalid" in output.lower()

    def test_render_from_json_no_summary(self):
        """Test rendering without summary field."""
        console = Console(record=True, width=120)
        data = {"characters": []}

        render_from_json(data, console)

        output = console.export_text()
        assert "no summary" in output.lower()

    def test_render_from_json_empty_lists(self):
        """Test rendering with empty character/broadcast/company lists."""
        console = Console(record=True, width=120)
        data = {
            "show_summary": "Test",
            "characters": [],
            "broadcast_info": [],
            "production_companies": [],
        }

        render_from_json(data, console)

        output = console.export_text()
        assert "No character info" in output

    def test_render_from_json_missing_fields(self):
        """Test rendering with missing optional fields."""
        console = Console(record=True, width=120)
        data = {"show_summary": "Test"}

        render_from_json(data, console)

        output = console.export_text()
        assert "Test" in output

    def test_render_from_json_uses_year_formatter(self):
        """Test that render_from_json uses year formatter for year fields."""
        console = Console(record=True, width=120)
        data = {
            "show_summary": "Test",
            "characters": [
                {
                    "character": "Test",
                    "actor": "Actor",
                    "relationship": "Main",
                    "year_joined": "present",
                    "description": "Desc",
                }
            ],
        }

        render_from_json(data, console)

        output = console.export_text()
        assert "Present" in output

    def test_render_from_json_pretty_print_exception(self):
        """Test exception handling during JSON pretty printing."""
        console = Console(record=True, width=120)

        # Create object that can't be JSON serialized easily
        class NonSerializable:
            pass

        data = {"obj": NonSerializable(), "show_summary": "Test"}

        render_from_json(data, console)

        output = console.export_text()
        # Should fall back to str() representation
        assert "Test" in output or "NonSerializable" in output
