import discord
from discord.ext import commands
import time
import random
import asyncio


class Dice(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog <Dice.py> is online. {time.time()}")

    # Commands
    @commands.command(aliases=["dice"])
    async def roll(self, ctx, roll, modifier=0):
        parts = roll.split("d")
        count = int(parts[0])
        die = int(parts[1])

        rolls = []
        for i in range(count):
            rolls.append(random.randint(1, die))
        total = sum(rolls) + modifier
        if sum(rolls) == 20 and count == 1 and die == 20:
            await ctx.send(
                f"{ctx.author.mention} rolled a **{total}** with {count} {die}-sided dice:\n{rolls}\nand the modifier of:\n{modifier}\n*Critical success!*")
        elif sum(rolls) == 1 and count == 1 and die == 20:
            await ctx.send(
                f"{ctx.author.mention} rolled a **{total}** with {count} {die}-sided dice:\n{rolls}\nand the modifier of:\n{modifier}\n*Critical failure!*")
        else:
            await ctx.send(
                f"{ctx.author.mention} rolled a **{total}** with {count} {die}-sided dice:\n{rolls}\nand the modifier of:\n{modifier}")

    @commands.command(aliases=["gr"])
    async def group_roll(self, ctx, roll):

        message = await ctx.send("React to this message within 20 seconds to join the roll")
        await message.add_reaction("✅")

        await asyncio.sleep(20)

        roll = "".join([i for i in roll if i != " "])
        parts = roll.split("d")
        count = int(parts[0])
        die = int(parts[1])

        message = await ctx.channel.fetch_message(message.id)

        reaction = message.reactions[0]

        users = []

        async for u in reaction.users():
            users.append(u)

        e = discord.Embed(title="Group roll", description=roll)
        for user in users:
            if user.bot:
                continue
            result = sum([random.randint(1, die) for i in range(count)])
            e.add_field(name=user.name, value=result, inline=False)
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Dice(client))
