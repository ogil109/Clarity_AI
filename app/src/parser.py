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
    timestamp = datetime.fromtimestamp(int(parts[0]), timezone.utc).isoformat(
        timespec="seconds"
    )
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
    with open(filename, "r", encoding="utf-8") as file:
        lines = []
        for line in file:
            timestamp, host_from, host_to = parse_log_line(line)
            lines.append((timestamp, host_from, host_to))

    # Built-in Timsort is fast enough in nearly sorted lists (using insertion sort).
    lines.sort(key=lambda x: x[0])
    return lines


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

    # Avoid duplicates using set.
    connected_hosts = set()

    for timestamp, host_from, host_to in filtered_logs:
        if start_time <= timestamp <= end_time:
            # Manage bidirectional connections requirement.
            if host_from == host:
                connected_hosts.add(host_to)
            elif host_to == host:
                connected_hosts.add(host_from)

    return list(connected_hosts)
