# I can assure you, this cog is vital for the performance and useability of Scuffed b- I mean Sirbot

import discord
import io
import aiohttp
import json
from discord.ext import commands
from utils import logger

async def image(self, link):
    await logger.log_info(self, f"image function ran with {link}")
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            json_data = json.loads(await resp.text())
            await logger.log_info(self, json_data["url"])
            async with session.get(json_data["url"]) as resp:
                return io.BytesIO(await resp.read())


class neko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def neko(self, ctx):
        await logger.log_info(self, "neko ran")
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(await image(self, "https://nekos.life/api/v2/img/neko"), "neko.png"))
        await logger.log_info(self, "attachment sent\n----------")
        
    @neko.command()
    async def gif(self, ctx):
        await logger.log_info(self, "neko gif ran")
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(await image(self, "https://nekos.life/api/v2/img/ngif"), "neko.gif"))
        await logger.log_info(self, "attachment sent\n----------")

    @neko.group(invoke_without_command=True, case_insensitive=True)
    async def lewd(self, ctx):
        await logger.log_info(self, "neko lewd ran")
        if ctx.guild and ctx.channel.is_nsfw() is False:
            await logger.log_info(self, "Ran outside of nsfw channel\n----------")
            return await ctx.send("How lewd of you <:AYAYAFlushed:822094723199008799>")
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(await image(self, "https://nekos.life/api/v2/img/lewd"), "neko.png"))
        await logger.log_info(self, "attachment sent\n----------")

    @lewd.command(aliases=["gif"])
    async def lewd_gif(self, ctx):
        await logger.log_info(self, "neko lewd gif ran")
        if ctx.guild and ctx.channel.is_nsfw() is False:
            await logger.log_info(self, "Ran outside of nsfw channel\n----------")
            return await ctx.send("How lewd of you <:AYAYAFlushed:822094723199008799>")
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(await image(self, "https://nekos.life/api/v2/img/nsfw_neko_gif"), "neko.gif"))
        await logger.log_info(self, "attachment sent\n----------")


def setup(bot):
    bot.add_cog(neko(bot))