import discord
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound, ExtensionNotLoaded


class Moderation(commands.Cog, name="Moderation"):
	def __init__(self, bot):
		self.bot = bot


	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True


	@commands.has_permissions(manage_channels=True)
	@commands.command(aliases=["slowdown", "cooldown"])
	async def slowmode(self, ctx, delay: int = 5):
		"""
		Sets the slowmode of the channel to the specified amount.
		Default to 5 seconds.
		
		Usage: /slowmode [delay]
		"""
		# creating embed
		if delay == 0:
			description = f"Turned off slowmode."
		else:
			description = f"Set slowmode to {delay} seconds." 
		embed = discord.Embed(description=description,
							  timestamp=ctx.message.created_at,
							  color=0x60DB71)

		# setting slowmode and sending embed
		await ctx.channel.edit(slowmode_delay=delay)
		await ctx.send(embed=embed) 
	

	@commands.has_permissions(manage_messages=True)
	@commands.command(aliases=["purge", "delete"])
	async def clear(self, ctx, limit: int = 5, user: discord.Member = None):
		"""
		Clears the specified amount of messages in the channel the command was invoked in.
		Default to 5 messages.
		Can clear up to 1000 messages. 

		Usage: /clear [limit]
		"""
		if limit > 1000:
			limit = 1000

		# deletes messages
		await ctx.message.delete()
		if user:
			check = lambda m:m.author == user
			deleted = await ctx.channel.purge(limit=limit, check=check)
		else:
			deleted = await ctx.channel.purge(limit=limit)
		
		# creating and sending embed
		embed = discord.Embed(title=f"Deleted {len(deleted)} messages.",
							  timestamp=ctx.message.created_at,
							  color=0x60DB71)
		await ctx.send(embed=embed, delete_after=10.0)


	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, user: discord.Member, *, reason=None):
		"""
		Kicks the specified user from the server. 

		Usage: /kick <user>
		"""
		embed = discord.Embed(title=f"Kicked `{user}`.",
							  description=f"**Reason** ```{reason}```",
							  timestamp=ctx.message.created_at,
							  color=0x60DB71)

		# kicking the specified user and sending embed
		await user.kick(reason=reason)
		await ctx.send(embed=embed)
	

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user: discord.Member, *, reason: str = None):
		"""
		Bans the specified user from the server.

		Usage: /ban <user>
		"""
		embed = discord.Embed(title=f"Banned `{user}`.",
							  description=f"**Reason** ```{reason}```",
							  timestamp=ctx.message.created_at,
							  color=0x60DB71)

		# banning the specified user and sending embed
		await user.ban(reason=reason)
		await ctx.send(embed=embed)
	
	
	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, user, *, reason: str = None):
		"""
		Unbans the specified user.

		Usage: /unban <user>
		"""
		banned_users = await ctx.guild.bans()
		user_name, user_discrim = user.split("#")

		# creating embed
		embed = discord.Embed(title=f"Unbanned `{user_name}#{user_discrim}`.",
							  description=f"**Reason** ```{reason}```",
							  timestamp=ctx.message.created_at,
							  color=0x60DB71)
		
		for ban in banned_users:
			user = ban.user
			if (user_name, user_discrim) == (user.name, user.discriminator):
				# unbanning the specified user and sending embed
				await ctx.guild.unban(user, reason=reason)
				await ctx.send(embed=embed)

	
async def setup(bot):
	await bot.add_cog(Moderation(bot=bot))
