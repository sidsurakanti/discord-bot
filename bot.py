import discord
from discord.activity import ActivityType as at
from discord.ext import commands, tasks

import asyncio
import os
from itertools import cycle
import logging

from utils.config import TOKEN


logging.basicConfig(level=logging.INFO)
print('Connecting...')

class Bot(commands.Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(command_prefix=kwargs.pop('command_prefix', '.'),
						 case_insensitive=True,
						 intents=discord.Intents.all(),
						 *args, **kwargs)

	async def on_ready(self):
		await self.wait_until_ready()

		# gets the number of servers the bot is in
		guilds = len([guild async for guild in self.fetch_guilds(limit=150)])

		statuses = cycle([discord.Activity(name=f'use prefix "{self.command_prefix}"', type=at.playing), 
						  discord.Activity(name=f"{guilds} servers", type=at.watching),
						  discord.Activity(name=f"{self.command_prefix}help", type=at.listening)])

		# change bot status
		@tasks.loop(minutes=1)
		async def status():
			await self.change_presence(activity=next(statuses))

		status.start() 

		# loads extensions
		await self.load_extension("jishaku")  
		for cog in os.listdir('cogs'):
			if cog.endswith('.py'):
				await self.load_extension(f"cogs.{cog[:-3]}")
				print(f'Loaded cog: {cog[:-3]}')

		print(f"{self.user.name} is ready!") 

	async def on_message(self, message):
		"""When a user sends a message."""
		if message.author.bot:
			return

		# create bot invite link
		invite_link = discord.utils.oauth_url(self.user.id, permissions=discord.Permissions(administrator=True))

		# create embed
		embed = discord.Embed(color=self.user.color)
		embed.description = f"Prefix(s): {', '.join([f'`{prefix}`' for prefix in self.command_prefix])}"
		embed.add_field(name="\u200b", value=f"[Invite Link]({invite_link})", inline=0)
		embed.set_author(name=self.user, icon_url=self.user.display_avatar.url)

		# send embed if bot is mentioned
		if message.content == self.user.mention:
			await message.channel.send(embed=embed)

		await self.process_commands(message)

	async def process_commands(self, message):
		if message.author.bot:
			return

		ctx = await self.get_context(message)
		await self.invoke(ctx)

	@classmethod 
	async def setup(cls):
		bot = cls()
		try:
			await bot.start(TOKEN)
		except KeyboardInterrupt:
			await bot.close()


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(Bot.setup())
