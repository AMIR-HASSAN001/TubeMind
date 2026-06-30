from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str):
    """
    Extracts the YouTube video ID from different URL formats.
    """

    parsed_url = urlparse(url)

    # https://youtu.be/VIDEO_ID
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    # https://www.youtube.com/watch?v=VIDEO_ID
    if parsed_url.hostname in (
        "www.youtube.com",
        "youtube.com",
        "m.youtube.com",
    ):
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]

        if parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/")[2]

        if parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]

    return None


from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


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

    return None


def fetch_transcript(video_url: str):

    video_id = extract_video_id(video_url)

    api = YouTubeTranscriptApi()

    transcript_list = api.list(video_id)

    try:
        transcript = transcript_list.find_transcript(["en"])

    except:

        try:
            transcript = transcript_list.find_generated_transcript(["en"])

        except:

            transcript = next(iter(transcript_list))

    fetched = transcript.fetch()

    return " ".join(chunk.text for chunk in fetched)