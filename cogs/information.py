from discord import Embed, Permissions

from discord.ext import commands
from discord.utils import oauth_url

class Information(commands.Cog):
    "Informational related commands "
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["invite"], help="Posts links relevant to the bot")
    async def links(self, ctx):
        permission_names = (
            "send_messages",
            "embed_links",
            "attach_files",
            "add_reactions",
            "use_external_emojis"
        )
        perms = Permissions()
        perms.update(**dict.fromkeys(permission_names, True))
        embed = Embed(
            description=
f"""[**Bot Invite Link**]({oauth_url(self.bot.user.id, perms)})
[**Home Server**](https://discord.gg/dWX6fpGUK9)
[**Github Repo**]({self.bot.github_repo})\n
I hope you're having a good day :)""",
            color=0x00A9E0)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/822087750798016552.gif?v=1")
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))