import sys
from datetime import datetime, timezone


def parse_log_line(line):
    """
    A function to parse a log line and extract timestamp, host_from, and host_to.

    UNIX timestamp is parsed to ISO format to match CLI args.

    Parameters:
    line (str): The log line to be parsed.

    Returns:
    tuple: Containing ISO timestamp (datetime), host_from (str), and host_to (str).
    """
    parts = line.strip().split()
    timestamp = datetime.fromtimestamp(
        int(parts[0]) / 1000, timezone.utc
    )  # UNIX timestamp in ms, so divide by 1000.
    host_from, host_to = parts[1], parts[2]
    return timestamp, host_from, host_to


def process_logs(filename) -> list:
    """
    A function to process logs from a file, extract timestamp, host_from, and host_to, sort them, and return the sorted list.

    Parameters:
    filename (str): The name of the file to process.

    Returns:
    list: A list of tuples containing timestamp (datetime), host_from (str), and host_to (str).
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = []
            for line in file:
                timestamp, host_from, host_to = parse_log_line(line)
                lines.append((timestamp, host_from, host_to))

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
    A function to find connected hosts within a specified time range for a given host.

    Parameters:
    logs (list): A list of tuples containing timestamp, host_from, and host_to.
    host (str): The host for which connections need to be found.
    start_time (datetime): The start time of the range to consider.
    end_time (datetime): The end time of the range to consider.

    Returns:
    list: A list of connected hosts within the specified time range for the given host.
    """
    # Filter logs based on the start and end timestamps before iteration.
    filtered_logs = [
        (timestamp, host_from, host_to)
        for timestamp, host_from, host_to in logs
        if start_time <= timestamp <= end_time
    ]

    connected_hosts = []

    for timestamp, host_from, host_to in filtered_logs:
        if start_time <= timestamp <= end_time:
            # Manage bidirectional connections requirement.
            if host_from == host:
                connected_hosts.append(host_to)
            elif host_to == host:
                connected_hosts.append(host_from)

    return list(connected_hosts)
