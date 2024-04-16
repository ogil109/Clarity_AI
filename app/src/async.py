import argparse
import asyncio
from collections import Counter
from datetime import datetime, timedelta, timezone

import aiofiles
from parse import parse_log_line
from sortedcontainers import SortedList

# Create a global sorted list to store log entries by timestamp.
logs = SortedList(key=lambda x: x[0])


async def process_logs_continuous(pathname):
    """
    Processes logs continuously from a specified file path asynchronously, writing to the global logs list.

    Args:
        pathname (str): The path to the log file to be processed.

    Raises:
        FileNotFoundError: If the specified file is not found.
        IOError: If there is an error reading the file.
    """
    try:
        # Reading file asyncronously to avoid blocking the main logging thread.
        async with aiofiles.open(pathname, "r", encoding="utf-8") as file:
            while True:
                line = await file.readline()
                if not line:
                    await asyncio.sleep(5)  # 5 seconds between checks
                    continue
                log_entry = parse_log_line(line)
                logs.add(log_entry)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {pathname}") from e
    except IOError as e:
        raise IOError(f"Error reading file: {pathname}") from e


def prune_logs() -> None:
    # Remove log entries older than two hours to keep memory usage low.
    two_hours_ago = datetime.now(timezone.utc) - timedelta(hours=2)
    while logs and logs[0][0] < two_hours_ago:
        logs.pop(0)


def generate_report(host) -> None:
    """
    Generate a report of connections to and from a given host in the last hour and the host with the most connections.

    Args:
        host (str): The hostname to generate the report for.

    Returns:
        None: This function does not return anything. It prints the connections to and from the given host in the last hour.
    """
    now = datetime.now(timezone.utc)
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    # Filter logs based on the start and end timestamps before iteration (to reduce list size).
    recent_logs = [log for log in logs if one_hour_ago <= log[0] <= now]
    # Avoid duplicates by using sets.
    connections_to = {log[2] for log in recent_logs if log[1] == host}
    connections_from = {log[1] for log in recent_logs if log[2] == host}
    # Determine host with most connections.
    connection_counts = Counter(log[1] for log in recent_logs)
    most_active_host, most_active_count = (
        connection_counts.most_common(1)[0] if connection_counts else (None, 0)
    )

    # Report
    print(f"Connections to {host} in the last hour: {connections_to}")
    print(f"Connections from {host} in the last hour: {connections_from}")
    if most_active_host:
        print(
            f"Host with the most connections: {most_active_host} with {most_active_count} connections"
        )
    else:
        print("No active connections in the last hour.")


async def periodic_report(host, interval=3600):
    while True:
        await asyncio.sleep(interval)
        prune_logs()
        generate_report(host)


def parse_args():
    """Defines arguments for filename and hostname to monitor."""
    parser = argparse.ArgumentParser(description="Continuously monitor log files.")
    parser.add_argument(
        "filename", type=str, help="Path to the log file being written."
    )
    parser.add_argument("hostname", type=str, help="Hostname to monitor.")

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


async def main():
    args = parse_args()
    log_task = asyncio.create_task(process_logs_continuous(args.filename))
    report_task = asyncio.create_task(periodic_report(args.hostname))
    await asyncio.gather(log_task, report_task)


if __name__ == "__main__":
    asyncio.run(main())
