# TorDL

TorDL is a lightweight desktop application for searching torrent metadata, sending downloads directly to a Synology NAS, and monitoring their progress from a simple interface.

The project is built in Python with CustomTkinter and uses Synology Download Station as the download backend.

## Features

- Search for movies and torrent entries
- Display movie posters and metadata
- Show torrent filename and file size
- Send magnet links directly to Synology Download Station
- View active and completed downloads
- Monitor download progress
- Display current download speed
- Display Synology task status such as:
  - `downloading`
  - `paused`
  - `finished`
- Manage downloads through the Synology Download Station API
- Simple dark desktop interface

## How it works

```text
TorDL
  │
  ├── Search
  │      │
  │      ├── Torrent source
  │      └── TMDB
  │
  ├── Movie metadata
  │      ├── Title
  │      └── Poster
  │
  └── Download
         │
         ▼
  Synology Download Station
         │
         ▼
       NAS
```

TorDL does not download torrent data itself.

The application sends magnet links to Synology Download Station, which handles the actual BitTorrent download.

## Project structure

```text
TorDL/
├── main.py
├── search_torrent.py
├── download.py
├── assets/
│   ├── hard-drive-download.png
│   └── cloud-download.png
├── .env
├── LICENSE
└── README.md
```

### `main.py`

Contains the CustomTkinter user interface.

Responsibilities include:

- Search bar
- Search results
- Movie rows
- Download buttons
- Downloads page
- Progress bars
- Page navigation

### `search_torrent.py`

Handles torrent searches and returns structured results to the interface.

Handles communication with The Movie Database API.

It can be used to:

- Clean torrent filenames
- Identify movies
- Retrieve official movie titles
- Retrieve poster URLs


Example result:

```python
{
    "movie_title": "Example Movie",
    "torrent_title": "Example.Movie.2026.1080p...",
    "size": "2.4 GB",
    "poster_url": "https://image.tmdb.org/...",
    "magnet": "magnet:?xt=urn:btih:..."
}
```

### `download.py`

Handles communication with the Synology Download Station API.

Main responsibilities:

```python
add_download()
get_downloads()
pause_download()
resume_download()
delete_download()
```

Download Station tasks can return information such as:

```python
{
    "id": "dbid_33",
    "title": "Example Movie",
    "status": "downloading",
    "size": 1992718106,
    "downloaded": 397834010,
    "speed": 11760799,
    "progress": 19.96
}
```

## Requirements

TorDL currently uses:

```text
Python 3.12+
CustomTkinter
Pillow
Requests
python-dotenv
```

Install the dependencies with:

```bash
pip install customtkinter pillow requests python-dotenv
```



## Configuration

Create a `.env` file in the root directory.

Example:

```env
TMDB_TOKEN=your_tmdb_token
TMDB_API_KEY=your_tmdb_api_key

NAS_URL=https://192.168.1.63:5001
NAS_USERNAME=your_username
NAS_PASSWORD=your_password
```

Do not commit this file to Git.

Add it to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.DS_Store
```

## Running TorDL

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Launch TorDL:

```bash
python main.py
```

## Synology setup

TorDL requires:

- A Synology NAS
- DSM
- Download Station installed
- Network access to the NAS
- A Synology account authorized to use Download Station

The application communicates with Synology through the DSM Web API.

For local development, the NAS may use a self-signed HTTPS certificate.

Ideally, use a valid certificate rather than permanently disabling TLS certificate verification.

## Downloads page

TorDL periodically requests the current Download Station task list.

The interface can display:

```text
Movie title
Status
Progress
Download speed
```

Example:

```text
Example Movie

████████████████░░░░░░░░

64.3%

downloading
11.2 MB/s
```

The downloads view can be refreshed periodically using CustomTkinter/Tkinter's:

```python
root.after(...)
```

This allows the application to update download progress without restarting the interface.

## TMDB

TorDL can use TMDB to turn filenames such as:

```text
Harry Potter And The Goblet Of Fire (2005) [2160p] [4K] [BluRay]
```

into cleaner metadata such as:

```text
Harry Potter and the Goblet of Fire
2005
Poster
```

TMDB is used only for movie and TV metadata.

## Security

Recommended practices:

- Do not hardcode NAS passwords in source files
- Store credentials in `.env`
- Do not expose DSM directly to the public Internet unnecessarily
- Prefer LAN or VPN access for the Synology API
- Use a dedicated Synology account with only the permissions TorDL needs
- Keep DSM and Download Station updated
- Use HTTPS

## Legal use

TorDL is intended for downloading content that you are legally authorized to access, including public-domain, freely distributed, open-source, or otherwise authorized content.

The application itself does not host or distribute media files.

## Current status

TorDL is currently under development.

Current focus:

- Search interface
- TMDB poster integration
- Synology Download Station integration
- Download progress monitoring
- Simple desktop UI

Possible future improvements:

- Pause and resume buttons
- Delete task button
- Better download status indicators
- Download history
- TV series support
- Automatic refresh improvements
- Packaging as a native macOS `.app`