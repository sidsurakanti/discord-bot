from datetime import datetime
import discord
from discord.ext import commands

from utils.covid.main import country_new, country_total, world_new, world_total


class Coronavirus(commands.Cog, name="Coronavirus"):
	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True


	@commands.group(invoke_without_command=True)
	async def cases(self, ctx, *, country: str):
		"""
		Coronvirus stats for the specified country.

		Usage: /country <country>
		"""

		
		# data
		try:
			data = country_total(country.replace(" ", "-").lower())
			new_data = country_new(country.replace(" ", "-").lower())
		except KeyError:
			embed = discord.Embed(title=f"{self.bot.wrong} Country not found: `{country}`", 
								  timestamp=datetime.utcnow())
			return await ctx.send(embed=embed)
		except IndexError:
			embed = discord.Embed(title=f"{self.bot.wrong} Country not found: `{country}`", 
								  timestamp=datetime.utcnow())
			return await ctx.send(embed=embed)
		
		# creating and sending embed
		embed = discord.Embed(color=0xC36865, timestamp=datetime.utcnow())
		embed.set_author(name=f"{data[0]}")
		embed.add_field(name="Cases",  value=f"{data[1]:,}")
		embed.add_field(name="Deaths", value=f"{data[2]:,}", inline=0)
		embed.add_field(name="New Cases", value=f"{new_data[0]:,}", inline=0)
		embed.add_field(name="New Deaths", value=f"{new_data[1]:,}")
		embed.set_footer(text="Powered by https://covid19api.com")

		await ctx.send(embed=embed)
	
	
	@cases.command()
	async def world(self, ctx):
		"""
		Coronavirus statistics for the world.

		Usage: /cases world
		"""

		# getting data 
		data = world_total()
		new_data = world_new()

		# creating and sending embed
		embed = discord.Embed(timestamp=datetime.utcnow(), color=0xC36865)
		embed.set_author(name="World")
		embed.add_field(name="Cases", value=f"{data[0]:,}")
		embed.add_field(name="Deaths", value=f"{data[1]:,}", inline=0)
		embed.add_field(name="New Cases", value=f"{new_data[0]:,}", inline=0)
		embed.add_field(name="New Deaths", value=f"{new_data[1]:,}")
		embed.set_footer(text="Powered by https://covid19api.com")
		
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Coronavirus(bot=bot))
