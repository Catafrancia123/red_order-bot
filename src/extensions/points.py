"This cog is in development, do not load it yet."

import discord, sys, os, sqlite3
from discord.ext import commands
sys.path.append(os.path.abspath(os.path.join('..', 'schemas')))
from schemas.saveloader import load, add, edit

SAVE = "save.db"

class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(with_app_command = True, brief = "Increases a user's points.")
    async def points_increase(self, ctx, is_social_credit: bool, target: discord.User, amount: int):
        if is_social_credit:
            point_type = "social_credit"
        elif not is_social_credit:
            point_type = "ration"

        cur_amount = await load(SAVE, point_type, target.name)
        if cur_amount is None:
            await add(SAVE, point_type, target.name, 0)
            cur_amount = 0
        await edit(SAVE, point_type, target.name, cur_amount+amount)
        await ctx.reply(f"Increased {amount} {point_type}(s) to: {target.name}.")

    @commands.hybrid_command(with_app_command = True, brief = "Decreases a user's points.")
    async def points_decrease(self, ctx, is_social_credit: bool, target: discord.User, amount: int):
        if is_social_credit:
            point_type = "social_credit"
        elif not is_social_credit:
            point_type = "ration"

        cur_amount = await load(SAVE, point_type, target.name)
        if cur_amount is None:
            await add(SAVE, point_type, target.name, 0)
            cur_amount = 0
        await edit(SAVE, point_type, target.name, cur_amount-amount)
        await ctx.reply(f"Decreased {amount} {point_type}(s) to: {target.name}.")

    @commands.hybrid_command(with_app_command = True, brief = "Sets a user's points to a set amount")
    async def points_set(self, ctx, is_social_credit: bool, target: discord.User, amount: int):
        if is_social_credit:
            point_type = "social_credit"
        elif not is_social_credit:
            point_type = "ration"

        cur_amount = await load(SAVE, point_type, target.name)
        if cur_amount is None:
            await add(SAVE, point_type, target.name, amount)
        else:
            await edit(SAVE, point_type, target.name, amount)
        await ctx.reply(f"Set to {amount} {point_type}(s) to: {target.name}.")

    @commands.hybrid_command(with_app_command = True, brief = "Returns the mentioned user's points")
    async def points_amount(self, ctx, is_social_credit: bool, target: discord.User = None):
        if target is None:
            target = ctx.author
        
        if is_social_credit:
            point_type = "social_credit"
        elif not is_social_credit:
            point_type = "ration"
        
        cur_amount = await load(SAVE, point_type, target.name)
        if cur_amount is None:
            await add(SAVE, point_type, target.name, 0)
            cur_amount = 0
        await ctx.reply(f"{target.name} has {cur_amount} {point_type}(s)")

async def setup(bot):
    await bot.add_cog(Points(bot=bot))   