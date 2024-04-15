import sys
from datetime import datetime, timezone


def parse_log_line(line) -> tuple[datetime, str, str]:
    """
    Parses a log line and extracts the timestamp, host_from, and host_to information.

    Parameters:
    line (str): A string representing a log line.

    Returns:
    tuple: Containing extracted timestamp (datetime), host_from (str), and host_to (str).
    """
    parts = line.strip().split()
    timestamp = datetime.fromtimestamp(
        int(parts[0]) / 1000, timezone.utc
    )  # UNIX timestamp in ms, so divide by 1000.
    host_from, host_to = parts[1], parts[2]
    return timestamp, host_from, host_to


def process_logs(pathname) -> list:
    """
    Processes log entries from a specified file.

    Opens the file, reads and parses each line, builds a list of tuples and sorts it based on timestamp.

    Parameters:
    filename (str): The name of the file containing log entries.

    Returns:
    list: A list of tuples, each containing timestamp, host_from, and host_to from the log file.
    """
    try:
        with open(pathname, "r", encoding="utf-8") as file:
            lines = []
            for line in file:
                timestamp, host_from, host_to = parse_log_line(line)
                lines.append((timestamp, host_from, host_to))

        # Sort by parsed datetime (ISO format).
        lines.sort(key=lambda x: x[0])
        return lines
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    except IOError:
        print("Error reading file.")
        sys.exit(1)


def find_logs(logs, host, start_time, end_time) -> list:
    """
    Filters logs based on timestamps and avoids duplicates for bidirectional connections.

    Parameters:
    logs (list): List of tuples containing timestamp, host_from, and host_to.
    host (str): The host to find connections for.
    start_time (datetime): The start timestamp to filter logs.
    end_time (datetime): The end timestamp to filter logs.

    Returns:
    list: List of connected hosts to the specified host.
    """
    # Filter logs based on the start and end timestamps before iteration (to reduce list size).
    filtered_logs = [
        (host_from, host_to)
        for timestamp, host_from, host_to in logs
        if start_time <= timestamp <= end_time
    ]

    # Avoid duplicates by using a set.
    connected_hosts = set()

    for host_from, host_to in filtered_logs:
        # Manage bidirectional connections requirement.
        if host_from == host:
            connected_hosts.add(host_to)
        elif host_to == host:
            connected_hosts.add(host_from)

    return list(connected_hosts)
