from pytube.extract import video_id, playlist_id
from pytube.exceptions import RegexMatchError


def get_type(uri):
    try:
        id_video = video_id(uri)
        type_video = 'video'
    except RegexMatchError:
        try:
            id_video = playlist_id(uri)
            type_video = 'playlist'
        except RegexMatchError:
            id_video = None
            type_video = None
    return type_video
