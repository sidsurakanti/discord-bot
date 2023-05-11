import discord
from discord.ext import commands

class Errors(commands.Cog, name="Errors"):
	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		print(error.__class__.__name__, error)
		embed = discord.Embed(description=f"Error while invoking command: {error.__class__.__name__}",
							  timestamp=ctx.message.created_at,
							  color=0xE85936)
		return await ctx.send(embed=embed)


async def setup(bot):
	await bot.add_cog(Errors(bot=bot))
