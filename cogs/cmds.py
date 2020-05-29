import discord
from discord.ext import commands
from main import prefix

player_dict = dict()

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name='help', aliases=['h'])
    async def help(self, ctx, search=None):
        """embed = discord.Embed(title='Hilfe Seite', description=' ', color=discord.Colour.orange())
        embed.add_field(name='Fun', value='', inline=False)
        embed.add_field(name='Werbung', value=f'`{prefix}werbeinfo` - `{prefix}partner`', inline=False)
        embed.add_field(name='Moderation', value='', inline=False)
        embed.add_field(name='Ticket', value=f'`{prefix}new` - `{prefix}close`', inline=False)"""
        
        embed = discord.Embed(title='Help',
                              description='Du brauchst Hilfe bei Commands? Dann suche doch hier einfach',
                              color=discord.Colour.orange())
        embed.add_field(name='Fun:',
                        value='`ping` - `meme`',
                        inline=False)
        embed.add_field(name='Moderation:',
                        value='`clear` - `kick` - `ban` - `unban` - `warn` - `mute` - `unmute` - `warn`',
                        inline=False)
        embed.add_field(name='Ticket:',
                        value=f'`{prefix}new` - `{prefix}close`',
                        inline=False)
        embed.set_footer(text=f'Tipp: Mein Prefix ist {prefix}')
        
        if not search is None:
            if search == 'new':
                await ctx.send('Diese funktion wird nocht entwickelt')
            else:
                await ctx.send('Diese funktion wird nocht entwickelt')
        
        await ctx.send(embed=embed)
        
    @commands.command(name='play')
    async def play(self, ctx, url):
        print('1')
        print(ctx.message.author)
        channel = ctx.message.author.voice.voice_channel

        print('2')
        await self.client.join_voice_channel(channel)
        server = ctx.message.server
        voice = self.client.voice_client_in(server)
        player = await voice.create_ytdl_player(url)
        player_dict[server.id] = player
        player.start()

    @commands.command(name='stop')
    async def stop(self, ctx):
        server = ctx.message.server
        player = player_dict[server.id]
        player.stop()
        del player_dict[server.id]
        
        
def setup(client):
    client.add_cog(Commands(client))
    print("Commands loaded")
