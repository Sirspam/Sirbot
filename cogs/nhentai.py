# https://pypi.org/project/NHentai-API/

import logging

from discord import Embed

from discord.ext import commands
from NHentai.nhentai_async import NHentaiAsync

nhentai = NHentaiAsync()


async def sauce_embed(sauce):
    tags = str()
    for x in getattr(sauce, "tags"):
        tags = tags + x + ", "
    if tags == str():
        tags = "None"
    artist = str()
    for x in getattr(sauce, "artists"):
        artist = artist + x + ", "
    if artist == str():
        artist = "None"
    parodies = str()
    for x in getattr(sauce, "parodies"):
        parodies = parodies + x + ", "
    if artist == str():
        artist = "None"
    sec_title = "**Alternative Title:** "
    for x in getattr(sauce, "secondary_title"):
        sec_title = sec_title + x
    characters = str()
    for x in getattr(sauce, "characters"):
        characters = characters + x + ", "
    if artist == str():
        artist = "None"
    if "english" in getattr(sauce, "languages"):
        lang = "🇬🇧"
    elif "japanese" in getattr(sauce, "languages"):
        lang = "🇯🇵"
    elif "chinese" in getattr(sauce, "languages"):
        lang = "🇨🇳"
    else: 
        lang = "❔"
    embed = Embed(
        title=f"{lang} "+getattr(sauce,"title"),
        url="https://nhentai.net/g/"+getattr(sauce,"id")+"/",
        description=sec_title,
        colour=0xec2753,
    )
    embed.add_field(
        name="Tags",
        value=tags,
        inline=False
    )
    embed.add_field(
        name="Artists",
        value=artist,
        inline=True
    )
    if parodies:
        embed.add_field(
            name="Parodies",
            value=parodies,
            inline=True
        )
    if characters:
        embed.add_field(
            name="Characters",
            value=characters,
            inline=False
        )
    embed.set_footer(text=str(getattr(sauce,"total_pages"))+" total pages")
    embed.set_image(url=(getattr(sauce,"images"))[0])
    return embed


class NHentaiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def cog_before_invoke(self, ctx):
        logging.info(f"Invoked {ctx.command} in {ctx.guild.name} by {ctx.author.name}\nArgs: {ctx.args}" )

    async def cog_after_invoke(self, ctx):
        logging.info(f"Concluded {ctx.command}")


    @commands.is_nsfw()
    @commands.group(invoke_without_command=True, aliases=["nh"])
    async def nhentai(self, ctx, *, argument=None):
        logging.info(f"nhentai ran in {ctx.guild.name}")
        if argument is None:
            sauce = await nhentai.get_random()
        elif argument.isdigit():
            sauce = await nhentai._get_doujin(id=argument)
            if sauce is None:
                raise commands.BadArgument
        else:
            raise commands.BadArgument
        await ctx.send(embed=await sauce_embed(sauce))
        logging.info("successfully concluded nhentai")

def setup(bot):
    bot.add_cog(NHentaiCog(bot))
