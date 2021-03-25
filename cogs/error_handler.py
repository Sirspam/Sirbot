import math
import logging
from discord.ext import commands


class error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        logging.info(f"on_command_error triggered")
        if isinstance(error, commands.BadArgument):
            logging.info("BadArgument handler ran\n----------")
            return await ctx.send(f"You've given a bad argument!\nCheck ``{ctx.prefix}help`` for what arguments you need to give", delete_after=20)

        elif isinstance(error, commands.CommandNotFound):
            logging.info("CommandNotFound handler ran\n----------")
            return await ctx.send("Command not found", delete_after=20)

        elif isinstance(error, commands.BotMissingPermissions):
            logging.info(f"BotMissingPermissions handler ran - {error.missing_perms}\n----------")
            return await ctx.send(f"Bot missing the following permissions: {error.missing_perms}")

        elif isinstance(error, commands.NotOwner):
            logging.info("NotOwner handler ran\n----------")
            return await ctx.send("This is an owner only command.", delete_after=20)

        elif isinstance(error, commands.CommandOnCooldown):
            logging.info("CommandOnCooldown handler ran\n----------")
            return await ctx.send(f"Command on cooldown, ``{math.ceil(error.retry_after)} seconds``", delete_after=int(math.ceil(error.retry_after)))

        elif isinstance(error, commands.MissingRequiredArgument):
            logging.info("MissingRequiredArgument handler ran\n----------")
            # \n``Missing: {error.param.name}``")
            return await ctx.send(f"You didn't give a required argument.", delete_after=20)

        elif isinstance(error, commands.CheckFailure) or isinstance(error, commands.MissingPermissions):
            logging.info("MissingPermissions handler ran\n----------")
            return await ctx.send("You don't have the permissions for this command.", delete_after=20)
        logging.error(f"{error}\n----------")


def setup(bot):
    bot.add_cog(error_handler(bot))
