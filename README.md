# Declutter Tool

## Description

Declutter Tool is a Python script designed to help users manage and organize their file system by automating common cleanup tasks. It identifies and removes empty folders, deletes files older than a specified number of days, detects and removes duplicate files, and optionally organizes files into folders based on their file extensions. The tool safely moves deleted files to the system recycle bin or trash and maintains a detailed log of all actions performed.

## Features

- Remove empty folders recursively.
- Delete files older than a configurable threshold.
- Detect and delete duplicate files based on file content.
- Organize files by their extension type into dedicated folders.
- Dry run mode for safe testing without modifying files.
- Detailed logging with customizable log file location.

## Configuration

You can customize the script behavior by modifying the following variables in the script:

| Variable                         | Description                                                                                                            | Default / Example                                  |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `TARGET_DIR`                     | The target directory to scan and clean.                                                                                | `r"C:\Users\YourUsername\Downloads"`               |
| `DAYS_OLD_THRESHOLD`             | Files older than this number of days will be deleted.                                                                  | `120`                                               |
| `ORGANIZE_BY_TYPE`               | Set to `True` to organize files by their extension type into subfolders; otherwise `False`.                            | `True`                                             |
| `LOG_DIR`                        | Directory where the log file will be saved.                                                                            | `r"C:\Users\YourUsername\Documents\DeclutterLogs"` |
| `LOG_FILE`                       | Full path of the log file (constructed using `LOG_DIR`).                                                               | Automatically set inside the script                |
| `DRY_RUN`                        | Set to `True` to perform a test run without making any actual changes.                                                 | `True`                                            |
| `DUPLICATE_SCOPE_TOP_LEVEL_ONLY` | Set to `True` to check for duplicate files only within the top-level directory; otherwise searches all subdirectories. | `False`                                            |

## Requirements

- Python 3.6 or higher
- `send2trash` Python package

Install dependencies with:

```bash
pip install send2trash
```

## Running the Code

Run the script with Python:

```bash
python declutter_tool.py
