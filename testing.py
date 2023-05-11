import discord
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound, ExtensionNotLoaded

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
		try:
			# unloading extension
			await self.bot.unload_extension(f"cogs.{name}")
			embed = discord.Embed(description=f"Unloaded cog: `{name.title()}`",
								  timestamp=ctx.message.created_at,
								  color=0x60DB71)
			await ctx.send(embed=embed)
		except Exception as error:
			print(error.__class__.__name__, error)
			embed = discord.Embed(description=f"Error while unloading cog: `{error.__class__.__name__}`",
								  timestamp=ctx.message.created_at,
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
			await self.bot.load_extension(f"cogs.{name}")
			embed = discord.Embed(description=f"Loaded cog: `{name.title()}`",
								  timestamp=ctx.message.created_at,
								  color=0x60DB71)
			await ctx.send(embed=embed)
	
		# if error
		except Exception as error:
			print(error.__class__.__name__, error)
			embed = discord.Embed(description=f"Error while loading cog: `{error.__class__.__name__}`.",
								  timestamp=ctx.message.created_at,
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
			await self.bot.reload_extension(f"cogs.{name}")

		# if extension isn't found
		except ExtensionNotFound:
			embed = discord.Embed(description=f"Extension not found: `{name.title()}`",
								  timestamp=ctx.message.created_at,
								  color=0xE85936)
			return await ctx.send(embed=embed)

		# if extension isn't loaded
		except ExtensionNotLoaded:
			try:
				await self.bot.load_extension(f"cogs.{name}")
			except AttributeError:
				embed = discord.Embed(description=f"Extension not found: `{name.title()}`",
								      timestamp=ctx.message.created_at,
								      color=0xE85936)
				return await ctx.send(embed=embed)
		
		# creating and sending embed
		embed = discord.Embed(description=f"Reloaded cog: `{name.title()}`",
							  timestamp=ctx.message.created_at,
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
						await self.bot.reload_extension(f"cogs.{file[:-3]}")
					except ExtensionNotLoaded:
						await self.bot.load_extension(f"cogs.{file[:-3]}")

			# if all cogs were reloaded without error
			else: 
				embed = discord.Embed(description=f"Reloaded all cogs.",
									  timestamp=ctx.message.created_at,
									  color=0x60DB71)
				await ctx.send(embed=embed)
			
		# error
		except Exception as error:
			print((error_cls:=error.__class__.__name__), error)
			embed = discord.Embed(description=f"Error while reloading cogs: `{error_cls}`",
								  timestamp=ctx.message.created_at,
								  color=0xE85936)
			await ctx.send(embed=embed)


async def setup(bot):
	await bot.add_cog(Testing(bot=bot))