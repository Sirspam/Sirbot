import logging
from math import ceil
from asyncio import sleep, TimeoutError

from discord import Embed, Colour

from discord.ext import commands


class ErrorEmbed(Embed):
    def __init__(self, *kwargs):
        super().__init__()
        self.title = kwargs[0]
        self.description = kwargs[1]
        self.colour = Colour.red()


class CommandErrorHandler(commands.Cog):
    "Handles exceptions raised"
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        logging.info(f"ErrorHandler invoked")
        
        if hasattr(ctx.command, "on_error"):
            return
        
        if isinstance(error, commands.CommandNotFound):
            logging.info("CommandNotFound handler ran")
            await ctx.message.add_reaction("❔")
        
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "❔"
            try:
                await self.bot.wait_for('reaction_add', timeout=10, check=check)
            except TimeoutError:
                return
            else:
                return await ctx.reply(embed=ErrorEmbed(
                    "Command Not Found",
                    f"Use {ctx.prefix}help to check available commands"
                ))

        if isinstance(error, commands.BadArgument):
            logging.info("BadArgument handler ran")
            return await ctx.reply(embed=ErrorEmbed(
                "Bad Argument",
                f"You've given a bad argument for {ctx.command}"
            )) # Response could be better

        if isinstance(error, commands.MissingRequiredArgument):
            logging.info(f"MissingRequiredArgument handler ran")
            return await ctx.reply(embed=ErrorEmbed(
                "Missing Required Arguments",
                f"{ctx.command} requires the {error.param.name} argument\nCheck ``{ctx.prefix}help {ctx.command}`` for more help"
            ))

        if isinstance(error, commands.BotMissingPermissions):
            logging.info(f"BotMissingPermissions handler ran - {error.missing_perms}")
            return await ctx.reply(embed=ErrorEmbed(
                "Bot Missing Permissions"
                ,error.missing_perms
            ))

        if isinstance(error, commands.CommandOnCooldown):
            logging.info("CommandOnCooldown handler ran")
            message = await ctx.reply(embed=ErrorEmbed(
                "Command on Cooldown",
                f"{ceil(error.retry_after)} seconds"
            ))
            await sleep(int(ceil(error.retry_after)))
            return await message.edit(embed=Embed(
                title="Cooldown Finished",
                colour=Colour.green()
            ))

        if isinstance(error, commands.MissingPermissions):
            logging.info("MissingPermissions handler ran")
            return await ctx.reply(embed=ErrorEmbed(
                "Missing Permissions",
                "You don't have the permissions for this command"
            ))

        if isinstance(error, commands.NSFWChannelRequired):
            logging.info("NSFWChannelRequired hander ran")
            return await ctx.reply(embed=ErrorEmbed(
                "How lewd of you 😳",
                f"{ctx.command} can only be ran in an nsfw channel"
            ))
        
        # For unhandled errors
        github_issue_url = ""
        if self.bot.github_repo:
            github_issue_url = f"open an [issue report]({self.bot.github_repo}/issues) or"
        await ctx.send(embed=ErrorEmbed(
            "Uh oh. An unhandled error occured <:NotLikeAqua:822089498866221076>",
            f"If this keeps occuring {github_issue_url} go pester {self.bot.get_user(self.bot.owner_id).mention}\n\n```py\n{error}```",
        ))

        if self.bot.logging_channel_id:
            return await self.bot.get_channel(self.bot.logging_channel_id).send(embed=Embed(
                title=f"Unhandled error raised by ``{ctx.command}``",
                description=
                f"""**Guild ID**```{ctx.guild.id} ({ctx.guild.name})```
                **Author ID**```{ctx.author.id} ({ctx.author.name}#{ctx.author.discriminator})```
                **Message Content**```{ctx.message.content}```
                **Error**```py\n{error}```""",
                colour=Colour.red(),
                url=ctx.message.jump_url
            ))


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
