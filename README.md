> **Note:** this repo is a fork of the original github [project](https://github.com/nzbget/PasswordDetector)
> made by @hugbug.

## Requirements

- NZBGet v23+ and Python 3.8+
- Legacy NZBGet v22: use [v2.0](https://github.com/nzbgetcom/Extension-PasswordDetector/releases/tag/v2.0) release
- Python 2.x: use legacy version 1.7 [here](https://forum.nzbget.net/viewtopic.php?f=8&t=1391&hilit=passworddetector)

# PasswordDetector

Password detection [script](https://nzbget.com/documentation/extension-scripts/) for [NZBGet](https://nzbget.com).

Authors:
- JVM <jvmed@users.sourceforge.net>
- Andrey Prygunkov <hugbug@users.sourceforge.net>
- Clinton Hall <clintonhall@users.sourceforge.net>
- get39678
- prinz2311

Detects nzbs with password protected .rar archive.

If a password is detected the download is marked as bad or paused. This status informs other scripts about failure and allows NZBGet to choose another duplicate for download (if available).

## Installation

- Download the newest version from [releases page](https://github.com/nzbgetcom/Extension-PasswordDetector/releases).
- Unpack into pp-scripts directory. Your pp-scripts directory now should have folder "PasswordDetector" with file "main.py";
- Open settings tab in NZBGet web-interface and define settings for PasswordDetector;
- Save changes and restart NZBGet.

## Options

### PassAction

Action if password found (`Pause`, `Mark Bad`).

- **Pause** allows to define password. Once resumed, password detection skipped to allow NZB to complete.
- **Mark Bad** removes the download from queue and (if option "DeleteCleanupDisk" is active) the downloaded files are deleted from disk. If duplicate handling is active (option "DupeCheck") then another duplicate is chosen for download if available.

The status "FAILURE/BAD" is passed to other scripts and informs them about failure.

## When detection happens

- **When the nzb is added to the queue (`NZB_ADDED`)**: rar-archive file lists are checked as soon as the nzb is added to the queue.
- **During download (`FILE_DOWNLOADED`)**: rar-archive volumes are checked as they arrive.
- **After download (`NZB_DOWNLOADED`)**: final check before unpacking begins.

## Credits

This script is part of the [NZBGet](https://nzbget.com) project.
