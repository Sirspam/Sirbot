import discord
import logging
from discord.ext import commands
from firebase_admin import firestore
from utils import prefixes


dab = firestore.client()


class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(case_insensitive=True, aliases=["invite"])
    async def links(self, ctx):
        logging.info(f"Recieved link in {ctx.guild.name}")
        embed = discord.Embed(
            description="""
            [Bot Invite Link](https://discord.com/api/oauth2/authorize?client_id=822029618969182218&permissions=313408&scope=bot) | 
            [Bot's Home Server](https://discord.gg/dWX6fpGUK9) | [Github Repo](https://github.com/sirspam/Sirbot)\n\n\n
            this text is just filler for the thumbnail\n
            I hope you're having a good day :)\n""",
            color=0x00A9E0)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/822087750798016552.gif?v=1")
        await ctx.reply(embed=embed)
        logging.info(f'Link embed sent')

    @commands.command(case_insensitive=True)
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def set_prefix(self, ctx, *, arg):
        logging.info(f"Recieved set_prefix {arg} in {ctx.guild.name}")
        if arg[:1]!='"' or arg[-1:]!='"':
            raise commands.BadArgument
        if arg == '">"':
            col_ref = dab.collection("prefixes").document('collectionlist').get().get('array')
            col_ref.remove(str(ctx.guild.id))
            dab.collection("prefixes").document('collectionlist').update({'array': col_ref})
            dab.collection("prefixes").document(str(ctx.guild.id)).delete()
            await ctx.reply("Prefix successfully set to ``>``!")
            await prefixes.prefix_delete(ctx.guild.id)
            logging.info("Deleted from database (default value)")
            return
        col_ref = dab.collection("prefixes").document("collectionlist").get().get("array")
        if str(ctx.guild.id) not in col_ref:
            col_ref.append(str(ctx.guild.id))
            col_ref.sort()
            dab.collection("prefixes").document("collectionlist").update({"array": col_ref})
        doc_ref = dab.collection("prefixes").document(str(ctx.guild.id))
        arg=arg[1:]
        arg=arg[:-1]
        doc_ref.set({
            "prefix": arg
        })
        await ctx.reply(f"Prefix successfully set to ``{arg}``!")
        logging.info("Prefix successfully set")
        await prefixes.cache_prefixes()


def setup(bot):
    bot.add_cog(Text(bot))
