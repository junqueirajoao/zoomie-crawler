import re


def find_youtube_video(html, video_id):
    valid_id = isinstance(video_id, str) and re.fullmatch(
        r"[A-Za-z0-9_-]{11}", video_id
    )
    if not valid_id:
        raise ValueError(
            "video_id must be exactly 11 characters: letters, digits, '_' or '-'"
        )

    escaped_id = re.escape(video_id)
    patterns = (
        (
            "youtube-watch",
            rf"(?<![A-Za-z0-9.-])(?:https?://)?(?:www\.)?youtube\.com/watch\?"
            rf"(?:[^&\"'<>#\s]*&(?:amp;)?)*v={escaped_id}(?![A-Za-z0-9_-])",
        ),
        (
            "youtube-embed",
            rf"(?<![A-Za-z0-9.-])(?:https?://)?(?:www\.)?youtube\.com/embed/"
            rf"{escaped_id}(?![A-Za-z0-9_-])",
        ),
        (
            "youtube-nocookie",
            rf"(?<![A-Za-z0-9.-])(?:https?://)?(?:www\.)?youtube-nocookie\.com/embed/"
            rf"{escaped_id}(?![A-Za-z0-9_-])",
        ),
        (
            "youtu-be",
            rf"(?<![A-Za-z0-9.-])(?:https?://)?(?:www\.)?youtu\.be/"
            rf"{escaped_id}(?![A-Za-z0-9_-])",
        ),
        ("id", rf"(?<![A-Za-z0-9_-]){escaped_id}(?![A-Za-z0-9_-])"),
    )

    occurrences = (
        (kind, match.group(0))
        for kind, pattern in patterns
        for match in re.finditer(pattern, html)
    )
    unique_occurrences = dict.fromkeys(occurrences)
    return [
        {"type": kind, "value": value}
        for kind, value in unique_occurrences
    ]