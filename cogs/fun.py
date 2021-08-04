import logging
from io import BytesIO
from json import loads

from discord import File, HTTPException
from random import choice, randint

from discord.ext import commands
from os.path import splitext


class Fun(commands.Cog):
    "Fun Commands for doing funnies"
    def __init__(self, bot):
        self.bot = bot
        self.colours = ["🟥","🟩","🟪","🟧","🟨","🟫","🔳"]

    @commands.command(help="<:amogus:826403430905937941>") # Need to check this emote will actually appear in the help embed
    async def amogus(self, ctx):
        square_colour = choice(self.colours)
        if randint(0,10) == 10:
            await ctx.send(f"""⬛{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}
⬛{square_colour}<:sus_glass_1:826440778095394866><:sus_glass_2:826440778297507840><:sus_glass_3:826440778091331614><:sus_glass_4:826440778012295177><:sus_glass_5:826440778242457650>
{square_colour}{square_colour}<:sus_glass_6:826440777797468181><:sus_glass_7:826440778196320298><:sus_glass_8:826440778220961802><:sus_glass_9:826440777834954794><:sus_glass_10:826440778040475679>
{square_colour}{square_colour}<:sus_glass_11:826440778158702602><:sus_glass_12:826440778254516235><:sus_glass_13:826440778376020008><:sus_glass_14:826440778351640576><:sus_glass_15:826440778292396072>
{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}
{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}
⬛{square_colour}{square_colour}⬛⬛{square_colour}{square_colour}
⬛{square_colour}{square_colour}⬛⬛{square_colour}{square_colour}""")
        else:
            await ctx.send(f"""⬛{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}
⬛{square_colour}🟦🟦⬜⬜⬜
{square_colour}{square_colour}🟦🟦🟦⬜⬜
{square_colour}{square_colour}🟦🟦🟦🟦🟦
{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}
{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}
⬛{square_colour}{square_colour}⬛⬛{square_colour}{square_colour}
⬛{square_colour}{square_colour}⬛⬛{square_colour}{square_colour}""")

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(aliases=["nya"], help="Posts a kawaii neko")
    async def neko(self, ctx):
        async with ctx.channel.typing():
            async with self.bot.session.get("https://nekos.life/api/v2/img/neko") as resp:
                url = loads(await resp.text())["url"]
                logging.info(url)
            async with self.bot.session.get(url) as resp:
                root, ext = splitext(url)
                try:
                    await ctx.reply(file=File(BytesIO(await resp.read()), f"kawaii_neko{ext}"))
                except HTTPException:
                    await ctx.reply(url)


def setup(bot):
    bot.add_cog(Fun(bot))