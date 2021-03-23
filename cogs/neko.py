# I can assure you, this cog is vital for the performance and useability of Scuffed b- I mean Sirbot

import discord
import io
import aiohttp
import json
import logging
from discord.ext import commands

async def image(self, link):
    logging.info(f"image function ran with {link}")
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            json_data = json.loads(await resp.text())
            logging.info(json_data["url"])
            async with session.get(json_data["url"]) as resp:
                return io.BytesIO(await resp.read())


class neko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def neko(self, ctx):
        logging.info("neko ran")
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(await image(self, "https://nekos.life/api/v2/img/neko"), "neko.png"))
        logging.info("attachment sent\n----------")
        
    @neko.command()
    async def gif(self, ctx):
        logging.info("neko gif ran")
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(await image(self, "https://nekos.life/api/v2/img/ngif"), "neko.gif"))
        logging.info("attachment sent\n----------")

    @neko.group(invoke_without_command=True, case_insensitive=True)
    async def lewd(self, ctx):
        logging.info("neko lewd ran")
        if ctx.guild and ctx.channel.is_nsfw() is False:
            logging.info("Ran outside of nsfw channel\n----------")
            return await ctx.send("How lewd of you <:AYAYAFlushed:822094723199008799>")
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(await image(self, "https://nekos.life/api/v2/img/lewd"), "neko.png"))
        logging.info("attachment sent\n----------")

    @lewd.command(aliases=["gif"])
    async def lewd_gif(self, ctx):
        logging.info("neko lewd gif ran")
        if ctx.guild and ctx.channel.is_nsfw() is False:
            logging.info("Ran outside of nsfw channel\n----------")
            return await ctx.send("How lewd of you <:AYAYAFlushed:822094723199008799>")
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(await image(self, "https://nekos.life/api/v2/img/nsfw_neko_gif"), "neko.gif"))
        logging.info("attachment sent\n----------")


def setup(bot):
    bot.add_cog(neko(bot))
