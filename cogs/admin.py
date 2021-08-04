import logging

from firebase_admin import firestore

from utils import prefixes
from discord.ext import commands


dab = firestore.client()


class Admin(commands.Cog):
    "Administrator only Commands"
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help="Changes the bot's default prefix for this server")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def set_prefix(self, ctx, *, arg):
        if arg[:1]!='"' or arg[-1:]!='"':
            raise commands.BadArgument
        if arg == f'"{self.bot.default_prefix}"':
            col_ref = dab.collection("prefixes").document('collectionlist').get().get('array')
            col_ref.remove(str(ctx.guild.id))
            dab.collection("prefixes").document('collectionlist').update({'array': col_ref})
            dab.collection("prefixes").document(str(ctx.guild.id)).delete()
            await ctx.reply(f"Prefix successfully set to ``{self.bot.default_prefix}``!")
            await prefixes.prefix_delete(ctx.guild.id)
            logging.info("Deleted from database (default value)")
            return
        col_ref = dab.collection("prefixes").document("collectionlist").get().get("array")
        if str(ctx.guild.id) not in col_ref:
            col_ref.append(str(ctx.guild.id))
            col_ref.sort()
            dab.collection("prefixes").document("collectionlist").update({"array": col_ref})
        doc_ref = dab.collection("prefixes").document(str(ctx.guild.id))
        arg=arg[1:][:-1]
        doc_ref.set({
            "prefix": arg
        })
        await ctx.reply(f"Prefix successfully set to ``{arg}``!")
        await prefixes.cache_prefixes()


def setup(bot):
    bot.add_cog(Admin(bot))
