import discord
from discord.ext import commands


def is_not_pinned(mess):
	return not mess.pinned


class Moderation(commands.Cog):
	def __init__(self, client):
		self.client = client  # Globale Variable erstellen
	
	@commands.command(name='ban')
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member: discord.Member, *, reason: str = None):
		await member.ban(reason=reason)
		ctx.send('Ich habe %s gebannt.' % member.display_name)
		userid = member.replace('<', '')
		userid = userid.replace('@', '')
		userid = userid.replace('!', '')
		userid = userid.replace('>', '')
	
	@ban.error
	async def ban_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send('Ich konnte diesen Member nicht finden')
		elif isinstance(error, commands.MissingPermissions):
			await ctx.send('Dir ist es nicht gestattet diesen befehl auszuführen')
	
	@commands.command(name='kick')
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member: discord.Member, *, reason=None):
		await member.kick(reason=reason)
		ctx.send('Ich habe %s vom Server entfernt.' % member.display_name)
	
	@kick.error
	async def kick_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send('Ich konnte diesen Member nicht finden')
		elif isinstance(error, commands.MissingPermissions):
			await ctx.send('Dir ist es nicht gestattet diesen befehl auszuführen')
	
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, args):
		count = int(args) + 1
		deleted = await ctx.channel.purge(limit=count, check=is_not_pinned)
		await ctx.send('{} Nachrichten gelöscht.'.format(len(deleted) - 1), delete_after=5)
	
	@clear.error
	async def clear_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send('Dir ist es nicht gestattet diesen befehl auszuführen')
	
	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def mute(self, ctx, member: discord.Member):
		guild = ctx.guild
		for role in guild.roles:
			if role.name == 'Muted':
				await member.add_roles(role)
				await ctx.send('{} wurde gemuted!'.format(member.mention))
				return
			else:
				overwrite = discord.PermissionOverwrite(send_messages=False)
				newRole = await guild.create_role(name='Muted')
				for channel in guild.text_channels:
					await channel.set_permissions(newRole, overwrite=overwrite)
					await member.add_roles(newRole)
					await ctx.send('{} wurde gemuted!'.format(member.mention))
					return
	
	@mute.error
	async def mute_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send('Ich konnte diesen Member nicht finden')
		elif isinstance(error, commands.MissingPermissions):
			await ctx.send('Dir ist es nicht gestattet diesen befehl auszuführen')
	
	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def unmute(self, ctx, member: discord.Member):
		guild = ctx.guild
		for role in guild.roles:
			if role.name == 'Muted':
				await member.remove_roles(role)
				await ctx.send('{} wurde entmuted'.format(member.mention))
				return
	
	@unmute.error
	async def unmute_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send('Ich konnte diesen Member nicht finden')
		elif isinstance(error, commands.MissingPermissions):
			await ctx.send('Dir ist es nicht gestattet diesen befehl auszuführen')


def setup(client):
	client.add_cog(Moderation(client))  # Cog hinzufügen
	print("Mod-system loaded on Version V1.0")
