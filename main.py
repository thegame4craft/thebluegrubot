import asyncio

import discord
from discord.ext import commands
import json, logging


with open('config.json') as file:
	config_data = json.load(file)

token = config_data['token']
prefix = config_data['prefix']

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d/%m/%Y %H:%M:%S',
					level=logging.INFO)

bot = commands.AutoShardedBot(command_prefix=prefix)

bot.remove_command('help')


def loadcog(cogname):
	if cogname.endswith('.py'):
		bot.load_extension(f'cogs.{cogname[:-3]}')


loadcog('ticket.py')
loadcog('werbesys.py')
loadcog('moderation.py')
loadcog('cmds.py')


@bot.event
async def on_message(message):
	if message.content.startswith(prefix):
		logging.info(
			f'{message.guild.name} - [{message.channel.name}] <{message.author.name}#{message.author.discriminator}>: {message.content}')
		await bot.process_commands(message)



@bot.event
async def on_ready():
	logging.info(f'╔════════════════════════════════════')
	logging.info(f'║ Logged succsessfully in as {bot.user}')
	logging.info(f'║ Active shards: {bot.shard_count} (Count)')
	logging.info(f'╚════════════════════════════════════')
	bot.loop.create_task(status_task())
	

@bot.command(name='ping')
async def ping(ctx):
	print('1')
	print('2')
	embed = discord.Embed(title='Pong', description=f'Dein Shard: {bot.shard_id}', color=discord.Color.orange())
	print('2.5')
	"""for i in len(bot.shard_count):
		i = i + 1"""
	print('3')
	
	embed.add_field(name=f'Shard 0', value=f'Ping: {bot.latencies[0][1]}', inline=True)
	await ctx.send(embed=embed)
	print('4')


async def status_task():
	while True:
		# print(bot.latency)
		await bot.change_presence(activity=discord.Game('!help'), status=discord.Status.online)
		await asyncio.sleep(5)
		# print(bot.latency)
		await bot.change_presence(activity=discord.Game('Minecraft-Java server: discord.gg/M2YeaGA'),
								  status=discord.Status.online)
		await asyncio.sleep(5)


@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandError):
		# print('CMD not found')
		# await ctx.send('Was soll ich ausführen? Ich konnte keinen befehl finden')
		return


bot.run(token)
