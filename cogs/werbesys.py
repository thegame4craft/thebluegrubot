import logging

import discord
from discord.ext import commands


class WerbeSystem(commands.Cog):
	def __init__(self, client):
		self.client = client  # Globale Variable erstellen
	
	@commands.Cog.listener()
	async def on_message(self, message):  # Self als ersten Parameter, sonst gibt es Fehler
		guild = self.client.get_guild(message.guild.id)  # Nur ein beispiel, da du immer self.client benutzen musst
	
	@commands.command()
	async def partner(self, ctx):
		if self.client.is_ready():
			embed = discord.Embed(title='Parterschaft?',
								  description='Wende dich an den support oder erstelle ein ticket.',
								  color=discord.Colour.gold())
			await ctx.send(embed=embed)
	
	@commands.command(aliases=['winfo'])
	async def werbeinfo(self, ctx):
		if self.client.is_ready():
			embed = discord.Embed(title='Werbe Information', description='', color=discord.Colour.dark_purple())
			embed.add_field(name='Werbung level 1:', value='...')  # TODO
			await ctx.send(embed=embed)


def setup(client):
	client.add_cog(WerbeSystem(client))
	print("WerbeSystem loaded on Version V1.0")
