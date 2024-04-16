import argparse
from datetime import datetime, timezone

from parse import find_logs, process_logs


def valid_datetime(s: str) -> datetime:
    """Returns a valid, timezone aware datetime object from a string (ISO format)."""
    try:
        return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
    except ValueError as e:
        raise ValueError(f"Invalid datetime format: {s}") from e


def parse_args() -> argparse.Namespace:
    """
    Defines arguments for filename, start_datetime, end_datetime, and hostname. Accepts strings and parses timestamp with valid datetime().
    """
    parser = argparse.ArgumentParser(description="Log Parser Tool")
    parser.add_argument(
        "filename",
        type=str,
        help="The absolute path to the log file to parse",
    )
    parser.add_argument(
        "start_datetime",
        type=valid_datetime,
        help="Start datetime in ISO format (e.g., 2021-01-01T00:00:00.000Z)",
    )
    parser.add_argument(
        "end_datetime",
        type=valid_datetime,
        help="End datetime in ISO format (e.g., 2021-01-01T01:00:00.000Z)",
    )
    parser.add_argument("hostname", type=str, help="Hostname to find connections for")

    # Handle invalid input
    args = None
    while args is None:
        try:
            args = parser.parse_args()
        except TypeError as e:
            args = None
            raise TypeError("Invalid input. Please try again.") from e

    if not any(vars(args)):
        raise SystemExit("No arguments provided. Exiting.")

    return args


def main() -> None:
    args = parse_args()
    logs = process_logs(args.filename)
    connections = find_logs(logs, args.hostname, args.start_datetime, args.end_datetime)
    print(
        f"\nConnections to/from {args.hostname} between {args.start_datetime} and {args.end_datetime}:\n"
    )
    for connection in connections:
        print(connection)

    print(f"\nFound {len(connections)} connections.\n")


if __name__ == "__main__":
    main()
