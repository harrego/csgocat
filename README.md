# csgocat

Keep your CSGO team informed what's playing 

## Contributions

Thanks to [chxrlt](https://github.com/chxrlt) for writing all of the `mpris` and `xdotool` code!

## Usage

1) Install Linux, I recommend Ubuntu
2) Install `xdotool`, `sudo apt install xdotool` on Ubuntu, `sudo pacman -S xdotool` on Arch
3) Change `USER_JUKEBOX` in `main.py` to either `Jukebox.Rhytmbox` or `Jukebox.Spotify`
4) Enable the console in CSGO and get into a game
5) Run `main.py` and quickly tab back into your game, it will give you a 5 second head start
6) When a song is about to change, stand still and let it type into your game

## How it works

It uses `mpris` to determine the current song playing in either Rhythmbox or Spotify, a hash of the title and the artist is stored in `/tmp/songhash` and every second the current song is polled and compared against the cached hash. If the song has changed then `xdotool` will open the CSGO console and type `say Now playing: TITLE by ARTIST`. Before a song changes make sure you are standing still or you may type bad input into the console!

## Disclaimer

CSGO is a multiplayer video game with an anti-cheat. Like all applications that interact with the game it may lead to a "cheat detection" and get you banned. This IS NOT a cheat but it is always unknown what will trigger anti-cheat. Run this tool AT YOUR OWN RISK and I am not responsible for any action as a result of using this tool.