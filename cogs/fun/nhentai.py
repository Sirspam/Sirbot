# https://pypi.org/project/NHentai-API/

import discord
import logging
from discord.ext import commands
from NHentai import NHentai

nhentai = NHentai()


async def sauce_embed(sauce):
    tags = str()
    for x in getattr(sauce, "tags"):
        tags = tags + x + ", "
    artist = str()
    for x in getattr(sauce, "artists"):
        artist = artist + x + ", "
    parodies = str()
    for x in getattr(sauce, "parodies"):
        parodies = parodies + x + ", "
    sec_title = "**Alternative Title:** "
    for x in getattr(sauce, "secondary_title"):
        sec_title = sec_title + x
    characters = str()
    for x in getattr(sauce, "characters"):
        characters = characters + x + ", "
    if "english" in getattr(sauce, "languages"):
        lang = "🇬🇧"
    elif "japanese" in getattr(sauce, "languages"):
        lang = "🇯🇵"
    elif "chinese" in getattr(sauce, "languages"):
        lang = "🇨🇳"
    else: 
        lang = "❔"
    embed = discord.Embed(
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

    @commands.is_nsfw()
    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["nh"])
    async def nhentai(self, ctx, *, argument=None):
        logging.info("nhentai ran")
        if argument is None:
            sauce = nhentai.get_random()
            logging.info(sauce)
            await ctx.send(embed=await sauce_embed(sauce))
            logging.info("Posted embed\n----------")
        elif argument.isdigit():
            sauce = nhentai._get_doujin(id=argument)
            logging.info(sauce)
            if sauce is None:
                return await ctx.send("S-Sorry, I can't find that id qwq")
            await ctx.send(embed=await sauce_embed(sauce))
            logging.info("Posted embed\n----------")

def setup(bot):
    bot.add_cog(NHentaiCog(bot))
