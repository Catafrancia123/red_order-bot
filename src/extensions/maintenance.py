import datetime, discord, sys, os, asqlite
sys.path.append(os.path.abspath(os.path.join('..', 'schemas')))
from schemas.saveloader import load
from extensions import EXT_LIST
from discord.ext import commands
from rich import print as rprint

admin_roles = [1288801886706860082, 1388909508129980598, 1378763072357011566]
#!                  BOT TEST                        RED ORDER       
SAVE = "../save.db"               

class Maintenance(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot
        self.time_format = datetime.datetime.strftime(datetime.datetime.now(datetime.timezone.utc), "Today at %I:%M %p UTC.")

    @commands.has_any_role(*admin_roles)
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

    @commands.has_any_role(*admin_roles[1:])
    @commands.hybrid_command(with_app_command = True, brief = "Used to sync commands.")
    async def sync(self, ctx):
        user = ctx.author
        rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_blue]EVN 02[/light_blue]] Bot extension sync initiated by {user.name}')
        for ext in EXT_LIST[:-1]: #! <-- The number here represents how much modules is unloaded.
            try:   
                await self.bot.reload_extension(ext.name)
                rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]SUCCESSFUL[/light_green]] Module \"{ext.name}\" has been reloaded.')
            except Exception as e:
                rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[bright_red]ERROR[/bright_red]] Module \"{ext.name}\" failed to reload.')
                print(e)
            await self.bot.tree.sync()

        await ctx.reply("All commands have been synced.")

async def setup(bot):
    await bot.add_cog(Maintenance(bot=bot))