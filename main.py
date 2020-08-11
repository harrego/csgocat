import dbus
import time
import sys
import os
import subprocess
import hashlib
import argparse
from dataclasses import dataclass
from enum import Enum

# MARK: csgo related

def xdostring(s):
  for c in s:
    if c == " ":
        subprocess.call(["xdotool", "key", "space"])
    elif c == ":":
        subprocess.call(["xdotool", "key", "colon"])
    else:
        subprocess.call(["xdotool", "key", c])

def csgo_say(msg):
    subprocess.call(["xdotool", "key", "grave"])
    xdostring("say " + msg)
    subprocess.call(["xdotool", "key", "Return"])
    subprocess.call(["xdotool", "key", "grave"])

def multiline_csgo_say(msgs):
    for msg in msgs:
        csgo_say(msg)
        time.sleep(0.5)

# MARK: song related

class Jukebox(Enum):
    Spotify = "org.mpris.MediaPlayer2.spotify"
    Rhythmbox = "org.mpris.MediaPlayer2.rhythmbox"

class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def hash(self):
        song_str = f"{self.title}/{self.artist}".encode("utf-8")
        hash_str = hashlib.sha1(song_str).hexdigest()
        return hash_str

    def formatted(self, jukebox):
        jukebox_str = ""
        if jukebox is not None:
            jukebox_str = f" on {jukebox.name}"
        return f"{self.title} by {self.artist}{jukebox_str}"

SONGHASH_DIR = "/tmp/songhash"
USER_JUKEBOX = Jukebox.Spotify

def current_song(jukebox):
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object(jukebox.value, "/org/mpris/MediaPlayer2")

    spotify_props = dbus.Interface(spotify_bus, "org.freedesktop.DBus.Properties")
    metadata = spotify_props.Get("org.mpris.MediaPlayer2.Player", "Metadata")

    return Song(metadata["xesam:title"], metadata["xesam:artist"][0])

def write_hash_cache(hash_str):
    with open(SONGHASH_DIR, "w") as name_file:
        name_file.write(hash_str)

def read_hash_cache():
    if not os.path.isfile(SONGHASH_DIR):
        return True
    with open(SONGHASH_DIR, "r") as hash_file:
        read_hash = hash_file.read()
        return read_hash

def song_check(song):
    new_song_hash = song.hash()
    if read_hash_cache() != new_song_hash:
        write_hash_cache(new_song_hash)
        return True
    else:
        return False

# MARK: main loop

time.sleep(5)
while True:
    now_playing = current_song(USER_JUKEBOX)
    if song_check(now_playing):
        csgo_say(f"Now playing: {now_playing.formatted(USER_JUKEBOX)}")
    time.sleep(1)
