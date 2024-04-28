# Backup Tool

This is a simple backup tool implemented in Python using Tkinter for the graphical user interface (GUI). It allows users to select a source directory, destination directory, and optionally specify a filename for the backup. The tool then creates a ZIP archive of the source directory and saves it to the specified destination.

## Features

- **Graphical User Interface:** Provides an intuitive interface for users to select directories and initiate backups.
- **Asynchronous Backup:** Utilizes threading to perform the backup operation asynchronously, preventing the GUI from freezing during long backups.
- **Progress Tracking:** Displays progress bars and estimated remaining time during the backup process.
- **Saved Destinations:** Allows users to save frequently used destination directories for quick access.

## Usage

1. Run the `backup_tool.py` script.
2. Use the "Browse" buttons to select the source and destination directories.
3. Optionally, specify a custom filename for the backup.
4. Click the "Backup" button to start the backup process.
5. Monitor the progress bar and remaining time label for the backup status.
6. Once completed, a confirmation message will be displayed.

## Requirements

- Python 3.x
- tkinter (Included in standard Python library)

## How to Run

```bash
python backup_tool.py
```

## Contributors

- Konstantinos Pavlakis (https://github.com/konpavidis)
