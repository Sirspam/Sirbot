# https://waifu.pics/docs

import discord
import io
import json
import logging
from discord.ext import commands
from random import choice
from os.path import splitext

class Waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # haha very long list
        self.bot.waifu_categories = ["waifu", "neko", "bully", "cuddle", "cry", "hug", "awoo", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "happy", "wink", "poke", "dance", "cringe", "blush"]


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.group(invoke_without_command=True, aliases=["wa"])
    async def waifu(self, ctx, category="waifu"):
        logging.info(f"waifu invoked in {ctx.guild.name}")
        category = category.lower()
        if category == "random":
            category = choice(self.bot.waifu_categories)
        elif category not in self.bot.waifu_categories:
            raise commands.BadArgument
        async with ctx.channel.typing():
            results = await get_image(self, f"sfw/{category}")
            await ctx.reply(file=discord.File(results[0], f"{category}{results[1]}"))
        logging.info("attachment sent")

    @waifu.group(invoke_without_command=True)
    @commands.is_nsfw()
    async def nsfw(self, ctx):
        logging.info(f"nsfw invoked in {ctx.guild.name}")
        async with ctx.channel.typing():
            results = await get_image(self, f"nsfw/waifu")
            await ctx.reply(file=discord.File(results[0], f"nsfw_waifu{results[1]}"))
        logging.info("attachment sent")

    @nsfw.command()
    @commands.is_nsfw()
    async def neko(self, ctx):
        logging.info(f"nsfw neko invoked in {ctx.guild.name}")
        async with ctx.channel.typing():
            results = await get_image(self, f"nsfw/neko")
            await ctx.reply(file=discord.File(results[0], f"nsfw_neko{results[1]}"))
        logging.info("attachment sent")

    @nsfw.command()
    @commands.is_nsfw()
    async def trap(self, ctx):
        logging.info(f"nsfw trap invoked in {ctx.guild.name}")
        async with ctx.channel.typing():
            results = await get_image(self, f"nsfw/trap")
            await ctx.reply(file=discord.File(results[0], f"nsfw_trap{results[1]}"))
        logging.info("attachment sent")


def setup(bot):
    bot.add_cog(Waifu(bot))


async def get_image(self, endpoint):
    logging.info(f"get_image function invoked with {endpoint}")
    link = "https://api.waifu.pics/"+endpoint
    async with self.bot.session.get(link) as resp:
        json_data = json.loads(await resp.text())
        logging.info(json_data["url"])
        async with self.bot.session.get(json_data["url"]) as resp:
            root, ext = splitext(json_data["url"])
            return (io.BytesIO(await resp.read()),ext)
