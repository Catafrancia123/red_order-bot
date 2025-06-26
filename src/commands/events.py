from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(with_app_command = True, brief = "uhh my head hurts")
    async def test(self, ctx): 
        await ctx.reply("uhh my head hurts\n- WPCO AI Bot")

async def setup(bot):
    await bot.add_cog(Events(bot=bot))