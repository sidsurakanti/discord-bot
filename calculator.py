import discord
from discord.ext import commands

from utils.calculator.main import calc


class Calculator(commands.Cog, name="Calculator"):
	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True


	@commands.command(aliases=["calc", "calculator"])
	async def calculate(self, ctx, *, expr: str):
		"""
		Calculates simple expressions (+, -, *, /).
		
		Usage: /calculate <expression> 
		Example: /calc 8 * 8 / 2
		"""
		result = calc(expr.replace(',', ''))
		embed = discord.Embed(description=f"{result}")
		await ctx.send(embed=embed)


async def setup(bot):
	await bot.add_cog(Calculator(bot=bot))