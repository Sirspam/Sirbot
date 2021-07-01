# https://waifu.pics/docs

import logging
from io import BytesIO
from json import loads
from random import choice

from discord import File, HTTPException

from discord.ext import commands
from os.path import splitext


class Waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # haha funny long list
        self.bot.waifu_categories = ["waifu", "neko", "bully", "cuddle", "cry", "hug", "awoo", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "happy", "wink", "poke", "dance", "cringe", "blush"]


    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.group(invoke_without_command=True, aliases=["wa"])
    async def waifu(self, ctx, category="waifu"):
        category = category.lower()
        if category == "random":
            category = choice(self.bot.waifu_categories)
        # The nya and awoo ifs allow a wee bit of tomfoolery and have a long nya/awoo still work. There's likely a better alternative for doing it though.
        elif "nya" in category:
            category = "neko"
        elif "awoo" in category:
            category = "awoo"
        elif category not in self.bot.waifu_categories:
            raise commands.BadArgument
        async with ctx.channel.typing():
            results = await get_image(self, f"sfw/{category}")
            try:
                await ctx.reply(file=File(results[0], f"{category}{results[1]}"))
            except HTTPException:
                await ctx.reply(results[2])

    @waifu.group(invoke_without_command=True)
    @commands.is_nsfw()
    async def nsfw(self, ctx):
        async with ctx.channel.typing():
            results = await get_image(self, f"nsfw/waifu")
            try:
                await ctx.reply(file=File(results[0], f"nsfw_waifu{results[1]}"))
            except HTTPException:
                await ctx.reply(results[2])

    @nsfw.command()
    @commands.is_nsfw()
    async def neko(self, ctx):
        async with ctx.channel.typing():
            results = await get_image(self, f"nsfw/neko")
            try:
                await ctx.reply(file=File(results[0], f"nsfw_waifu{results[1]}"))
            except HTTPException:
                await ctx.reply(results[2])

    @nsfw.command()
    @commands.is_nsfw()
    async def trap(self, ctx):
        async with ctx.channel.typing():
            results = await get_image(self, f"nsfw/trap")
            try:
                await ctx.reply(file=File(results[0], f"nsfw_waifu{results[1]}"))
            except HTTPException:
                await ctx.reply(results[2])


def setup(bot):
    bot.add_cog(Waifu(bot))


async def get_image(self, endpoint):
    logging.info(f"get_image function invoked with {endpoint}")
    link = "https://api.waifu.pics/"+endpoint
    async with self.bot.session.get(link) as resp:
        url = loads(await resp.text())["url"]
        logging.info(url)
        async with self.bot.session.get(url) as resp:
            root, ext = splitext(url)
            return (BytesIO(await resp.read()),ext,url)
