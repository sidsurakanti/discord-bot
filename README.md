A simple, multifunctional discord bot made with [discord.py](https://discordpy.readthedocs.io/en/stable/).

## Commands

#### General 
- `choose`: Randomly chooses from the specified options
- `emojis`: Shows the list of emojis available in the server
- `ping`: Returns the bot's latency
- `say`: Allows the bot to send a specified message to a certain channel
- `serverinfo`: Displays information about the server
- `info`: Displays information about a specified user
- `avatar`: Displays the avatar of the specified user

#### Calculator
- `calculate`: Calculates simple arithmetic expressions (+, -, *, /)

#### Music
- `listening`: Shows information about the track that the specified user is currently listening to on Spotify
- `lyrics`: Provides the lyrics for the specified song

#### COVID-19
- `cases` [(API discontinued)](https://covid19api.com/): Shows coronavirus statistics for the specified country

#### Moderation
- `kick`: Kicks specified user from the server
- `ban`: Bans specified user from the server
- `unban`: Unbans specified user
- `clear`: Clears specified amount of messages from the channel
- `slowmode`: Sets slowmode of the channel to the specified time

#### Source
- `source`: Shows the source code for the specified command

## Usage

To use this bot in your own server, you'll need to set up your environment:

1. Clone this repository
```shell 
git clone https://github.com/sidsurakanti/discord-bot-2.git
```
2. Install required dependencies
```shell
pip install -r requirements.txt
```
3. Create a new `config.py` file that looks like 
```py
# config.example.py
TOKEN="INSERT DISCORD BOT TOKEN HERE"
LYRICS_KEY="INSERT MUSIXMATCH TOKEN HERE"
SPOTIFY_CLIENT="INSERT SPOTIFY CLIENT ID HERE"
SPOTIFY_SECRET="INSERT SPOTIFY CLIENT SECRET HERE"
```
4. Run the bot using `python bot.py` in your terminal
5. Invite the bot to your own server
6. Run commands!
