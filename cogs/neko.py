# https://nekos.life/api/v2/endpoints

import logging
from io import BytesIO
from json import loads

from discord import File, HTTPException

from discord.ext import commands
from os.path import splitext


class Neko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(aliases=["nya"])
    async def neko(self, ctx):
        async with ctx.channel.typing():
            results = await get_image(self)
            try:
                await ctx.reply(file=File(results[0], f"kawaii_neko{results[1]}"))
            except HTTPException:
                await ctx.reply(results[2])


def setup(bot):
    bot.add_cog(Neko(bot))


async def get_image(self):
    async with self.bot.session.get("https://nekos.life/api/v2/img/neko") as resp:
        url = loads(await resp.text())["url"]
        logging.info(url)
        async with self.bot.session.get(url) as resp:
            root, ext = splitext(url)
            return (BytesIO(await resp.read()),ext,url)
