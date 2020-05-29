import asyncio
import logging

import discord, random
from discord.ext import commands
from main import prefix

bot = commands.AutoShardedBot(command_prefix=prefix)


class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client  # Globale Variable erstellen

    @commands.Cog.listener()
    async def on_message(self, message):  # Self als ersten Parameter, sonst gibt es Fehler
        guild = self.client.get_guild(message.guild.id)


        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            message.author: discord.PermissionOverwrite(read_messages=True)
        }
        if message.content.startswith(prefix + 'new'):
            if self.client.is_ready():
                ticket_channel = await guild.create_text_channel(name=f'Ticket-{str(random.randint(1, 9999)).zfill(4)}',
                                                                 reason='WerbeManager Ticket Opened',
                                                                 category=guild.categories[3],
                                                                 overwrites=overwrites)
                embed = discord.Embed(title='Dein Ticket',
                                      description='Bitte halte dich an folgende regeln: \n'
                                                  '1. Nicht spammen \n'
                                                  '2. Das Team hat immer letztes Wort \n'
                                                  '3. Warten. Das Team kümmert sich schon noch um dich',
                                      color=discord.Colour.red())
                await ticket_channel.send(embed=embed)

        if message.content.startswith(prefix + 'close'):
            if self.client.is_ready():
                if message.channel.name.startswith('ticket'):
                    await message.channel.send('Das Ticket wird in 3 Sekunden gelöscht')
                    await asyncio.sleep(3)
                    await discord.TextChannel.delete(self=message.channel, reason='WerbeManager Ticket Closed')
                else:
                    await message.channel.send('Du musst in einem Ticket channel sein')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 712197273764757554 or payload.message_id == 712321899010457620:
            if payload.emoji.name == '➕':
                guild = self.client.get_guild(payload.guild_id)

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True),
                    payload.member: discord.PermissionOverwrite(read_messages=True)
                }
                ticket_channel = await guild.create_text_channel(name=f'Ticket-{str(random.randint(1, 9999)).zfill(4)}',
                                                                 reason='WerbeManager Ticket Opened',
                                                                 category=guild.categories[3],
                                                                 overwrites=overwrites)
                embed = discord.Embed(title='Dein Ticket',
                                      description='Bitte halte dich an folgende regeln: \n'
                                                  '1. Nicht spammen \n'
                                                  '2. Das Team hat immer letztes Wort \n'
                                                  '3. Warten. Das Team kümmert sich schon noch um dich',
                                      color=discord.Colour.red())
                embed.set_footer(text='Tippe !close um das Ticket zu schliessen')
                await ticket_channel.send(embed=embed)




def setup(client):
    client.add_cog(Ticket(client))
    print("Ticket system loaded on Version V1.1")
