"This cog is in development, do not load it yet."

import discord, json
from discord.ext import commands

def load_json(path : str, to_load : str, object : str = None) -> any: #* loads stuff from json
    with open(path, mode="r", encoding="utf-8") as read_file:
        load = json.load(read_file)
        
    #* json throws a keyerror if the data is not found.
    try:
        if object != None:
            data = load[object][to_load]
        elif object == None:
            data = load[to_load]
    except KeyError:
        return None

    read_file.close()
    return data

def edit_json(path : str, to_change : str, value, object : str = None): #* Can edit/add
    with open(path, mode="r", encoding="utf-8") as read_file:
        data = json.load(read_file)
        
    if object != None:
        data[object][to_change] = value
    elif object == None:
        data[to_change] = value
    read_file.close()

    with open(path, "w") as outfile:
        json.dump(data, outfile)
    outfile.close()

class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(with_app_command = True, brief = "Increases a user's points.")
    async def points_increase(self, ctx, is_social_credit: bool, target: discord.User, amount: int):
        if is_social_credit:
            point_type = "social_credit"
        elif not is_social_credit:
            point_type = "ration"

        cur_amount = load_json(f"{point_type}.json", target.name)
        if cur_amount is None:
            cur_amount = 0
        edit_json(f"{point_type}.json", target.name, cur_amount+amount)
        await ctx.reply(f"Increased {amount} {point_type}(s) to: {target.name}.")

    @commands.hybrid_command(with_app_command = True, brief = "Decreases a user's points.")
    async def points_decrease(self, ctx, is_social_credit: bool, target: discord.User, amount: int):
        if is_social_credit:
            point_type = "social_credit"
        elif not is_social_credit:
            point_type = "ration"

        cur_amount = load_json(f"{point_type}.json", target.name)
        if cur_amount is None:
            cur_amount = 0
        edit_json(f"{point_type}.json", target.name, cur_amount-amount)
        await ctx.reply(f"Decreased {amount} {point_type}(s) to: {target.name}.")

    @commands.hybrid_command(with_app_command = True, brief = "Sets a user's points to a set amount")
    async def points_set(self, ctx, is_social_credit: bool, target: discord.User, amount: int):
        if is_social_credit:
            point_type = "social_credit"
        elif not is_social_credit:
            point_type = "ration"

        edit_json(f"{point_type}.json", target.name, amount)
        await ctx.reply(f"Set {amount} {point_type}(s) to: {target.name}.")

    @commands.hybrid_command(with_app_command = True, brief = "Returns the mentioned user's points")
    async def points_amount(self, ctx, is_social_credit: bool, target: discord.User):
        if is_social_credit:
            point_type = "social_credit"
        elif not is_social_credit:
            point_type = "ration"
        
        cur_amount = load_json(f"{point_type}.json", target.name)
        if cur_amount is None:
            cur_amount = 0
        await ctx.reply(f"{target.name} has {cur_amount} of {point_type}(s)")

async def setup(bot):
    await bot.add_cog(Points(bot=bot))   