A simple, multifunctional discord bot made with `discord.py`.

## Commands

#### General 
- `calculate`: Calculates simple mathematical expressions (+, -, *, /).
- `avatar`: Displays the avatar of the specified user.
- `choose`: Chooses randomly from the specified options. 
- `emojis`: Shows the list of emojis available on the server.
- `info`: Provides information about a specific user.
- `ping`: Shows the bot's latency.
- `say`: Allows the bot to send a specified message to a certain channel.
- `serverinfo`: Gives information about the server.

#### Music
- `listening`: Shows information about the track that the specified user is currently listening to on Spotify.
- `lyrics`: Provides the lyrics for the specified song.

#### Coronavirus
- `cases`: Shows coronavirus statistics for the specified country.

#### Moderation
- `ban`: Bans the specified user from the server.
- `clear`: Clears the specified amount of messages from the channel.
- `kick`: Kicks the specified user from the server. 
- `slowmode`: Sets the slowmode of the channel to the specified time.
- `unban`: Unbans the specified user.

#### Source
- `source`: Shows the source code for the specified command.

## Usage

To use this bot on your own server, you'll need to set up your environment:

1. Clone this repository.
```shell 
git clone https://github.com/sidsurakanti/discord-bot-2.git
```
2. Install the dependencies.
```shell
pip install -r requirements.txt
```
3. Create a new `config.py` file that looks like 
```py
# config.example.py
TOKEN = "INSERT DISCORD BOT TOKEN HERE"
LYRICS_KEY = "INSERT MUSIXMATCH TOKEN HERE"
SPOTIFY_CLIENT = "INSERT SPOTIFY CLIENT ID HERE"
SPOTIFY_SECRET = "INSERT SPOTIFY CLIENT SECRET HERE"
```
4. Run the bot with `python bot.py`.
5. Invite the bot to your own server.
