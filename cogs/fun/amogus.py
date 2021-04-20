# When the cog is sus!
# ⠀⠀⠀⡯⡯⡾⠝⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢊⠘⡮⣣⠪⠢⡑⡌
# ⠀⠀⠀⠟⠝⠈⠀⠀⠀⠡⠀⠠⢈⠠⢐⢠⢂⢔⣐⢄⡂⢔⠀⡁⢉⠸⢨⢑⠕⡌
# ⠀⠀⡀⠁⠀⠀⠀⡀⢂⠡⠈⡔⣕⢮⣳⢯⣿⣻⣟⣯⣯⢷⣫⣆⡂⠀⠀⢐⠑⡌
# ⢀⠠⠐⠈⠀⢀⢂⠢⡂⠕⡁⣝⢮⣳⢽⡽⣾⣻⣿⣯⡯⣟⣞⢾⢜⢆⠀⡀⠀⠪
# ⣬⠂⠀⠀⢀⢂⢪⠨⢂⠥⣺⡪⣗⢗⣽⢽⡯⣿⣽⣷⢿⡽⡾⡽⣝⢎⠀⠀⠀⢡
# ⣿⠀⠀⠀⢂⠢⢂⢥⢱⡹⣪⢞⡵⣻⡪⡯⡯⣟⡾⣿⣻⡽⣯⡻⣪⠧⠑⠀⠁⢐
# ⣿⠀⠀⠀⠢⢑⠠⠑⠕⡝⡎⡗⡝⡎⣞⢽⡹⣕⢯⢻⠹⡹⢚⠝⡷⡽⡨⠀⠀⢔
# ⣿⡯⠀⢈⠈⢄⠂⠂⠐⠀⠌⠠⢑⠱⡱⡱⡑⢔⠁⠀⡀⠐⠐⠐⡡⡹⣪⠀⠀⢘
# ⣿⣽⠀⡀⡊⠀⠐⠨⠈⡁⠂⢈⠠⡱⡽⣷⡑⠁⠠⠑⠀⢉⢇⣤⢘⣪⢽⠀⢌⢎
# ⣿⢾⠀⢌⠌⠀⡁⠢⠂⠐⡀⠀⢀⢳⢽⣽⡺⣨⢄⣑⢉⢃⢭⡲⣕⡭⣹⠠⢐⢗
# ⣿⡗⠀⠢⠡⡱⡸⣔⢵⢱⢸⠈⠀⡪⣳⣳⢹⢜⡵⣱⢱⡱⣳⡹⣵⣻⢔⢅⢬⡷
# ⣷⡇⡂⠡⡑⢕⢕⠕⡑⠡⢂⢊⢐⢕⡝⡮⡧⡳⣝⢴⡐⣁⠃⡫⡒⣕⢏⡮⣷⡟
# ⣷⣻⣅⠑⢌⠢⠁⢐⠠⠑⡐⠐⠌⡪⠮⡫⠪⡪⡪⣺⢸⠰⠡⠠⠐⢱⠨⡪⡪⡰
# ⣯⢷⣟⣇⡂⡂⡌⡀⠀⠁⡂⠅⠂⠀⡑⡄⢇⠇⢝⡨⡠⡁⢐⠠⢀⢪⡐⡜⡪⡊
# ⣿⢽⡾⢹⡄⠕⡅⢇⠂⠑⣴⡬⣬⣬⣆⢮⣦⣷⣵⣷⡗⢃⢮⠱⡸⢰⢱⢸⢨⢌
# ⣯⢯⣟⠸⣳⡅⠜⠔⡌⡐⠈⠻⠟⣿⢿⣿⣿⠿⡻⣃⠢⣱⡳⡱⡩⢢⠣⡃⠢⠁
# ⡯⣟⣞⡇⡿⣽⡪⡘⡰⠨⢐⢀⠢⢢⢄⢤⣰⠼⡾⢕⢕⡵⣝⠎⢌⢪⠪⡘⡌⠀
# ⡯⣳⠯⠚⢊⠡⡂⢂⠨⠊⠔⡑⠬⡸⣘⢬⢪⣪⡺⡼⣕⢯⢞⢕⢝⠎⢻⢼⣀⠀
# ⠁⡂⠔⡁⡢⠣⢀⠢⠀⠅⠱⡐⡱⡘⡔⡕⡕⣲⡹⣎⡮⡏⡑⢜⢼⡱⢩⣗⣯⣟
# ⢀⢂⢑⠀⡂⡃⠅⠊⢄⢑⠠⠑⢕⢕⢝⢮⢺⢕⢟⢮⢊⢢⢱⢄⠃⣇⣞⢞⣞⢾
# ⢀⠢⡑⡀⢂⢊⠠⠁⡂⡐⠀⠅⡈⠪⠪⠪⠣⠫⠑⡁⢔⠕⣜⣜⢦⡰⡎⡯⡾⡽


import discord
import logging
from discord.ext import commands
from random import choice
from random import randint


colours = ["🟥","🟩","🟪","🟧","🟨","🟫","🆒"]


class amogus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def amogus(self, ctx):
        logging.info(f"Recieved amogus in {ctx.guild.name}")
        square_colour = choice(colours)
        if randint(0,10) == 10:
            await ctx.send(f"""⬛{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}
⬛{square_colour}<:sus_glass_1:826440778095394866><:sus_glass_2:826440778297507840><:sus_glass_3:826440778091331614><:sus_glass_4:826440778012295177><:sus_glass_5:826440778242457650>
{square_colour}{square_colour}<:sus_glass_6:826440777797468181><:sus_glass_7:826440778196320298><:sus_glass_8:826440778220961802><:sus_glass_9:826440777834954794><:sus_glass_10:826440778040475679>
{square_colour}{square_colour}<:sus_glass_11:826440778158702602><:sus_glass_12:826440778254516235><:sus_glass_13:826440778376020008><:sus_glass_14:826440778351640576><:sus_glass_15:826440778292396072>
{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}
{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}
⬛{square_colour}{square_colour}⬛⬛{square_colour}{square_colour}
⬛{square_colour}{square_colour}⬛⬛{square_colour}{square_colour}""")
            logging.info("Sussy amogus sent.")
        else:
            await ctx.send(f"""⬛{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}
⬛{square_colour}🟦🟦⬜⬜⬜
{square_colour}{square_colour}🟦🟦🟦⬜⬜
{square_colour}{square_colour}🟦🟦🟦🟦🟦
{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}
{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}{square_colour}
⬛{square_colour}{square_colour}⬛⬛{square_colour}{square_colour}
⬛{square_colour}{square_colour}⬛⬛{square_colour}{square_colour}""")
            logging.info("Amogus sent.")


def setup(bot):
    bot.add_cog(amogus(bot))

# this single py file should put me on a suicide watch list