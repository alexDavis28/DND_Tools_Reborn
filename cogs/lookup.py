import discord
from discord.ext import commands
import time
import requests


class Lookup(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog <Lookup.py> is online. {time.time()}")

    # Commands
    @commands.command(aliases=["find"])
    async def search(self, ctx, *, text):
        url = f"https://api.open5e.com/search/?format=json&text=%22{text}%22"
        page = requests.get(url).json()
        result = page["results"][0]
        embed = discord.Embed(title=result["name"], description=result["highlighted"],
                              color=discord.Colour.from_rgb(236, 33, 39))
        await ctx.send(embed=embed)

    @commands.command()
    async def spell(self, ctx, *, text):
        url = f"https://api.open5e.com/spells/?format=json&search={text}"
        page = requests.get(url).json()
        results = page["results"]
        result = results[0]
        for r in results:
            if r["name"].lower() == text.lower():
                result = r

        embed = discord.Embed(title=result["name"], color=discord.Colour.from_rgb(148, 0, 211))
        embed.add_field(name="Description", value=result['desc'][:1024], inline=False)

        if result["higher_level"] != "":
            embed.add_field(name="Higher Level", value=result["higher_level"], inline=False)
        embed.add_field(name="Range", value=result["range"], inline=False)
        embed.add_field(name="Duration", value=result["duration"], inline=False)
        embed.add_field(name="Casting time", value=result["casting_time"], inline=False)
        embed.add_field(name="Level", value=result["level"], inline=False)
        embed.add_field(name="Class", value=result["dnd_class"], inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def monster(self, ctx, *, text):

        url = f"https://api.open5e.com/monsters/?format=json&search={text}"
        page = requests.get(url).json()
        results = page["results"]
        result = results[0]
        for r in results:
            if r["name"].lower() == text.lower():
                result = r

        embed = discord.Embed(title=result["name"], color=discord.Colour.from_rgb(255, 0, 0))

        embed.add_field(name="Challenge Rating", value=result["challenge_rating"], inline=False)
        embed.add_field(name="Type", value=result["type"], inline=False)
        embed.add_field(name="Alignment", value=result["alignment"], inline=False)
        embed.add_field(name="Armor class", value=result["armor_class"], inline=False)
        embed.add_field(name="Armor", value=result["armor_desc"], inline=False)
        embed.add_field(name="Health", value=f'Hit points: ({result["hit_points"]})\n Hit dice: ({result["hit_dice"]})',
                        inline=False)

        speeds = []
        for value in result["speed"]:
            speeds.append(f'{value}: {result["speed"][value]}')
        speed = "\n".join(speeds)

        embed.add_field(name="Speed", value=speed, inline=False)

        embed.add_field(name="Stats",
                        value=f'Strength:{result["strength"]}\nDexterity:{result["dexterity"]}\nConstitution:{result["constitution"]}\nIntelligence:{result["intelligence"]}\nWisdom:{result["wisdom"]}\nCharisma:{result["charisma"]}\n')
        embed.add_field(name="Senses", value=result["senses"], inline=False)

        for action in result["actions"]:
            embed.add_field(name=action["name"], value=action["desc"], inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def condition(self, ctx, *, text):
        url = f"https://api.open5e.com/conditions/?format=json&search={text}"
        page = requests.get(url).json()
        results = page["results"]
        result = results[0]
        for r in results:
            if r["name"].lower() == atext.lower():
                result = r

        embed = discord.Embed(title=result["name"], color=discord.Colour.from_rgb(0, 255, 0))

        embed.add_field(name="Description", value=result["desc"], inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def race(self, ctx, *, text):
        url = f"https://api.open5e.com/races/?format=json&search={text}"
        page = requests.get(url).json()
        results = page["results"]
        result = results[0]
        for r in results:
            if r["name"].lower() == text.lower():
                result = r

        embed = discord.Embed(title=result["name"], color=discord.Colour.from_rgb(169, 169, 169))

        embed.add_field(name="Description", value=(result["desc"].split("\n")[1]), inline=False)
        embed.add_field(name="Ability score increase", value=result["asi_desc"][29:], inline=False)
        embed.add_field(name="Age", value=result["age"][11:], inline=False)
        embed.add_field(name="Size", value=result["size"][12:], inline=False)
        embed.add_field(name="Speed", value=result["speed_desc"][13:], inline=False)
        embed.add_field(name="Languages", value=result["languages"][17:], inline=False)
        embed.add_field(name="Vision", value=result["vision"], inline=False)
        embed.add_field(name="Traits", value=result["traits"])

        await ctx.send(embed=embed)

    @commands.command(aliases=["class"])
    async def _class(self, ctx, *, text):
        url = f"https://api.open5e.com/classes/?format=json&search={text}"
        page = requests.get(url).json()
        results = page["results"]
        result = results[0]
        for r in results:
            if r["name"].lower() == text.lower():
                result = r

        embed = discord.Embed(title=result["name"], color=discord.Colour.from_rgb(0, 191, 255))
        embed.add_field(name="Health",
                        value=f'At first level, you start with {result["hit_dice"]} hit dice. Your HP at 1st level is {result["hp_at_1st_level"]}. At higher levels, your HP is {result["hp_at_higher_levels"]}',
                        inline=False)
        embed.add_field(name="Proficiencies", value=f'{result["prof_armor"]}\n{result["prof_weapons"]}', inline=False)
        embed.add_field(name="Equipment", value=result["equipment"], inline=False)
        # embed.add_field(name="Spellcasting ability", value=result["spellcasting"], inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["class_desc"])
    async def class_description(self, ctx, *, text):
        url = f"https://api.open5e.com/classes/?format=json&search={text}"
        page = requests.get(url).json()
        results = page["results"]
        result = results[0]
        for r in results:
            if r["name"].lower() == text.lower():
                result = r

        desc = result["desc"].split("\n")

        for i in desc:
            print(f"{i} is type: {type(i)}")
            if i == "" or i is None or len(i) == 1:
                print("oh no")
                pass
            else:
                await ctx.author.send(i)
        await ctx.send(f"Sent class description to {ctx.author.mention}")

    @commands.command()
    async def class_table(self, ctx, dnd_class, level_num=0):
        url = f"https://api.open5e.com/classes/?format=json&search={dnd_class}"
        page = requests.get(url).json()
        results = page["results"]
        result = results[0]
        for r in results:
            if r["name"].lower() == dnd_class.lower():
                result = r
        table = result["table"]

        table_lines = table.split("\n")
        del table_lines[1]

        formatted_lines = []
        for line in table_lines:
            formatted_line = line.split('|')
            formatted_line = [i for i in formatted_line if i != ""]
            formatted_lines.append(formatted_line)

        categories = formatted_lines[0]

        level_lines = formatted_lines[1:len(formatted_lines)]
        levels = []
        for line in level_lines:
            levels.append([line[0], line[1:len(line)]])
        # await ctx.send(levels)

        embed = discord.Embed(title=f'Class table for {result["name"]}', color=discord.Colour.from_rgb(0, 191, 255))

        if level_num == 0:
            await ctx.send("Please specify level")
        else:
            print(f"level {level_num}")
            level = levels[int(level_num) - 1]
            desc = []
            for i, part in enumerate(level[1]):
                desc.append(f"{categories[i + 1]}: {part}\n")
            desc = "".join(desc)

            embed.add_field(name=level[0], value=desc, inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    async def weapon(self, ctx, *, text):
        url = f"https://api.open5e.com/weapons/?format=json&search={text}"
        page = requests.get(url).json()
        results = page["results"]
        result = results[0]
        for r in results:
            if r["name"].lower() == text.lower():
                result = r

        embed = discord.Embed(title=result["name"], color=discord.Colour.from_rgb(255, 255, 255))
        embed.add_field(name="Category", value=result["category"], inline=False)
        embed.add_field(name="Cost", value=result["cost"], inline=False)
        embed.add_field(name="Damage", value=f'{result["damage_dice"]} {result["damage_type"]} damage', inline=False)
        embed.add_field(name="Properties", value="\n".join(result["properties"]), inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Lookup(client))
