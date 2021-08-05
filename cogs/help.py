from contextlib import suppress

from discord import Embed, Colour

from discord.ext import commands
from utils.prefixes import get_prefix


class HelpEmbed(Embed):
    def __init__(self, ctx, **kwargs):
        super().__init__(**kwargs)
        self.set_footer(text=f"Use {ctx.prefix}help [command] or {ctx.prefix}help [category] for more information")
        if ctx.bot.github_repo:
            self.set_author(name=f"{ctx.me.display_name} Help", icon_url=ctx.me.avatar_url, url=ctx.bot.github_repo)
        else:
            self.set_author(name=f"{ctx.me.display_name} Help", icon_url=ctx.me.avatar_url)
        self.colour = Colour.blue()

class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "help": "Help Command",
                "aliases": ["commands"],
                "hidden": True
            }
        )

    async def send_bot_help(self, mapping):
        """triggers when `<prefix>help` is called"""
        self.context.prefix = await get_prefix(self.context)
        if self.context.prefix is None:
            self.context.prefix = self.context.bot.default_prefix
        embed = HelpEmbed(self.context, title="Command Categories")
        usable = 0 

        for cog, commands in mapping.items():
            if filtered_commands := await self.filter_commands(commands): 
                amount_commands = len(filtered_commands)
                usable += amount_commands
                if cog:
                    name = cog.qualified_name
                    description = cog.description or "\u200b"
                else:
                    name = "No Category"
                    description = "Commands with no category"
                embed.add_field(name=f"{name} Category", value=description, inline=True)
        embed.description = f"{len(self.context.bot.commands)} commands | {usable} usable" 
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        self.context.prefix = await get_prefix(self.context)
        if self.context.prefix is None:
            self.context.prefix = self.context.bot.default_prefix
        signature = self.get_command_signature(command)
        embed = HelpEmbed(self.context, title=signature, description=command.help or "\u200b")
        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name, inline=True)
        can_run = "No"
        with suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"
        embed.add_field(name="Usable", value=can_run, inline=True)
        if command._buckets and (cooldown := command._buckets._cooldown): # use of internals to get the cooldown of the command
            embed.add_field(name="Cooldown", value=f"{cooldown.per:.0f} seconds", inline=True)
        await self.get_destination().send(embed=embed)

    async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
        self.context.prefix = await get_prefix(self.context)
        if self.context.prefix is None:
            self.context.prefix = self.context.bot.default_prefix
        embed = HelpEmbed(self.context, title=title, description=description or "\u200b")
        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "\u200b", inline=False)
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())

class HelpCog(commands.Cog):
    def __init__(self, bot):
       self.bot = bot
       help_command = HelpCommand()
       help_command.cog = self
       bot.help_command = HelpCommand()


def setup(bot):
    bot.add_cog(HelpCog(bot))