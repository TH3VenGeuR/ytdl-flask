from pytube import Playlist, YouTube
from pytube.exceptions import VideoUnavailable


def get_video_from_playlist(url):
    try:
        playlist = Playlist(url)
        url_list = []
        list_video = []
        for url_video in playlist.video_urls:
            list_video.append(get_video(url_video))
        print(list_video)
        return list_video
    except VideoUnavailable:
        return None


def get_video(url):
    try:
        video = YouTube(url)
        stream = video.streams.filter(progressive=True, file_extension='mp4')
        saudio = video.streams.filter(only_audio=True).first()
        thumbnail = video.thumbnail_url
        list_url_dl = []
        list_resolution = []
        title = video.title
        list_url_dl.append(saudio.url)
        list_resolution.append("Audio")
        for video in stream:
            list_url_dl.append(video.url)
            list_resolution.append(video.resolution)
        list_video = [list_resolution, list_url_dl]
        list_video = list(map(list, zip(*list_video)))  # transpose
        return list_video, thumbnail, title
    except VideoUnavailable:
        return None
