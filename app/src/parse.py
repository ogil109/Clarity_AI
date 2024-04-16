from datetime import datetime, timezone


def parse_log_line(line) -> tuple[datetime, str, str]:
    parts = line.strip().split()
    timestamp = datetime.fromtimestamp(
        int(parts[0]) / 1000, timezone.utc
    )  # UNIX timestamp in ms, so divide by 1000.
    host_from, host_to = parts[1], parts[2]
    return timestamp, host_from, host_to


def process_logs(pathname):
    """
    Processes logs from a specified file path.

    Args:
        pathname (str): The path to the log file to be processed.

    Returns:
        list: A list of tuples containing the parsed timestamps, host_from, and host_to.
              The list is sorted by parsed timestamp (datetime).

    Raises:
        FileNotFoundError: If the specified file is not found.
        IOError: If there is an error reading the file.
    """
    try:
        with open(pathname, "r", encoding="utf-8") as file:
            lines = []
            for line in file:
                timestamp, host_from, host_to = parse_log_line(line)
                lines.append((timestamp, host_from, host_to))
        # Sort by parsed timestamp (datetime).
        lines.sort(key=lambda x: x[0])
        return lines
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {pathname}") from e
    except IOError as e:
        raise IOError(f"Error reading file: {pathname}") from e


def find_logs(logs_list, host, start_time, end_time) -> list:
    # Filter logs based on the start and end timestamps before iteration (to reduce list size) and pop timestamp from every tuple.
    filtered_logs = [
        (host_from, host_to)
        for timestamp, host_from, host_to in logs_list
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
