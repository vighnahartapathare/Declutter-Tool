import os
import shutil
import hashlib
import time
from send2trash import send2trash
from datetime import datetime


# CONFIGURATION

TARGET_DIR = r"C:\Users\YourUsername\Downloads"  # Change this to your target folder
DAYS_OLD_THRESHOLD = 30  # Number of days to consider a file as old
ORGANIZE_BY_TYPE = True  # Whether to organize files by their extension type

# Specify the folder where the log file will be saved
LOG_DIR = r"C:\Users\YourUsername\Documents\DeclutterLogs"  # Change this to your desired log folder
LOG_FILE = os.path.join(LOG_DIR, "declutter_log.txt")  # Full path of log file

DRY_RUN = True  # Set True to test without making any changes
DUPLICATE_SCOPE_TOP_LEVEL_ONLY = False  # True = check duplicates only in the top-level directory


# HELPER FUNCTIONS


def get_file_hash(file_path):
    """Generate SHA-256 hash of a file content for duplicate detection."""
    try:
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None  # Return None if file cannot be read

def is_file_old(file_path, days_old):
    """Check if the file is older than the given threshold in days."""
    last_modified = os.path.getmtime(file_path)
    file_age_days = (time.time() - last_modified) / (60 * 60 * 24)
    return file_age_days >= days_old

def log_action(message):
    """Write a message to the log file with timestamp and print it."""
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} - {message}\n")
    print(message)

def is_log_file(file_path):
    """Check if a file path corresponds to the log file itself to avoid deleting/moving it."""
    return os.path.basename(file_path) == os.path.basename(LOG_FILE)


# MAIN CLEANUP FUNCTIONS


def find_and_remove_empty_folders(directory, summary):
    """Recursively find and remove empty folders."""
    removed = 0
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        if not dirnames and not filenames:
            try:
                if not DRY_RUN:
                    os.rmdir(dirpath)
                log_action(f"Removed empty folder: {dirpath}")
                removed += 1
            except Exception as e:
                log_action(f"Failed to remove folder {dirpath}: {e}")
    summary['empty_folders_removed'] = removed

def find_and_remove_old_files(directory, days_old, summary):
    """Find and delete files older than the specified days threshold."""
    deleted = 0
    for dirpath, _, filenames in os.walk(directory):
        for file in filenames:
            full_path = os.path.join(dirpath, file)
            if is_log_file(full_path):
                continue  # Skip the log file itself
            try:
                if is_file_old(full_path, days_old):
                    if not DRY_RUN:
                        send2trash(full_path)  # Send to recycle bin/trash
                    log_action(f"Deleted old file: {full_path}")
                    deleted += 1
            except Exception as e:
                log_action(f"Error deleting file {full_path}: {e}")
    summary['old_files_deleted'] = deleted

def find_and_remove_duplicates(directory, summary):
    """Find duplicate files by hash and remove duplicates."""
    hashes = {}
    removed = 0

    # Define directories to scan depending on scope flag
    if DUPLICATE_SCOPE_TOP_LEVEL_ONLY:
        search_dirs = [directory]
    else:
        search_dirs = [os.path.join(dp) for dp, _, _ in os.walk(directory)]

    for dirpath in search_dirs:
        for file in os.listdir(dirpath):
            full_path = os.path.join(dirpath, file)
            if not os.path.isfile(full_path) or is_log_file(full_path):
                continue
            file_hash = get_file_hash(full_path)
            if file_hash:
                if file_hash in hashes:
                    try:
                        if not DRY_RUN:
                            send2trash(full_path)
                        log_action(f"Removed duplicate: {full_path}")
                        removed += 1
                    except Exception as e:
                        log_action(f"Failed to delete duplicate {full_path}: {e}")
                else:
                    hashes[file_hash] = full_path
    summary['duplicates_removed'] = removed

def organize_files_by_type(directory, summary):
    """Move files in the top-level directory into subfolders by their file extension."""
    moved = 0
    for file in os.listdir(directory):
        full_path = os.path.join(directory, file)
        if not os.path.isfile(full_path) or is_log_file(full_path):
            continue
        ext = os.path.splitext(file)[1].lower().strip('.')
        if ext == "":
            ext = "others"
        target_folder = os.path.join(directory, ext.upper())
        os.makedirs(target_folder, exist_ok=True)
        try:
            new_path = os.path.join(target_folder, file)
            if full_path != new_path:
                if not DRY_RUN:
                    shutil.move(full_path, new_path)
                log_action(f"Moved {file} to {target_folder}")
                moved += 1
        except Exception as e:
            log_action(f"Failed to move {full_path}: {e}")
    summary['files_moved'] = moved


# RUN SCRIPT


def main():
    print(f"Scanning directory: {TARGET_DIR}")
    print(f"DRY_RUN mode: {'ON' if DRY_RUN else 'OFF'}")
    
    # Ensure the log directory exists, create if missing
    os.makedirs(LOG_DIR, exist_ok=True)
    
    summary = {
        'empty_folders_removed': 0,
        'old_files_deleted': 0,
        'duplicates_removed': 0,
        'files_moved': 0
    }
    
    # Initialize the log file (overwrite on each run)
    with open(LOG_FILE, "w") as f:
        f.write(f"--- Digital Declutter Assistant Log ---\n")

    print("Removing empty folders...")
    find_and_remove_empty_folders(TARGET_DIR, summary)

    print("Deleting old files...")
    find_and_remove_old_files(TARGET_DIR, DAYS_OLD_THRESHOLD, summary)

    print("Removing duplicate files...")
    find_and_remove_duplicates(TARGET_DIR, summary)

    if ORGANIZE_BY_TYPE:
        print("Organizing files by type (top-level only)...")
        organize_files_by_type(TARGET_DIR, summary)

    print("\nCleanup complete. Check the log file for details.\n")
    print("Summary:")
    print(f"  Empty folders removed: {summary['empty_folders_removed']}")
    print(f"  Old files deleted:     {summary['old_files_deleted']}")
    print(f"  Duplicate files removed: {summary['duplicates_removed']}")
    print(f"  Files organized:       {summary['files_moved']}")
    print("\nTip: Set DRY_RUN = True for a safe test run (no changes made).")

if __name__ == "__main__":
    main()
