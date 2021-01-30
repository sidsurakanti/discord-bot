import discord
from discord.ext import commands

from datetime import datetime as dt


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
		"""If a command fails to execute properly."""
		print(error.__class__.__name__, error)
		embed = discord.Embed(title=f"{self.bot.wrong} Error while invoking command: `{error.__class__.__name__}`",
							  timestamp=dt.utcnow(),
							  color=0xE85936)
		return await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Errors(bot=bot))
