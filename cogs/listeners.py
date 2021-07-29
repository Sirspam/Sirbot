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

    @commands.Cog.listener("before_invoke")
    async def before_invoke(ctx):
        logging.info(f"Invoked {ctx.command} in {ctx.guild.name} by {ctx.author.name}\nArgs: {ctx.args}" )

    @commands.Cog.listener("after_invoke")
    async def after_invoke(ctx):
        logging.info(f"Concluded {ctx.command}")


def setup(bot):
    bot.add_cog(Listeners(bot))
