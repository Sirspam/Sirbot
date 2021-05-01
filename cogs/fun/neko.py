# I can assure you, this cog is vital for the performance and useability of Scuffed b- I mean Sirbot
#https://www.nekos.life/api/v2/endpoints


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


class Neko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def neko(self, ctx):
        logging.info(f"Recieved neko in {ctx.guild.name}")
        async with ctx.channel.typing():
            await ctx.reply(file=discord.File(await image(self, "https://nekos.life/api/v2/img/neko"), "neko.png"))
        logging.info("attachment sent")
        
    @neko.command()
    async def gif(self, ctx):
        logging.info(f"Recieved neko gif in {ctx.guild.name}")
        async with ctx.channel.typing():
            await ctx.reply(file=discord.File(await image(self, "https://nekos.life/api/v2/img/ngif"), "neko.gif"))
        logging.info("attachment sent")

    @neko.group(invoke_without_command=True, case_insensitive=True)
    @commands.is_nsfw()
    async def lewd(self, ctx):
        logging.info(f"Recieved neko lewd in {ctx.guild.name}")
        async with ctx.channel.typing():
            await ctx.reply(file=discord.File(await image(self, "https://nekos.life/api/v2/img/lewd"), "neko.png"))
        logging.info("attachment sent")

    @lewd.command(aliases=["gif"])
    @commands.is_nsfw()
    async def lewd_gif(self, ctx):
        logging.info(f"Recieved neko lewd gif in {ctx.guild.name}")
        async with ctx.channel.typing():
            await ctx.reply(file=discord.File(await image(self, "https://nekos.life/api/v2/img/nsfw_neko_gif"), "neko.gif"))
        logging.info("attachment sent")


def setup(bot):
    bot.add_cog(Neko(bot))
