import pytest

from youtube_detector import find_youtube_video


VIDEO_ID = "eiKEhwPUGY0"


def test_finds_embed_url():
    html = f'<iframe src="https://www.youtube.com/embed/{VIDEO_ID}">'

    results = find_youtube_video(html, VIDEO_ID)

    assert any(result["type"] == "youtube-embed" for result in results)


def test_finds_embed_url_without_scheme():
    html = f'<iframe src="//www.youtube.com/embed/{VIDEO_ID}">'

    results = find_youtube_video(html, VIDEO_ID)

    assert any(result["type"] == "youtube-embed" for result in results)


def test_does_not_treat_similar_domain_as_youtube():
    html = f'<iframe src="https://notyoutube.com/embed/{VIDEO_ID}">'

    results = find_youtube_video(html, VIDEO_ID)

    assert not any(result["type"] == "youtube-embed" for result in results)


def test_finds_watch_url_with_video_parameter_after_another_parameter():
    html = f'<a href="https://www.youtube.com/watch?feature=share&v={VIDEO_ID}">'

    results = find_youtube_video(html, VIDEO_ID)

    assert any(result["type"] == "youtube-watch" for result in results)


def test_watch_value_stops_at_video_id():
    html = f'<a href="https://www.youtube.com/watch?v={VIDEO_ID}&t=10">'

    results = find_youtube_video(html, VIDEO_ID)

    watch_result = next(
        result for result in results if result["type"] == "youtube-watch"
    )
    assert watch_result["value"] == f"https://www.youtube.com/watch?v={VIDEO_ID}"


def test_finds_watch_url_with_html_encoded_parameter_separator():
    html = (
        f'<a href="https://www.youtube.com/watch?feature=share'
        f'&amp;v={VIDEO_ID}">'
    )

    results = find_youtube_video(html, VIDEO_ID)

    assert any(result["type"] == "youtube-watch" for result in results)


def test_finds_nocookie_embed_url():
    html = f'<iframe src="https://www.youtube-nocookie.com/embed/{VIDEO_ID}">'

    results = find_youtube_video(html, VIDEO_ID)

    assert any(result["type"] == "youtube-nocookie" for result in results)


def test_finds_youtu_be_url():
    html = f'<a href="https://youtu.be/{VIDEO_ID}">'

    results = find_youtube_video(html, VIDEO_ID)

    assert any(result["type"] == "youtu-be" for result in results)


def test_finds_standalone_video_id():
    html = f'<div data-video="{VIDEO_ID}">'

    results = find_youtube_video(html, VIDEO_ID)

    assert {"type": "id", "value": VIDEO_ID} in results


def test_returns_empty_list_when_no_video_is_present():
    assert find_youtube_video("<p>nada aqui</p>", VIDEO_ID) == []


@pytest.mark.parametrize(
    "html",
    [
        f"<div>X{VIDEO_ID}</div>",
        f"<div>{VIDEO_ID}X</div>",
        f"<div>_{VIDEO_ID}</div>",
        f"<div>{VIDEO_ID}_</div>",
        f"<div>-{VIDEO_ID}</div>",
        f"<div>{VIDEO_ID}-</div>",
    ],
)
def test_does_not_find_id_with_adjacent_id_character(html):
    results = find_youtube_video(html, VIDEO_ID)

    assert results == []


def test_deduplicates_repeated_occurrences():
    link = f'<a href="https://youtu.be/{VIDEO_ID}">'
    html = link + link

    results = find_youtube_video(html, VIDEO_ID)

    assert len(results) == len({(result["type"], result["value"]) for result in results})
    assert sum(result["type"] == "youtu-be" for result in results) == 1


@pytest.mark.parametrize("invalid_video_id", ["", "short", "eiKEhwPUGY0!"])
def test_rejects_invalid_video_id(invalid_video_id):
    with pytest.raises(ValueError):
        find_youtube_video("<p>sem vídeo</p>", invalid_video_id)