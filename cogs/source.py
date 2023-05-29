import discord
from discord.ext import commands

from inspect import getsource


class Source(commands.Cog, name="Source"):
	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True

	@commands.command(aliases=["src"])
	async def source(self, ctx, name = None):
		"""
		Shows the source code for the specified command.

		Usage: /source <name>
		"""
		if name is None: 
			return
		if (command:= self.bot.get_command(name)) is None: 
			embed = discord.Embed(title=f"{self.bot.wrong} Command not found: `{name}`.",
								  timestamp=ctx.message.created_at,
							  	  color=0xE85936)
			return await ctx.send(embed=embed)
		
		def paginator(content: str, max=int):
			"""Converts lines into multiple pages."""
			pages, i = [''], 0
			for line in content.splitlines(keepends=True):
				if len(pages[i] + line) > max:
					i += 1
					pages.append('')
				pages[i] += line
			return pages

		try: 
			# get the source code for the specified command
			source = getsource(command.callback) 
		except AttributeError: 
			embed = discord.Embed(title=f"{self.bot.wrong} Command doesn't exist: {name}",
								  timestamp=ctx.message.created_at,
							  	  color=0xE85936)
			return await ctx.send(embed=embed)
		
		# paginate and send the code
		for page in paginator(source, 1920): 
			page = page.replace("`", "`\u200b")
			await ctx.send(f'```py\n{page}```')


async def setup(bot):
	await bot.add_cog(Source(bot=bot))
