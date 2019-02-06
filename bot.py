from discord.ext import commands
import discord, importlib

bot = commands.AutoShardedBot(command_prefix=['pet!', 'pet '], description='Adopt your own animal')

@commands.is_owner()
@bot.command(aliases=['r'])
async def reload(ctx, cog):
    try:
        importlib.reload(importlib.import_module(cog))
        bot.unload_extension(cog)
        bot.load_extension(cog)
        retv = f'{ctx.author.mention}, ``{cog}`` reloaded'
    except Exception as e:
        retv = f'{ctx.author.mention}, Error occured ({cog}): {e}'
    await ctx.send(retv)

cogs = ['cogs.pets', 'cogs.error', 'cogs.data', 'jishaku']
for x in cogs:
    try:
        bot.load_extension(x)
    except Exception as e:
        print(f'Error ocurred while cog {x} loaded\n{e}')

bot.run('token')
