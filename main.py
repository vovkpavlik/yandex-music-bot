import os

from environs import Env
from yandex_music.client import Client


def create_folders(folder, artists):    
    if not os.path.exists(folder):
        os.mkdir(folder)

    for artist in artists:
        os.makedirs(f"{folder}/{artist}", exist_ok=True)
    

def get_name_artist(client):    
    
    likes_track_list = client.users_likes_tracks()

    artists = []

    for track in likes_track_list:
        desc_track = track.fetch_track()
        name_artist = desc_track["artists"][0]["name"]
        artists.append(name_artist)

    return artists


def save_music(client, folder, extension):  

    likes_track_list = client.users_likes_tracks()
    
    for track in likes_track_list:
        desc_track = track.fetch_track()
        name_track = desc_track["title"]
        name_artist = desc_track["artists"][0]["name"]
        title = f"{name_artist} - {name_track}"
        path = f"{folder}/{name_artist}"

        track.fetch_track().download(f"{path}/{title}{extension}")


if __name__ == "__main__":
   
    env = Env()
    env.read_env()

    yandex_login = env.str("YANDEX_LOGIN")
    yandex_password = env.str("YANDEX_PASSWORD")

    client = Client.from_credentials(yandex_login, yandex_password)

    extension = ".mp3"
    all_music_folder = "music"

    create_folders(all_music_folder, get_name_artist(client))
    save_music(client, all_music_folder, extension)
