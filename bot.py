import discord
from discord.activity import ActivityType as at
from discord.ext import commands, tasks

import asyncio
import os
from itertools import cycle

from utils.config import TOKEN


print('Connecting...')


class Bot(commands.Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(command_prefix=kwargs.pop('command_prefix', '/'),
						 case_insensitive=True,
						 intents=discord.Intents.all(),
						 description="""A simple discord bot.""",
						 *args, **kwargs)


	async def on_ready(self):
		"""
		After the bot is ready.
		"""
		await self.wait_until_ready()
		self.wrong = "<a:wrong:804092357796036688>"
		self.tick = "<a:tick:804092358328582144>"

		# gets the number of guilds the bot is in
		guilds = len(await self.fetch_guilds(limit=None).flatten())

		# statuses
		statuses = cycle([discord.Activity(name=f'use prefix "{self.command_prefix}"', type=at.playing), 
						  discord.Activity(name=f"{guilds} servers", type=at.watching),
						  discord.Activity(name=f"{self.command_prefix}help", type=at.listening)])

		# a loop that changes the bot's status
		@tasks.loop(minutes=1)
		async def status():
			await self.change_presence(activity=next(statuses))

		status.start() 

		# loads extensions
		self.load_extension("jishaku")  
		for file in os.listdir('cogs'):
			if file.endswith('.py'):
				self.load_extension(f"cogs.{file[:-3]}")

		print(f"{self.user.name} is ready!") 


	async def on_message(self, message):
		"""When a user sends a message."""
		if message.author.bot:
			return

		# gets the invite link for the bot
		invite_link = discord.utils.oauth_url(self.user.id, permissions=discord.Permissions(administrator=True))

		# embed
		embed = discord.Embed(color=self.user.color)
		embed.description = f"""
								{self.description}
								
								Prefix(s): {" ".join([f"`{prefix}`" for prefix in self.command_prefix])}
								Owner: [`izzy#8332`](https://discord.com/users/521872289231273994)
							 """
		embed.add_field(name="\u200b", value=f"[**`Invite Link`**]({invite_link})", inline=0)
		embed.set_author(name=self.user, icon_url=self.user.avatar_url)

		# sends the embed if the message only contains the mention of the bot
		if message.content == f"<@!{self.user.id}>":
			await message.channel.send(embed=embed)

		await self.process_commands(message)


	async def process_commands(self, message):
		if message.author.bot:
			return

		ctx = await self.get_context(message=message)
		await self.invoke(ctx)


	@classmethod 
	async def setup(cls):
		"""Starts the bot."""
		bot = cls()
		try:
			await bot.start(TOKEN)
		except KeyboardInterrupt:
			await bot.close()


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(Bot.setup())
