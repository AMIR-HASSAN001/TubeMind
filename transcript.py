import os
import re
import glob
import tempfile
from urllib.parse import urlparse, parse_qs

from yt_dlp import YoutubeDL


def extract_video_id(url: str):
    parsed_url = urlparse(url)

    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    if parsed_url.hostname in (
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
    ):

        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]

        if parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/")[2]

        if parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]

    return None


def clean_vtt(text):
    lines = []

    for line in text.splitlines():

        line = line.strip()

        if (
            not line
            or line == "WEBVTT"
            or "-->" in line
            or line.startswith("Kind:")
            or line.startswith("Language:")
        ):
            continue

        line = re.sub(r"<[^>]+>", "", line)

        if line not in lines:
            lines.append(line)

    return " ".join(lines)


def fetch_transcript(video_url: str):

    with tempfile.TemporaryDirectory() as temp_dir:

        ydl_opts = {
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["en"],
            "subtitlesformat": "vtt",
            "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        subtitle_files = glob.glob(os.path.join(temp_dir, "*.vtt"))

        if not subtitle_files:
            raise Exception("No English subtitles found for this video.")

        with open(subtitle_files[0], "r", encoding="utf-8") as f:
            transcript = f.read()

    return clean_vtt(transcript)