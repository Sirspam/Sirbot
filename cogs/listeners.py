import logging

from discord.ext import commands
from utils.prefixes import prefix_delete

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_connect")
    async def on_connect(self):
        logging.info("Connected to Discord")

    @commands.Cog.listener("on_disconnect")
    async def on_disconnect(self):
        logging.info("Disconnected from Discord")

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        logging.info(f"Bot has successfully launched as {self.bot.user}")

    @commands.Cog.listener("on_guild_remove")
    async def on_guild_remove(guild):
        logging.info(f"Left guild: {guild.name}")
        await prefix_delete(guild.id)


def setup(bot):
    bot.add_cog(Listeners(bot))
