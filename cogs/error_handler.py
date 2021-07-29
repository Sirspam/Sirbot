import logging
from math import ceil
from asyncio import sleep

from discord import Embed, Colour

from discord.ext import commands

def ErrorEmbed(title: str, description: str) -> Embed:
    return Embed(
        title=title,
        description=description,
        colour=Colour.red()
    )

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        logging.info(f"ErrorHandler invoked")
        
        if hasattr(ctx.command, "on_error"):
            return
        
        if isinstance(error, commands.BadArgument):
            logging.info("BadArgument handler ran")
            return await ctx.reply(embed=ErrorEmbed("Bad Argument",f"Check ``{ctx.prefix}help`` for what arguments you need to give"))

        if isinstance(error, commands.BotMissingPermissions):
            logging.info(f"BotMissingPermissions handler ran - {error.missing_perms}")
            return await ctx.reply(embed=ErrorEmbed("Bot Missing Permissions",error.missing_perms))

        if isinstance(error, commands.CommandOnCooldown):
            logging.info("CommandOnCooldown handler ran")
            message = await ctx.reply(embed=ErrorEmbed("Command on Cooldown",f"{ceil(error.retry_after)} seconds"))
            await sleep(int(ceil(error.retry_after)))
            return await message.edit(embed=Embed(
                title="Cooldown Finished",
                colour=Colour.green()
            ))

        if isinstance(error, commands.MissingRequiredArgument):
            logging.info(f"MissingRequiredArgument handler ran. Missing: {error.param.name}")
            return await ctx.reply(embed=ErrorEmbed("Missing Required Arguments",error.param.name))

        if isinstance(error, commands.MissingPermissions):
            logging.info("MissingPermissions handler ran")
            return await ctx.reply(embed=ErrorEmbed("Missing Permissions","You don't have the permissions for this command"))

        if isinstance(error, commands.NSFWChannelRequired):
            logging.info("NSFWChannelRequired hander ran")
            return await ctx.reply("How lewd of you <:AYAYAFlushed:822094723199008799>\n``This command can only be ran in an nsfw channel``")

        logging.error(error)
        github_issue_url = ""
        if self.bot.github_repo:
            github_issue_url = f"open an [issue report]({self.bot.github_repo}/issues) or"
        await ctx.send(embed=Embed(
            title="Uh oh. An unhandled error occured ☹️",
            description=f"If this keeps occuring {github_issue_url} go pester {self.bot.get_user(self.bot.owner_id).name}\n\n```{error}```",
            colour=Colour.red()
        ))
        if self.bot.logging_channel_id:
            return await self.bot.get_channel(self.bot.logging_channel_id).send(embed=Embed(
                title=f"{ctx.command} in {ctx.guild.name}",
                description=
                f"""**Guild ID**```{ctx.guild.id}```
                **Author ID**```{ctx.author.id}```
                **Message Content**```{ctx.message.content}```
                **Error**```{error}```""",
                colour=Colour.red()
            ))


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
