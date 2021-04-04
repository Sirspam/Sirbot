# I can assure you, this cog is vital for the performance and useability of Scuffed b- I mean Sirbot
#https://www.nekos.life/api/v2/endpoints


import discord
import io
import aiohttp
import json
import logging
import asyncio
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
            await ctx.reply(file=discord.File(await image(self, "https://nekos.life/api/v2/img/neko"), "neko.png"))
        logging.info("attachment sent\n----------")
        
    @neko.command()
    async def gif(self, ctx):
        logging.info("neko gif ran")
        async with ctx.channel.typing():
            await ctx.reply(file=discord.File(await image(self, "https://nekos.life/api/v2/img/ngif"), "neko.gif"))
        logging.info("attachment sent\n----------")

    @neko.group(invoke_without_command=True, case_insensitive=True)
    @commands.is_nsfw()
    async def lewd(self, ctx):
        logging.info("neko lewd ran")
        async with ctx.channel.typing():
            await ctx.reply(file=discord.File(await image(self, "https://nekos.life/api/v2/img/lewd"), "neko.png"))
        logging.info("attachment sent\n----------")

    @lewd.command(aliases=["gif"])
    @commands.is_nsfw()
    async def lewd_gif(self, ctx):
        logging.info("neko lewd gif ran")
        async with ctx.channel.typing():
            await ctx.reply(file=discord.File(await image(self, "https://nekos.life/api/v2/img/nsfw_neko_gif"), "neko.gif"))
        logging.info("attachment sent\n----------")

    @commands.group(invoke_without_command=True, case_insensitive=True)
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def batch_neko(self, ctx, argument: int):
        logging.info(f"batch neko ran by {ctx.author.name} ({ctx.author.id})")
        async with ctx.channel.typing():
            await ctx.reply("I'm holding you accountable if I get rate limited")
            count = 0
            while argument != count:
                await ctx.send(file=discord.File(await image(self, "https://nekos.life/api/v2/img/neko"), "neko.png"))
                count = count + 1
                await asyncio.sleep(5)
            await ctx.send("k I'm done, bye")
        logging.info("attachment sent\n----------")

    @batch_neko.command()
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def _gif(self, ctx, argument: int):
        logging.info(f"batch_neko gif ran by {ctx.author.name} ({ctx.author.id})")
        async with ctx.channel.typing():
            await ctx.reply("I'm holding you accountable if I get rate limited")
            count = 0
            while argument != count:
                await ctx.reply(file=discord.File(await image(self, "https://nekos.life/api/v2/img/ngif"), "neko.gif"))
                count = count + 1
                await asyncio.sleep(5)
            await ctx.send("k I'm done, bye")
        logging.info("attachment sent\n----------")

    @batch_neko.group(invoke_without_command=True, case_insensitive=True)
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.is_nsfw()
    async def _lewd(self, ctx, argument: int):
        logging.info(f"neko lewd ran by {ctx.author.name} ({ctx.author.id})")
        async with ctx.channel.typing():
            await ctx.reply("I'm holding you accountable if I get rate limited")
            count = 0
            while argument != count:
                await ctx.send(file=discord.File(await image(self, "https://nekos.life/api/v2/img/lewd"), "neko.png"))
                count = count + 1
                await asyncio.sleep(5)
            await ctx.send("k I'm done, bye")
        logging.info("attachment sent\n----------")

    @lewd.command(aliases=["_gif"])
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.is_nsfw()
    async def _lewd_gif(self, ctx, argument: int):
        logging.info(f"neko lewd gif ran by {ctx.author.name} ({ctx.author.id})")
        async with ctx.channel.typing():
            await ctx.reply("I'm holding you accountable if I get rate limited")
            count = 0
            while argument != count:
                await ctx.send(file=discord.File(await image(self, "https://nekos.life/api/v2/img/nsfw_neko_gif"), "neko.gif"))
                count = count + 1
                await asyncio.sleep(5)
            await ctx.send("k I'm done, bye")
        logging.info("attachment sent\n----------")

def setup(bot):
    bot.add_cog(neko(bot))
