import discord
import logging
from discord.ext import commands
from discord.ext import tasks
from random import choice
from random import getrandbits


play_status_list = [
    "Beat Saber",
    "NEKOPARA Vol. 0",
    "NEKOPARA Vol. 1",
    "NEKOPARA Vol. 2",
    "NEKOPARA Vol. 3",
    "NEKOPARA Vol. 4",
    "Among Us",
    "Amogus"
    "with Nekos 🐾",
    "a muffin map"
]

watch_status_list = [
    "Aso being cute 😳",
    "Sirspam shit miss",
    "Aqua being useless",
    "Nekopara",
    "KonoSuba"
]


class status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=1)
    async def status(self):
        await self.bot.wait_until_ready()
        if getrandbits(1) == 1:
            value = choice(play_status_list)
            await self.bot.change_presence(activity=discord.Game(name=value))
            logging.info(f"Status set to: {value}")
        else:
            value = choice(watch_status_list)
            await self.bot.change_presence(activity=discord.Activity(name=value, type=discord.ActivityType.watching))
            logging.info(f"Status set to: {value}")

    @commands.Cog.listener()
    async def on_ready(self):
        self.status.start()


def setup(bot):
    bot.add_cog(status(bot))