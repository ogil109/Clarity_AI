from datetime import datetime, timezone

from parse import find_logs, parse_log_line, process_logs


def test_parse_log_line():
    log_line = "1617249600000 host1 host2"
    # Timestamp in ms, so divide by 1000.
    expected_timestamp = datetime.fromtimestamp(1617249600, timezone.utc)
    expected_host_from = "host1"
    expected_host_to = "host2"
    result = parse_log_line(log_line)
    assert result == (expected_timestamp, expected_host_from, expected_host_to)


def test_process_logs():
    log_lines = "app/tests/input-test.txt"
    # Sorting and parsing is expected
    expected_result = [
        (datetime.fromtimestamp(1565647204.351, timezone.utc), "Aadvik", "Matina"),
        (datetime.fromtimestamp(1565647205.599, timezone.utc), "Keimy", "Dmetri"),
        (datetime.fromtimestamp(1565647212.986, timezone.utc), "Tyreonna", "Rehgan"),
        (datetime.fromtimestamp(1565647228.897, timezone.utc), "Heera", "Eron"),
        (datetime.fromtimestamp(1565647246.869, timezone.utc), "Jeremyah", "Morrigan"),
        (datetime.fromtimestamp(1565647247.17, timezone.utc), "Khiem", "Tailee"),
    ]
    result = process_logs(log_lines)
    assert result == expected_result


def test_find_logs():
    logs = [
        (datetime.fromtimestamp(1565647204.351, timezone.utc), "Aadvik", "Matina"),
        (datetime.fromtimestamp(1565647205.599, timezone.utc), "Keimy", "Dmetri"),
        (datetime.fromtimestamp(1565647212.986, timezone.utc), "Tyreonna", "Rehgan"),
        (datetime.fromtimestamp(1565647228.897, timezone.utc), "Heera", "Eron"),
        (datetime.fromtimestamp(1565647246.869, timezone.utc), "Jeremyah", "Morrigan"),
        (datetime.fromtimestamp(1565647247.17, timezone.utc), "Khiem", "Tailee"),
    ]
    expected_result = ["Matina"]
    result = find_logs(
        logs,
        "Aadvik",
        datetime.fromtimestamp(1565647204.351, timezone.utc),
        datetime.fromtimestamp(1565647247.17, timezone.utc),
    )
    assert result == expected_result
