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
		Calculates simple arithmetic operations (+, -, *, /).
		
		Usage: /calculate <expression> 
		Example: /calc 8 * 8
		"""
		result = calc(expr.replace(',', ''))

		# removes the digits after the decimal point if they're are equal to 0
		if (num:=result.split('.'))[-1] == "0":
			result = int(num[0])

		embed = discord.Embed(title=f"`{result}`")
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Calculator(bot=bot))