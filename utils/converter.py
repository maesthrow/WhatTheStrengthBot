from datetime import datetime


def to_date_time(date_str: str):
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
