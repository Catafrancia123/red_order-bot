""" Version 1.0:
    - Creation of the bot."""

import discord, datetime, os, sys, asyncio, playsound3
from saveloader import load_json
from discord.ext import commands
from rich import print as rprint

def clear():
    if sys.platform.startswith(('win32')):
        os.system('cls')
    elif sys.platform.startswith(('linux', 'cygwin', 'darwin', 'freebsd')):
        os.system('clear')

BOTVER = "1.0"
logo = discord.File("images/logo.png", filename="logo.png")

class Bot(commands.Bot):
    def __init__(self):
        global intents

        intents = discord.Intents.default()
        intents.members = True #! can see members
        intents.message_content = True #! can see message content
        intents.reactions = True #! can see reactions

        super().__init__(command_prefix = "$", intents = intents)
    
    def make_error_embed(self, user : str, error_code : int = 99, error_msg : str = None) -> discord.Embed:
        time_format = datetime.datetime.strftime(datetime.datetime.now(datetime.timezone.utc), "Today at %I:%M %p UTC.")
        #* add more later!!
        errors = {1:"Command not found/doesn't exist.", 
                2:"An input is missing, please try again.",
                3:"An input is invalid/unprocessable.",
                4:"You don't have permission to run this command.",
                5:"Server Error. Either from API or Discord.",
                6:"Bot doesn't have permission to do the following action, ping catamapp or lightningstormyt ASAP.",
                7:"Command didn't register properly, ping catamapp or lightningstormyt ASAP.",
                8:"Intents not properly enabled, ping catamapp or lightningstormyt ASAP.",
                9:"Connection with Discord failed, please try again later.",
                10:"Connection with Discord failed, please try again later.", 
                11:"Connection with Discord failed, please try again later.", 
                99:f"Unknown Error, please ping catamapp/lightningstormyt ASAP. (ERR ??)\nError Message: {error_msg}\n(IF THIS IS A KEY ERROR IGNORE.)"}

        embedvar = discord.Embed(
            title=f"Error {error_code:02d}",
            description=f"{errors[error_code]}",
            color=discord.Color.red(),
        )
        embedvar.set_footer(text=time_format)
        embedvar.set_thumbnail(url="attachment://WPCO.png")
        if error_code != 99:
            print(f"ERR {error_code:02d}: {time_format} by {user}")

        return embedvar
    
    async def on_command_error(self, ctx, error):
        rprint(f'[[bright_red]ERROR[/bright_red]]', error)
        await ctx.reply(error)

    async def setup_hook(self):
        await self.load_extension("jishaku")
        
        func_commands = os.listdir("./commands")
        for command in func_commands:
            if command.endswith(".py") and not command.startswith("_"):
                try:
                    await self.load_extension(f"commands.{command[:-3]}")
                    rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]SUCCESSFUL[/light_green]] Module \"{command[:-3]}\" has been loaded.')
                except Exception as e:
                    rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[bright_red]ERROR[/bright_red]] Module \"{command[:-3]}\" failed to load.')

bot = Bot()

@bot.event
async def on_ready():
    rprint(f"[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]VERSION[/light_green]] Discord.py version [bright_yellow]{discord.__version__}[/bright_yellow], Bot version [bright_yellow]{BOTVER}[/bright_yellow]")
    rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]SUCCESSFUL[/light_green]] Logged in as [blue]{bot.user}[/blue] (ID: [#cccccc]{bot.user.id}[/#cccccc])')
    #! asyncio stupid, fix this
    await bot.tree.sync()
    rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]SUCCESSFUL[/light_green]] Synced slash commands and loaded jishaku.')
    rprint(f"[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[bright_yellow]WARNING[/bright_yellow]] Please ping catamapp/lightningstormyt for bot maintenance/unhandled errors.")
    rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]COMPLETE[/light_green]] Bot has completed startup and now can be used.')
    try:
        await asyncio.to_thread(playsound3.playsound, "sounds/beep.wav")
    except Exception as e:
        pass

if __name__ == "__main__":
    clear()
    bot.run(load_json("config.json", "token"))