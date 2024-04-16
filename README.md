# Case 1 
Given the name of a file, an init_datetime, an end_datetime, and a Hostname, return:
- A list of hostnames connected to the given host during the given period.

## Usage

```bash
python app/src/main.py "pathname" "ISO datetime" "ISO datetime" "hostname"
```
### Example

```bash
python app/src/main.py "input-file-10000.txt" "2019-08-12" "2019-08-14" "Matina"
```

# Case 2
Parse previously written log files and terminate or collect input from a new log file while it's being written and run indefinitely.

The script will output, once every hour:
- A list of hostnames connected to a given (configurable) host during the last hour.
- A list of hostnames received connections from a given (configurable) host during the last hour.
- The hostname that generated most connections in the last hour.

## Usage

```bash
python app/src/async "pathname to log file being written" "hostname to monitor"
```

### Example

```bash
python app/src/async.py "sample-log-file.txt" "Matina"
```

# Key features
## CPU and memory efficient
- logs are filtered by timestamp before searching them in parse.py.
- SortedList used to implement binary search, getting to O(log N) vs O(N).
- Pruning every 2h to limit list size (instead of printing results, a log file could be in place to save results).
## Parallelism
- File reading is performed asynchronously with aiofiles to avoid interrupting the main thread.

# Final considerations
Tests for the use case 1 are in app/tests. Case 2 is not tested.
