import discord, datetime
from pathlib import Path
from discord.ext import commands
from saveloader import load_json

parent = Path("./").cwd().parent
save = f"{parent}/src/config.json"

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logo = discord.File("images/logo.png", filename="logo.png")
        self.time_format = datetime.datetime.strftime(datetime.datetime.now(datetime.timezone.utc), "Today at %I:%M %p UTC.")

    @commands.hybrid_command(with_app_command = True, brief = "Hosts a deployment.")
    async def deployment(self, ctx, time_unix: int, location: str, text: str, host: discord.Member = None):
        if not host:
            user = ctx.author
        else:
            user = host

        embedvar = discord.Embed(
            title="Deployment",
            description=f"## Host: <@{user.id}>\nTime: <t:{time_unix}:t>, <t:{time_unix}:R>\nPlace: {location}\n\n{text}",
            color=discord.Color.red(),
        )
        embedvar.set_footer(text=self.time_format)
        
        await ctx.send(f"<@&{load_json(save, "member_role", "settings")}>", embed=embedvar)

    @commands.hybrid_command(with_app_command = True, brief = "Hosts a training.")
    async def training(self, ctx, type: str, time_unix: int, text: str, host: discord.Member = None):
        if not host:
            user = ctx.author
        else:
            user = host

        embedvar = discord.Embed(
            title=f"{type} Training",
            description=f"### Host: <@{user.id}>\nTime: <t:{time_unix}:t>, <t:{time_unix}:R>\n\n{text}",
            color=discord.Color.red(),
        )
        embedvar.set_footer(text=self.time_format)
        
        await ctx.send(f"<@&{load_json(save, "member_role", "settings")}>", embed=embedvar)

    @commands.hybrid_command(with_app_command = True, brief = "Hosts a tryout.")
    async def tryout(self, ctx, time_unix: int, location: str, text: str, host: discord.Member = None):
        if not host:
            user = ctx.author
        else:
            user = host

        embedvar = discord.Embed(
            title="A tryout is being hosted!",
            description=f"### Host: <@{user.id}>\nTime: <t:{time_unix}:t>, <t:{time_unix}:R>\nPlace: {location}\n\n{text}",
            color=discord.Color.red(),
        )
        embedvar.set_footer(text=self.time_format)
        
        await ctx.send(f"<@&{load_json(save, "member_role", "settings")}>", embed=embedvar)

async def setup(bot):
    await bot.add_cog(Events(bot=bot))