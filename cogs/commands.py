import discord
from discord.ext import commands

import random


class Commands(commands.Cog, name="Commands"):
	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True

	@commands.command()
	async def ping(self, ctx):
		"""
		Shows the latency of the bot.
		
		Usage: /ping
		"""
		latency = round(self.bot.latency * 1000)  
		embed = discord.Embed(
							  description=f"{latency}ms", 
							  color=self.bot.user.color,
							  timestamp=ctx.message.created_at
							  )
		await ctx.send(embed=embed)
		
	@commands.command()
	async def say(self, ctx, channel: discord.TextChannel, *, text: str):
		"""
		Says something in the specified channel.

		Usage: /say <channel> <text>
		"""
		await channel.send(text, allowed_mentions=discord.AllowedMentions().none())
		
	@commands.command()
	async def choose(self, ctx, *args):
		"""
		Chooses a random choice from the specified choices. 
		Choices are default to yes/no.

		Usage: /choose [choices]
		"""
		choices = args or ["Yes", "No"]
		answer = random.choice(choices)
		embed = discord.Embed(description=answer,
							  timestamp=ctx.message.created_at)
		await ctx.send(embed=embed)

	@commands.group(aliases=["av", "pfp"], invoke_without_command=True)
	async def avatar(self, ctx, *, user: discord.Member = None):
		"""
		Shows the avatar of the specified user.
		User is default to the user that invoked the command. 

		Usage: /avatar [user]
		"""
		user = user or ctx.author
		
		# creating and sending embed
		embed = discord.Embed(color=user.color, timestamp=ctx.message.created_at)
		embed.set_image(url=user.display_avatar.url)
		embed.set_author(name=user, icon_url=user.display_avatar.url)
		await ctx.send(embed=embed)

	@avatar.command()
	async def server(self, ctx):
		"""
		Shows the avatar of the server.

		Usage: /avatar server
		"""
		user = ctx.author

		# creating and sending embed
		embed = discord.Embed(color=user.color, timestamp=ctx.message.created_at)
		embed.set_image(url=ctx.guild.icon)
		embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
		await ctx.send(embed=embed)

	@commands.command(aliases=["userinfo", "whois"])
	async def info(self, ctx, *, user: discord.Member = None):
		"""
		Shows info about the specified user.
		User is default to the user that invoked the command. 

		Usage: /info [user]
		"""
		# gets user info
		user = user or ctx.author 
		roles = [role.mention for role in user.roles if role.name != "@everyone"]
		join_date = user.joined_at.strftime("%a, %b %d, %Y")
		registered_date = user.created_at.strftime("%a, %b %d, %Y")

		# creating and sending embed
		embed = discord.Embed(color=user.color,
							  timestamp=ctx.message.created_at)
		embed.set_author(
						name=f"{user}", 
						icon_url=user.display_avatar.url
						)		
		embed.set_thumbnail(url=user.display_avatar.url)
		embed.add_field(name="Joined", value=f"{join_date}")
		embed.add_field(name="Registered", value=f"{registered_date}")
		embed.set_footer(text=f"ID: {user.id}")
		
		if roles:
			embed.add_field(name="Roles", value=" ".join(roles), inline=False)
		
		await ctx.send(embed=embed)
	
	@commands.command()
	async def serverinfo(self, ctx):
		"""
		Shows info about the server.

		Usage: /serverinfo
		"""
		# get info
		guild = ctx.guild
		roles = [role.mention for role in guild.roles if role.name != "@everyone"]
		text_channels = len(guild.text_channels)
		voice_channels = len(guild.voice_channels)
		owner = guild.owner
		member_count = guild.member_count 
		created_at = guild.created_at.strftime("%a, %b %d, %Y")

		# create embed
		embed = discord.Embed(title=guild.name, 
							  color=ctx.author.color,
							  timestamp=ctx.message.created_at)
		embed.set_thumbnail(url=guild.icon)
		embed.set_footer(text=f"ID: {guild.id}")

		embed.add_field(name="Owner", value=owner.mention)
		embed.add_field(name="Created", value=f"{created_at}")
		embed.add_field(name="\u200b", value="\u200b")  # empty field
		embed.add_field(name="Text Channels", value=f"{text_channels}")
		embed.add_field(name="Voice Channels", value=f"{voice_channels}")
		embed.add_field(name="Member Count", value=f"{member_count}")
		if roles:
			embed.add_field(name="Roles", value=" ".join(roles), inline=0)
		
		await ctx.send(embed=embed)

	@commands.command()
	async def emojis(self, ctx):
		"""
		Shows the list of emojis in the server

		Usage: /emojis 
		"""
		emojis = ctx.guild.emojis
		embed = discord.Embed(title="Emojis", color=ctx.author.color, timestamp=ctx.message.created_at)
		embed.description = f"""
								Count: `{len(emojis)}`
								Animated: `{len(list(filter(lambda e:e.animated, emojis)))}`
								Regular: `{len(list(filter(lambda e:not e.animated, emojis)))}`

								{" ".join(map(str, emojis))}
							"""
		await ctx.send(embed=embed)


async def setup(bot):
	await bot.add_cog(Commands(bot=bot))