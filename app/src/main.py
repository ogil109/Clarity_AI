import argparse
from datetime import datetime, timezone

from parse import find_logs, process_logs


def valid_datetime(s: str) -> datetime:
    """Returns a valid, timezone aware datetime object from a string."""
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log Parser Tool")
    parser.add_argument(
        "filename", type=str, help="The absolute path to the log file to parse"
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logs = process_logs(
        args.filename
    )  # logs is a sorted list of tuples (timestamp, host_from, host_to)
    connections = find_logs(logs, args.hostname, args.start_datetime, args.end_datetime)
    print(f"Connections to/from {args.hostname}:\n")
    for connection in connections:
        print(connection)

    print(f"\nFound {len(connections)} connections.\n")


if __name__ == "__main__":
    main()
