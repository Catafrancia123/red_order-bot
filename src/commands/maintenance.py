import datetime, discord
from pathlib import Path
from discord.ext import commands
from rich import print as rprint

class Maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time_format = datetime.datetime.strftime(datetime.datetime.now(datetime.timezone.utc), "Today at %I:%M %p UTC.")

    @commands.hybrid_command(with_app_command = True, brief = "Shuts down the bot manually.")
    async def shutdown(self, ctx):
        user = ctx.author
        await ctx.reply(f"Bot shutdown initated by {user.name}.")
        rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_blue]EVN 01[/light_blue]] Bot shutdown initiated by {user.name}')
        await self.bot.close()

    @commands.hybrid_command(with_app_command = True, brief = "Shows the average ping of the bot.")
    async def ping(self, ctx):
        embedvar = discord.Embed(
            title="Pong!",
            description=f"Average bot ping: {round(self.bot.latency*1000)}ms",
            color=discord.Color.blue(),
        )
        embedvar.set_footer(text=self.time_format)

        await ctx.reply(embed=embedvar)

    @commands.hybrid_command(with_app_command = True, brief = "Used to sync commands.")
    async def sync(self, ctx):
        await self.bot.tree.sync()
        func_commands = Path("./")
        for command in [str(x) for x in func_commands.iterdir() if x.is_file()]:
            try:
                await self.reload_extension(command.replace("\\", ".")[:-3])
                rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]SUCCESSFUL[/light_green]] Module \"{command[:-3]}\" has been reloaded.')
            except Exception as e:
                rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[bright_red]ERROR[/bright_red]] Module \"{command[:-3]}\" failed to reload.')

        await ctx.reply("All commands have been synced.")

async def setup(bot):
    await bot.add_cog(Maintenance(bot=bot))