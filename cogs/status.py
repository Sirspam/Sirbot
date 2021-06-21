import logging
from random import choice, getrandbits

from discord import Game, Activity, ActivityType

from discord.ext import commands, tasks


play_status_list = [
    "Beat Saber",
    "Shiny Happy Days",
    "USAO Ultimate Hyper Mega Mix",
    "NEKOPARA Vol. 0",
    "NEKOPARA Vol. 1",
    "NEKOPARA Vol. 2",
    "NEKOPARA Vol. 3",
    "NEKOPARA Vol. 4",
    "Among Us",
    "Amogus",
    "a muffin map"
]

watch_status_list = [
    "Aso being cute 😳",
    "Sirspam shit miss",
    "Aqua being useless",
    "Nekopara",
    "KonoSuba",
]


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=1)
    async def status(self):
        await self.bot.wait_until_ready()
        if getrandbits(1) == 1:
            value = choice(play_status_list)
            await self.bot.change_presence(activity=Game(name=value))
            logging.info(f"Status set to: {value}")
        else:
            value = choice(watch_status_list)
            await self.bot.change_presence(activity=Activity(name=value, type=ActivityType.watching))
            logging.info(f"Status set to: {value}")

    @commands.Cog.listener()
    async def on_ready(self):
        self.status.start()


def setup(bot):
    bot.add_cog(Status(bot))