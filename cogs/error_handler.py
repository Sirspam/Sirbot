import math
from discord.ext import commands
from utils import logger


class error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await logger.log_info(self, f"on_command_error triggered")
        if isinstance(error, commands.BadArgument):
            await logger.log_info(self, "BadArgument handler ran\n----------")
            return await ctx.send("You've given a bad argument")

        elif isinstance(error, commands.CommandNotFound):
            await logger.log_info(self, "CommandNotFound handler ran\n----------")
            return await ctx.send("Command not found", delete_after=20)

        elif isinstance(error, commands.BotMissingPermissions):
            await logger.log_info(self, f"BotMissingPermissions handler ran - {error.missing_perms[0]}\n----------")
            return await ctx.send(f"Bot missing the following permissions: {error.missing_perms[0]}")

        elif isinstance(error, commands.NotOwner):
            await logger.log_info(self, "NotOwner handler ran\n----------")
            return await ctx.send('Owner only command')

        elif isinstance(error, commands.CommandOnCooldown):
            await logger.log_info(self, "CommandOnCooldown handler ran\n----------")
            return await ctx.send(f"Command on cooldown, ``{math.ceil(error.retry_after)} seconds``")

        elif isinstance(error, commands.MissingRequiredArgument):
            await logger.log_info(self, "MissingRequiredArgument handler ran\n----------")
            # \n``Missing: {error.param.name}``")
            return await ctx.send(f"You didn't give a required argument.")

        elif isinstance(error, commands.CheckFailure) or isinstance(error, commands.MissingPermissions):
            await logger.log_info(self, "MissingPermissions handler ran\n----------")
            return await ctx.send("You don't have the permissions for this command.")
        await logger.log_info(self, f"{error}\n----------")


def setup(bot):
    bot.add_cog(error_handler(bot))
