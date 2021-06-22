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
`--dir_path` : Directory from which files will be imported.

#### Example Call
```bash
python manage.py import_songs --dir_path "/path/to/music/dir/"
```

### TODO

## Disclaimer

This code is hosted for legal uses only, such as downloading content you own the rights to but no longer have a local copy of, downloading content under a permissive license, educational use, etc.
