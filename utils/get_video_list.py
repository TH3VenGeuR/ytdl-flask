from utils.get_video_type import get_type
from utils.get_videos import get_video_from_playlist, get_video


def get_video_list(url):
    type_video = get_type(url)
    if type_video == 'playlist':
        return get_video_from_playlist(url)
    elif type_video == 'video':
        return get_video(url)
    else:
        return None
