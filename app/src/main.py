import argparse
from datetime import datetime

from app.src.parser import find_logs, process_logs


def datetime_from_iso(s) -> datetime:
    return datetime.fromisoformat(s)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log Parser Tool")
    parser.add_argument("filename", type=str, help="The log file to parse")
    parser.add_argument(
        "start_datetime",
        type=datetime_from_iso,
        help="Start datetime in ISO format (e.g., 2021-01-01T00:00:00)",
    )
    parser.add_argument(
        "end_datetime",
        type=datetime_from_iso,
        help="End datetime in ISO format (e.g., 2021-01-01T01:00:00)",
    )
    parser.add_argument("hostname", type=str, help="Hostname to find connections for")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logs = process_logs(
        args.filename
    )  # logs is a sorted list of tuples (timestamp, host_from, host_to)
    connections = find_logs(logs, args.hostname, args.start_datetime, args.end_datetime)
    print("Connected hosts:", connections)


if __name__ == "__main__":
    main()
