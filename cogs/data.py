from discord.ext import commands
from psutil import Process as prc
from os import getpid
import discord

class Data:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def website(self, ctx):
        await ctx.send(embed=discord.Embed(description='https://truedl.github.io/digital-pet-website/').set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url))

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(embed=discord.Embed(description='https://discordapp.com/oauth2/authorize?client_id=505422489695027240&scope=bot&permissions=0').set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url))

    @commands.is_owner()
    @commands.command()
    async def m(self, ctx):
        await ctx.send(f'{ctx.author.mention}, {round(prc(getpid()).memory_info().rss/1024/1024, 2)} MB')

    @commands.command(aliases=['server'])
    async def support(self, ctx):
        await ctx.send(embed=discord.Embed(description='https://discord.gg/3eNQf2P').set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url))

    @commands.command(aliases=['upvote'])
    async def vote(self, ctx):
        await ctx.send(embed=discord.Embed(description='https://discordbots.org/bot/505422489695027240/vote').set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url))

def setup(bot):
    bot.add_cog(Data(bot))
