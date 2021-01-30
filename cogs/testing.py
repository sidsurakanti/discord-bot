import discord
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound, ExtensionNotLoaded

from datetime import datetime as dt
import os


class Testing(commands.Cog, name="Testing"):
	def __init__(self, bot):
		self.bot = bot


	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True


	@commands.command()
	@commands.has_permissions(administrator=True)
	async def unload(self, ctx, name: str):
		"""
		Unloads the specified extension.

		Usage: /unload <name>
		"""

		# unloading extension
		try:
			self.bot.unload_extension(f"cogs.{name}")
			embed = discord.Embed(title=f"{self.bot.tick} Unloaded cog: `{name.title()}`.",
								  timestamp=dt.utcnow(),
								  color=0x60DB71)
			await ctx.send(embed=embed)

		# error
		except Exception as error:
			print(error.__class__.__name__, error)
			embed = discord.Embed(title=f"{self.bot.wrong} Error while unloading cog: `{error.__class__.__name__}`.",
								  timestamp=dt.utcnow(),
								  color=0xE85936)
			await ctx.send(embed=embed)


	@commands.command()
	@commands.has_permissions(administrator=True)
	async def load(self, ctx, name: str):
		"""
		Loads the specified extension.

		Usage: /load <name>
		"""

		# loading extension 
		try: 
			self.bot.load_extension(f"cogs.{name}")
			embed = discord.Embed(title=f"{self.bot.tick} Loaded cog: `{name.title()}`.",
								  timestamp=dt.utcnow(),
								  color=0x60DB71)
			await ctx.send(embed=embed)
	
		# if error
		except Exception as error:
			print(error.__class__.__name__, error)
			embed = discord.Embed(title=f"{self.bot.wrong} Error while loading cog: `{error.__class__.__name__}`.",
								  timestamp=dt.utcnow(),
								  color=0xE85936)
			await ctx.send(embed=embed)


	@commands.group(invoke_without_command=True)
	@commands.has_permissions(administrator=True)
	async def reload(self, ctx, name: str):
		"""
		Reloads the specified cog.
		
		Usage: /reload <name>
		"""

		# reloading extension
		try:
			self.bot.reload_extension(f"cogs.{name}")

		# if extension isn't found
		except ExtensionNotFound:
			embed = discord.Embed(title=f"{self.bot.wrong} Extension not found: `{name.title()}`.",
								  timestamp=dt.utcnow(),
								  color=0xE85936)
			return await ctx.send(embed=embed)

		# if extension isn't loaded
		except ExtensionNotLoaded:
			try:
				self.bot.load_extension(f"cogs.{name}")
			except AttributeError:
				embed = discord.Embed(title=f"{self.bot.wrong} Extension not found: `{name.title()}`.",
								      timestamp=dt.utcnow(),
								      color=0xE85936)
				return await ctx.send(embed=embed)
		
		# creating and sending embed
		embed = discord.Embed(title=f"{self.bot.tick} Reloaded cog: `{name.title()}`.",
							  timestamp=dt.utcnow(),
							  color=0x60DB71)
		await ctx.send(embed=embed)


	@reload.command()
	@commands.has_permissions(administrator=True)
	async def all(self, ctx):
		"""
		Reloads all cogs.
		
		Usage: /reload all
		"""

		# looping thru the cogs folder and reloading all extensions
		try:
			for file in os.listdir('./cogs'):
					if file.endswith('.py'):
						try:
							self.bot.reload_extension(f"cogs.{file[:-3]}")
						except ExtensionNotLoaded:
							self.bot.load_extension(f"cogs.{file[:-3]}")

			# if all cogs were reloaded without error
			else: 
				embed = discord.Embed(title=f"{self.bot.tick} Reloaded all cogs.",
									  timestamp=dt.utcnow(),
									  color=0x60DB71)
				await ctx.send(embed=embed)
			
		# error
		except Exception as error:
			print((error_cls:=error.__class__.__name__), error)
			embed = discord.Embed(title=f"{self.bot.wrong} Error while reloading cogs: `{error_cls}`",
								  timestamp=dt.utcnow(),
								  color=0xE85936)
			await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Testing(bot=bot))