#this cog is a mess
import logging
from io import io
import aiohttp
import json

from discord import discord
from random import choice, randint

from discord.ext import commands

async def image(link):
    logging.info(f"image function ran with {link}")
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            json_data = json.loads(await resp.text())
            async with session.get(json_data["url"]) as resp:
                return io.BytesIO(await resp.read())

class Fun(commands.Cog):
    "Fun Commands for doing funnies"
    def __init__(self, bot):
        self.bot = bot
        self.colours = ["🟥","🟩","🟪","🟧","🟨","🟫","🔳"]

    @commands.command(help="<:amogus:826403430905937941>") # Need to check this emote will actually appear in the help embed (he never checked)
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
    @commands.group(invoke_without_command=True, help="Posts a kawaii neko")
    async def neko(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/neko"), "neko.png")) #also vital

    @commands.cooldown(1, 2, commands.BucketType.user)
    @neko.command(help="Posts a kawaii neko gif")
    async def gif(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/ngif"), "neko.gif")) #def vital, without the bot wont run correctly

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii fox girl")
    async def fox(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/fox_girl"), "fox.png")) #also vital please believe me thanks

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.group(invoke_without_command=True, help="Posts some kawaii feet")
    @commands.is_nsfw()
    async def feet(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/feet"), "feet.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts some kawaii yuri action")
    @commands.is_nsfw()
    async def yuri(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/yuri"), "yuri.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii futanari")
    @commands.is_nsfw()
    async def futa(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/futanari"), "futa.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii lewd kemonomimi")
    @commands.is_nsfw()
    async def lewdkemo(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/lewdkemo"), "lewdkemo.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @feet.command(aliases=["gif"], help="Posts a kawaii feet gif")
    @commands.is_nsfw()
    async def feet_gif(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/feetg"), "feet.gif"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.group(invoke_without_command=True, help="Posts some kawaii cumming")
    @commands.is_nsfw()
    async def cum(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/cum"), "cum.gif"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts some kawaii lewd kemonomimi")
    @commands.is_nsfw()
    async def erokemo(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/erokemo"), "erokemo.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="I have no idea what this posts exactly, just try it, it's probably pretty kawaii")
    @commands.is_nsfw()
    async def les(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/les"), "les.gif"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii lewd fox girl")
    @commands.is_nsfw()
    async def lewdfox(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/lewdk"), "lewdk.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts some kawaii lewd yuri action")
    @commands.is_nsfw()
    async def eroyuri(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/eroyuri"), "eroyuri.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts some kawaii lewd neko")
    @commands.is_nsfw()
    async def eron(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/eron"), "eron.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @cum.command(aliases=["jpg"], help="Posts a kawaii yummy cummy gif") #haha cum funny
    @commands.is_nsfw()
    async def cum_jpg(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/cum_jpg"), "cum.jpg"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii blowjob gif")
    @commands.is_nsfw()
    async def bj(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/bj"), "bj.gif"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii solo girl")
    @commands.is_nsfw()
    async def solo(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/solo"), "solo.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii kemonomimi")
    async def kemo(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/kemonomimi"), "kemonomimi.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii lewd avatar for your use, if you want")
    @commands.is_nsfw()
    async def nsfw_avatar(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/nsfw_avatar"), "nsfw_avatar.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii anal gif")
    @commands.is_nsfw()
    async def anal(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/anal"), "anal.gif"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii lewd image")
    @commands.is_nsfw()
    async def hentai(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/hentai"), "hentai.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts some kawaii lewd feet")
    @commands.is_nsfw()
    async def erofeet(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/erofeet"), "erofeet.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii artwork by ke-ta")
    @commands.is_nsfw()
    async def keta(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/keta"), "keta.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii blowjob image")
    @commands.is_nsfw()
    async def blowjob(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/blowjob"), "blowjob.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.group(invoke_without_command=True, help="Posts a kawaii gif of some pussy")
    @commands.is_nsfw()
    async def pussy(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/pussy"), "pussy.gif"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts some kawaii booba")
    @commands.is_nsfw()
    async def booba(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/tits"), "tits.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a truly kawaii lizard")
    async def lizard(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/lizard"), "lizard.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @pussy.command(aliases=["jpg"], help="Posts a kawaii image of some pussy")
    @commands.is_nsfw()
    async def pussy_jpg(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/pussy_jpg"), "pussy.jpg"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="I have no idea what this posts")
    @commands.is_nsfw()
    async def pwankg(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/pwankg"), "pwankg.gif"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="I have no idea what this posts either")
    @commands.is_nsfw()
    async def classic(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/classic"), "classic.gif"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="No idea, just try")
    @commands.is_nsfw()
    async def kuni(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/kuni"), "kuni.gif"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts some kawaii femdom")
    @commands.is_nsfw()
    async def femdom(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/femdom"), "femdom.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts some kawaii lewd kitsune")
    @commands.is_nsfw()
    async def ero_kitsune(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/erok"), "erok.png")) 

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii lewd fox girl")
    @commands.is_nsfw()
    async def fox_girl(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/fox_girl"), "fox_girl.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="More booba")
    @commands.is_nsfw()
    async def boobs(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/boobs"), "boobs.gif"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="what")
    @commands.is_nsfw()
    async def ero(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/ero"), "ero.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii smug gif")
    async def smug(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/smug"), "smug.gif"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a truly kawaii goose")
    async def goose(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/goose"), "goose.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Posts a kawaii lewd trap")
    @commands.is_nsfw()
    async def trap(self, ctx):
        await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/trap"), "trap.png"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @neko.group(invoke_without_command=True, help="Posts a kawaii lewd neko")
    @commands.is_nsfw()
    async def lewd(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/lewd"), "neko_lewd.png")) #equally as vital

    @commands.cooldown(1, 2, commands.BucketType.user)
    @lewd.command(aliases=["gif"], help="Posts a kawaii lewd neko gif")
    @commands.is_nsfw()
    async def lewd_gif(self, ctx):
            await ctx.send(file=discord.File(await image("https://nekos.life/api/v2/img/nsfw_neko_gif"), "neko_lewd_gif.gif")) #this too


def setup(bot):
    bot.add_cog(Fun(bot))