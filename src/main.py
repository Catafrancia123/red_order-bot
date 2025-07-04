""" Version 1.2-dev1:
    - Added a currency to the bot (Social credits & Rations)
    - SQLite implementation (nearly)"""

import discord, datetime, os, sys, asyncio, playsound3
from dotenv import load_dotenv
from pathlib import Path
from discord.ext import commands
from rich import print as rprint

def clear():
    if sys.platform.startswith(('win32')):
        os.system('cls')
    elif sys.platform.startswith(('linux', 'cygwin', 'darwin', 'freebsd')):
        os.system('clear')

BOTVER = "1.2-dev1"
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
                99:f"An error happened, please contact the developers.\nError Message: ```{error_msg}```"}

        embedvar = discord.Embed(
            title=f"Error {error_code:02d}",
            description=f"{errors[error_code]}",
            color=discord.Color.red(),
        )
        embedvar.set_footer(text=time_format)
        if error_code != 99:
            print(f"ERR {error_code:02d}: {time_format} by {user}")

        return embedvar

    async def setup_hook(self):
        rprint(f"[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]VERSION[/light_green]] Discord.py version [bright_yellow]{discord.__version__}[/bright_yellow], Bot version [bright_yellow]{BOTVER}[/bright_yellow]")
        await self.load_extension("jishaku")
        rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]SUCCESSFUL[/light_green]] Synced slash commands and loaded jishaku.')
        
        func_commands = Path("./commands")
        counter = 0
        for command in [str(x) for x in func_commands.iterdir() if x.is_file()]:
            if counter >= 3:
                break
            
            try:   
                await self.load_extension(command.replace("\\", ".")[:-3])
                rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]SUCCESSFUL[/light_green]] Module \"{command[:-3]}\" has been loaded.')
            except Exception as e:
                rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[bright_red]ERROR[/bright_red]] Module \"{command[:-3]}\" failed to load.')
                print(e)
            counter += 1
        await self.tree.sync()

bot = Bot()

@bot.event
async def on_ready():
    rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]SUCCESSFUL[/light_green]] Logged in as [blue]{bot.user}[/blue] (ID: [#cccccc]{bot.user.id}[/#cccccc])')
    rprint(f"[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[bright_yellow]WARNING[/bright_yellow]] Please ping catamapp for bot maintenance/unknown errors.")
    rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]COMPLETE[/light_green]] Bot has completed startup and now can be used.')
    try:
        await asyncio.to_thread(playsound3.playsound, "sounds/beep.wav")
    except Exception as e:
        pass

@bot.event
async def on_command_error(ctx, error):
    user = ctx.author
    time = datetime.datetime.now()
    time_format = time.strftime('%A, %d %B %Y, %I:%M %p') 
    if isinstance(error, commands.CommandNotFound):
        #! command not found
        await ctx.send(embed=bot.make_error_embed(user.name,1))
    elif isinstance(error, commands.MissingRequiredArgument):
        #! no input
        await ctx.send(embed=bot.make_error_embed(user.name,2))
    elif isinstance(error, commands.BadArgument):
        #! input not valid/wrong
        await ctx.send(embed=bot.make_error_embed(user.name,3))
    elif isinstance(error, commands.MissingAnyRole):
        #! no perms?
        await ctx.send(embed=bot.make_error_embed(user.name,4))
    elif isinstance(error, discord.HTTPException):
        #! discord.py error
        await ctx.send(embed=bot.make_error_embed(user.name,5))
    elif isinstance(error, commands.CheckFailure):
        #! not registered
        await ctx.send(embed=bot.make_error_embed(user.name,6))
    elif isinstance(error, discord.Forbidden):
        #! bot doesnt have perm to do an action
        await ctx.send(embed=bot.make_error_embed(user.name,7))
    elif isinstance(error, commands.CommandRegistrationError):
        #! command registration failed
        await ctx.send(embed=bot.make_error_embed(user.name,8))
    elif isinstance(error, discord.PrivilegedIntentsRequired):
        #! intents not properly enabled
        await ctx.send(embed=bot.make_error_embed(user.name,9))
    elif isinstance(error, discord.ConnectionClosed):
        #! connection with discord closed
        await ctx.send(embed=bot.make_error_embed(user.name,10))
    elif isinstance(error, discord.GatewayNotFound):
        #! connection with discord gateaway failed
        await ctx.send(embed=bot.make_error_embed(user.name,11))
    elif isinstance(error, discord.NotFound):
        #! 404 not found
        await ctx.send(embed=bot.make_error_embed(user.name,12))
    else:
        #! what happen?? (python error or smth)
        rprint(f"[[bright_red]ERROR[/bright_red]] Unknown error: {error}\n{time_format}")
        await ctx.send(embed=bot.make_error_embed(user.name,error_msg=error))

if __name__ == "__main__":
    clear()
    load_dotenv()
    bot.run(os.getenv("token"))