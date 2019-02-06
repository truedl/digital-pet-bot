from discord.ext import commands
import discord

class Errors:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(f'{ctx.author.mention}, Only owner command!')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'{ctx.author.mention}, You can\'t use this command, Try to ``pet!adopt``')
            ctx.command.reset_cooldown(ctx)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}, {error}')
            ctx.command.reset_cooldown(ctx)
        elif isinstance(error, commands.CommandOnCooldown):
            if int(error.retry_after/3600) > 1:
                await ctx.send(f'{ctx.author.mention}, You\'re on cooldown, try again in {round(error.retry_after/3600, 2)} hours')
            elif round(error.retry_after/60, 2) < 1:
                await ctx.send(f'{ctx.author.mention}, You\'re on cooldown, try again in {round(error.retry_after, 2)} seconds')
            else:
                await ctx.send(f'{ctx.author.mention}, You\'re on cooldown, try again in {round(error.retry_after/60, 2)} minutes')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'{ctx.author.mention}, {error}')
            ctx.command.reset_cooldown(ctx)
        else:
            print(error)

def setup(bot):
    bot.add_cog(Errors(bot))
