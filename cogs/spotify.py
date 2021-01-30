import discord
from discord.ext import commands

from datetime import datetime 

from utils.spotify.main import get_track
from utils.lyrics.main import get_lyrics


class Spotify(commands.Cog, name="Spotify"):
	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True
    

	@commands.command()
	async def listening(self, ctx, user: discord.Member = None):
		"""
		Shows info about the track that the specified user is currently listening to.
		User is default to the user that invoked the command.

		Usage: /listening [user]
		"""

		# sets user to ctx.author if user isn't specified
		user = user or ctx.author  

		for activity in user.activities:
			if isinstance(activity, discord.Spotify):
				# formatting the duration of the track
				duration = ":".join(str(activity.duration).split(".")[0].split(":")[1:])

				# creating and sending embed
				embed = discord.Embed(title=activity.title, 
									  url=get_track(activity.track_id),
									  color=0x60DB71,
							  		  timestamp=datetime.utcnow())

				embed.set_image(url=activity.album_cover_url) 
				embed.add_field(name="Artist", value=", ".join(activity.artists), inline=0)
				embed.add_field(name="Album", value=activity.album, inline=0)
				embed.add_field(name="Duration", value=duration, inline=0)
				
				return await ctx.send(embed=embed)
		
		# if the user isn't listening to anything
		else: 
			# creating and sending embed
			embed = discord.Embed(title=f"{self.bot.wrong} You're not listening to anything right now.",
								  color=0xE85936)
			await ctx.send(embed=embed)


	@commands.group(invoke_without_command=True)
	async def lyrics(self, ctx, name: str, *, artist: str = None):
		"""
		Gives you the lyrics for the specified song.

		Usage: /lyrics <name> <artist>
		"""

		# if aritist isn't provided
		if artist is None:  
			embed = discord.Embed(title=f"{self.bot.wrong} Please provide an artist.",
								  color=0xE85936)
			return await ctx.send(embed=embed)

		# creating and sending embed
		lyrics = get_lyrics(name, artist)
		embed = discord.Embed(description=f"""```{lyrics}```""",
							  color=0x60DB71,
							  timestamp=datetime.utcnow())
		embed.set_footer(text="Powered by https://musixmatch.com")
		await ctx.send(embed=embed)
	

	@lyrics.command()
	async def current(self, ctx, user: discord.Member = None):
		"""
		Gives you the lyrics for the track the specified user is currently listening to.
		User is default to the user that invoked the command.

		Usage: /lyrics current [user]
		"""

		# sets user to ctx.author
		user = user or ctx.author

		for activity in user.activities:
			if isinstance(activity, discord.Spotify):
				# getting data
				name = activity.title
				artist = activity.artist
				lyrics = get_lyrics(name, artist)

				# creating and sending embed
				embed = discord.Embed(description=f"""```{lyrics}```""",
							  		  timestamp=datetime.utcnow(),
									  color=0x60DB71)
				embed.set_footer(text="Powered by https://musixmatch.com")
				embed.set_author(name=f"{name} by {artist}")

				return await ctx.send(embed=embed)	

		# if the user isn't listening to anything
		else: 
			# creating and sending embed
			title = None 
			if user != ctx.author:
				title = f"{self.bot.wrong} `{user}` is not listening to spotify right now."
			else: 
				title = f"{self.bot.wrong} You're not listening to anything on spotify right now."
			embed = discord.Embed(title=title, color=0xE85936)
			await ctx.send(embed=embed)



def setup(bot):
	bot.add_cog(Spotify(bot=bot))
