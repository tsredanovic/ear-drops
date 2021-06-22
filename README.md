# Ear Drops

**Ear Drops** is a very opinionated music management platform written in Python using the [Django Web Framework](https://www.djangoproject.com/).


## Features

- Importing music from local files
- Downloading music from youtube
- Managing songs, artists and albums
- Web UI for browsing


## Requirements

- [Python 3.5+](https://www.python.org/downloads/)
- [ffmpeg](https://www.ffmpeg.org/download.html)
- other requirements are Python packages listed in `requirements.txt` file


## First Time Installation

1. Clone this repository
2. Create a python virtual environment
```bash
python3 -m venv venv
```
3. Activate the created virtual environment
```bash
source venv/bin/activate
```
4. Install requirements
```bash
pip install -r requirements.txt
```
5. Run migrations (this will create a `sqlite` database with appropriate tables)
```bash
python eardrops/manage.py migrate
```


## Creating users
1. Python virtual environment must be active
```bash
source venv/bin/activate
```
2. Run the `createsuperuser` command
```bash
python eardrops/manage.py createsuperuser
```
3. Enter desired user data (`username`, `email`, `password`) and confirm


## Running
1. Python virtual environment must be active
```bash
source venv/bin/activate
```
2. Run `runserver` command (will run on port 8000 by default)
```bash
python eardrops/manage.py runserver --noreload
```
3. Navigate to `http://127.0.0.1:8000/admin/` in your favourite browser
4. Log in with previously created user
5. Browse


## Commands

### Import Local Songs - `import_songs`

Recursively searches provided `dir_path` for `.mp3` files. 
Imports them with (`artist`, `album`, `title`) tags found on each file 
or prompts user for providing (`artist`, `title`) tags if not found.

#### Arguments
`--dir_path` : Directory from which files will be imported

#### Example Call
```bash
python eardrops/manage.py import_songs --dir_path "/path/to/music/dir/"
```

### Download Youtube Songs - `yt_download`

Parses a file provided with `file_path` for valid, youtube URLs (skipps already downloaded URLs).
Downloads audio from all provided URLs and fetches youtube metadata for each download. 
Fills (`artist`, `album`, `title`) tags from metadata or prompts user for (`artist`, `title`) tags if not found, asks for confirmation on each fill.
Shows summary of downloads and asks for confirmation before import.

#### Arguments
`--file_path` : File containg links (separated by linebreaks) to youtube videos from which audio will be downloaded

#### Example Call
```bash
python eardrops/manage.py yt_download --file_path "/path/to/file/youtube_urls.txt"
```


## Disclaimer

This code is hosted for legal uses only, such as downloading content you own the rights to but no longer have a local copy of, downloading content under a permissive license, educational use, etc.
