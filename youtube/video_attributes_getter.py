from urllib.parse import urlparse, parse_qs


def extract_video_id(url):
    # Разбор URL
    parsed_url = urlparse(url)

    if parsed_url.hostname == 'www.youtube.com':
        # Это стандартный URL, используем query
        query_params = parse_qs(parsed_url.query)
        return query_params.get('v', [None])[0]
    elif parsed_url.hostname == 'youtu.be':
        # Это короткий URL, берем последнюю часть пути
        return parsed_url.path[1:]  # Пропустим слэш
    else:
        return None


def get_video_url(video_id):
    base_url = "https://www.youtube.com/watch?v="
    video_url = base_url + video_id
    return video_url
