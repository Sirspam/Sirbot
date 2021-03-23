import discord
import logging
from discord.ext import commands


class text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(case_insensitive=True, aliases=["link"])
    async def links(self, ctx):
        logging.info(f'Recieved link in {ctx.guild.name}')
        embed = discord.Embed(
            description="[Bot Invite Link](https://discord.com/api/oauth2/authorize?client_id=822029618969182218&permissions=313408&scope=bot) | [Bot's Home Server](https://discord.gg/dWX6fpGUK9) | [Github Repo](https://github.com/sirspam/Sirbot)\n\n\nI hope you're having a good day :)\nthis text is just filler for the thumbnail\n",
            color=0x00A9E0)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/822087750798016552.gif?v=1")
        await ctx.send(embed=embed)
        logging.info(f'Link embed sent\n----------')

def setup(bot):
    bot.add_cog(text(bot))
