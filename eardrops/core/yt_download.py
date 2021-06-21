import json
import os
import re

import eyed3
import youtube_dl


def process_input(lines):
    urls = [line.strip() for line in lines if 'youtube' in line]
    url_data_objects = []
    for url in urls:
        video_id = re.search('((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)', url).group(0)
        url_data_objects.append({
            'url': url,
            'video_id': video_id,
            'clean_url': 'https://www.youtube.com/watch?v={}'.format(video_id)
        })
    return url_data_objects


def download_mp3(url, dir_path):
    ydl_opts = {
        'nocheckcertificate': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '{}/%(id)s.%(ext)s'.format(dir_path),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url, download=True)

    return video_info


def get_info(url):
    ydl_opts = {
        'nocheckcertificate': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url, download=False)

    return video_info
