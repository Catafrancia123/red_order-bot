import datetime
from discord.ext import commands
from rich import print as rprint

class Maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(with_app_command = True, brief = "Shuts down the bot manually.")
    async def shutdown(self, ctx):
        user = ctx.author
        await ctx.reply(f"Bot shutdown initated by {user.name}.")
        rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_blue]EVN 01[/light_blue]] Bot shutdown initiated by {user.name}')
        await self.bot.close()

    @commands.hybrid_command(with_app_command = True, brief = "Shows the average ping of the bot.")
    async def ping(self, ctx):
        await ctx.reply(f"Average bot ping: {round(self.bot.latency*1000)}ms")

    @commands.hybrid_command(with_app_command = True, brief = "Used to sync commands.")
    async def sync(self, ctx):
        await self.bot.tree.sync()
        await ctx.reply("All commands have been synced.")

async def setup(bot):
    await bot.add_cog(Maintenance(bot=bot))