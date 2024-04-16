from datetime import datetime, timezone
from unittest.mock import patch

import pytest

# src included in path at pyproject.toml (see [tool.pytest.ini_options])
from main import parse_args, valid_datetime


def test_parse_args_valid_arguments():
    with patch(
        "argparse._sys.argv",
        [
            "main.py",
            "app/tests/input-test.txt",
            "2021-01-01T00:00:00.000Z",
            "2021-01-01T01:00:00.000Z",
            "Example",
        ],
    ):
        args = parse_args()
        assert args.filename == "app/tests/input-test.txt"
        assert args.start_datetime == datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert args.end_datetime == datetime(2021, 1, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert args.hostname == "Example"


def test_parse_args_empty_arguments():
    with patch("argparse._sys.argv", ["main.py"]):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_invalid_hostname_type():
    with patch(
        "argparse._sys.argv",
        [
            "main.py",
            "app/tests/input-test.txt",
            "2021-01-01T00:00:00.000Z",
            "2021-01-01T01:00:00.000Z",
            123,
        ],
    ):
        with pytest.raises(TypeError):
            parse_args()


# Invalid datetime would be caught at valid_datetime level instead of parse_args
def test_valid_datetime_invalid_datetime():
    with pytest.raises(ValueError):
        valid_datetime("Invalid datetime")
