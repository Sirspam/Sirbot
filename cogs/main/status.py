import discord
import logging
from discord.ext import commands
from discord.ext import tasks
from random import randint
from utils import prefixes


play_status_list = [
    "Beat Saber",
    "NEKOPARA Vol. 0",
    "NEKOPARA Vol. 1",
    "NEKOPARA Vol. 2",
    "NEKOPARA Vol. 3",
    "NEKOPARA Vol. 4",
    "With Nekos 🐾"
]

watch_status_list = [
    "Aso being cute 😳",
    "Sirspam shit miss",
    "Nekopara"
]


class status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=1)
    async def status(self):
        await self.bot.wait_until_ready()
        if (randint(0, 1)) == 0:
            value = (randint(0, len(play_status_list)))-1
            await self.bot.change_presence(activity=discord.Game(name=play_status_list[value]))
            logging.info(f"Status set to: {play_status_list[value]}")
        else:
            value = (randint(0, len(watch_status_list)))-1
            await self.bot.change_presence(activity=discord.Activity(name=watch_status_list[value], type=discord.ActivityType.watching))
            logging.info(f"Status set to: {watch_status_list[value]}")

    @commands.Cog.listener()
    async def on_ready(self):
        self.status.start()


def setup(bot):
    bot.add_cog(status(bot))