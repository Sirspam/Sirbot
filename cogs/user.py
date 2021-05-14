from json.decoder import JSONDecodeError
import discord
import asyncio
import re
import json
import logging
from discord.ext import commands
from discord.utils import get
from firebase_admin import firestore

dab = firestore.client()


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["u"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def user(self, ctx, argument: discord.Member = None):
        if argument is not None:
            ctx.author = argument
        logging.info(f"Recieved user {ctx.author.id} in {ctx.guild.name}")
        ref = dab.collection("users").document(str(ctx.author.id)).get()
        if ref.exists is False:
            logging.info(f"User not found")
            if argument is None:
                return await ctx.reply(f"You're not in my database\nUse ``{ctx.prefix} user add`` to get started!")
            elif argument is not None:
                return await ctx.reply("That person isn't in my database")
        username = ref.get("username")
        scoresaber = ref.get("scoresaber")
        links_Message = f"[Scoresaber]({scoresaber}) "
        try:
            steam = ref.get("steam")
            links_Message = links_Message + f"| [Steam]({steam}) "
        except BaseException:
            True
        try:
            twitch = ref.get("twitch")
            links_Message = links_Message + f"| [Twitch]({twitch}) "
        except BaseException:
            True
        try:
            youtube = ref.get("youtube")
            links_Message = links_Message + f"| [Youtube]({youtube}) "
        except BaseException:
            True
        try:
            twitter = ref.get("twitter")
            links_Message = links_Message + f"| [Twitter]({twitter}) "
        except BaseException:
            True
        try:
            reddit = ref.get("reddit")
            links_Message = links_Message + f"| [Reddit]({reddit}) "
        except BaseException:
            True
        try:
            hmd = ref.get("hmd")
        except BaseException:
            hmd = None
        try:
            birthday = ref.get("birthday")
        except BaseException:
            birthday = None
        try:
            pfp = ref.get("pfp")
        except BaseException:
            pfp = None
        try:
            status = ref.get("status")
        except BaseException:
            status = None
        # try:
        #   this on for size, Mister
        try:
            colour = await commands.ColourConverter().convert(ctx, "0x"+ref.get("colour"))
            embed = discord.Embed(title=username, colour=colour)
        except BaseException:
            embed = discord.Embed(
                title=username,
                colour=discord.Colour.random())
        embed.add_field(name="Links", value=links_Message, inline=False)
        if hmd is not None:
            embed.add_field(name="HMD", value=hmd, inline=True)
        if birthday is not None:
            embed.add_field(name="Birthday", value=birthday, inline=True)
        if status is not None:
            embed.add_field(name="Status", value=status, inline=False)
        if pfp is not None:
            embed.set_thumbnail(url=pfp)
        else:
            embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
        logging.info('Response: user embed')


    @user.command(case_insensitive=True, aliases=["link"])
    async def add(self, ctx, argument=None):
        logging.info(f"Recieved user add {ctx.author.id} in {ctx.guild.name}")
        col_ref = dab.collection('users').document('collectionlist').get().get('array')
        if str(ctx.author.id) in col_ref:
            return await ctx.reply("You're already in the database!\nUse ``>user update`` instead")
        elif argument is None:
            sent = await ctx.reply('What is your scoresaber link?')
            try:
                msg = await self.bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                scoresaber = msg.content
            except asyncio.TimeoutError:
                await sent.delete()
                return await ctx.reply("You didn't reply in time, please restart the process")
        elif argument is not None:
            scoresaber = argument
        if scoresaber.isdigit():
            scoresaber = "https://scoresaber.com/u/"+scoresaber
        else:
            scoresaber = scoresaber.split("?", 1)[0]
            scoresaber = scoresaber.split("&", 1)[0]
        try:
            async with self.bot.session.get(f"https://new.scoresaber.com/api/player/{scoresaber[25:]}/full") as resp:
                json_data = json.loads(await resp.text())
        except JSONDecodeError:
            logging.info("JSONDecodeError raised. ScoreSaber API likely dead")
            return await ctx.reply("ScoreSaber returned an invalid json object, meaning the API is probably dead")
        if "error" in json_data:
            await ctx.reply("That scoresaber link seems to be invalid!\nPlease try again and use a valid link!")
            return
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.set({
            'username': ctx.author.name,
            'scoresaber': scoresaber,
        })
        try:
            col_ref.append(str(ctx.author.id))
            col_ref.sort()
            dab.collection('users').document('collectionlist').update({'array': col_ref})
        except Exception as e:
            return logging.info(e+"")
        await ctx.reply(f'{ctx.author.name} has sucessfully been added to the database!\nUse ``>user update`` to add optional customisation')
        logging.info(f'Response: {ctx.author.name} has sucessfully been added to the database')
    
    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member):
        return 
        # Need to make this work accross multiple servers


    @user.group(invoke_without_command=True, case_insensitive=True)
    async def remove(self, ctx, argument=None):
        logging.info(f"Recieved user remove {ctx.author.id} in {ctx.guild.name}")
        if argument is None:
            try:
                col_ref = dab.collection('users').document('collectionlist').get().get('array')
                col_ref.remove(str(ctx.author.id))
                dab.collection('users').document('collectionlist').update({'array': col_ref})
                dab.collection("users").document(str(ctx.author.id)).delete()
                await ctx.reply(f"{ctx.author.name} has been successfully removed from the database")
                logging.info(f"Response: {ctx.author.id} has been successfully removed to the database")
            except Exception as e:
                logging.error(e+"")
        elif argument is not None:
            if argument.lower() in ["username", "steam", "twitch", "youtube", "twitter", "reddit", "birthday", "pfp", "hmd", "status", "colour", "color"]:
                if argument.lower() == "username":
                    logging.info("Escalated to user remove username")
                    dab.collection("users").document(str(ctx.author.id)).update({
                        "username": ctx.author.name
                    })
                    await ctx.reply("I've removed your username")
                    logging.info(f"{ctx.author.name} has removed their username")
                else:
                    if argument.lower() == "color":
                        argument == "colour"
                    logging.info(f"Escalated to user remove {argument.lower()}")
                    doc_ref = dab.collection("users").document(str(ctx.author.id))
                    doc_ref.update({
                        argument.lower(): firestore.DELETE_FIELD
                    })
                    await ctx.reply(f"I've removed your {argument.lower()}")
                    logging.info(f"{ctx.author.name} has removed their {argument.lower()}")
            else:
                raise commands.BadArgument

    
    @user.group(invoke_without_command=True, case_insensitive=True)
    async def update(self, ctx):
        logging.info(f"Recieved user update")
        await ctx.reply(f"You need to state what you want to update!\nUse ``{ctx.prefix}help update`` to check the valid arguments")
        logging.info("no sub command given")

    @update.command(case_insensitive=True)
    async def username(self, ctx, *, argument):
        logging.info(f"Recieved user update username {ctx.author.id} in {ctx.guild.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({'username': argument})
        await ctx.reply(f"I've updated your username to {argument}!")
        logging.info(f"{ctx.author.name} has updated their username to {argument}")

    @update.command(case_insensitive=True)
    async def scoresaber(self, ctx, argument):
        logging.info(f"Recieved user update scoresaber {ctx.author.id} in {ctx.guild.name}")
        if argument.isdigit():
            argument = "https://scoresaber.com/u/"+argument
        else:
            argument = argument.split("?", 1)[0]
            argument = argument.split("&", 1)[0]
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'scoresaber': argument})
        await ctx.reply("I've updated your Scoresaber")
        logging.info(f"{ctx.author.name} has updated their scoresaber to {argument}")

    @update.command(case_insensitive=True)
    async def steam(self, ctx, argument):
        logging.info(f"Recieved user update steam {ctx.author.id} in {ctx.guild.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'steam': argument})
        await ctx.reply("I've updated your Steam")
        logging.info(f"{ctx.author.name} has updated their steam to {argument}")

    @update.command(case_insensitive=True)
    async def twitch(self, ctx, argument):
        logging.info(f"Recieved user update twitch {ctx.author.id} in {ctx.guild.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'twitch': argument})
        await ctx.reply("I've updated your Twitch")
        logging.info(f"{ctx.author.name} has updated their twitch to {argument}")

    @update.command(case_insensitive=True)
    async def youtube(self, ctx, argument):
        logging.info(f"Recieved user update youtube {ctx.author.id} in {ctx.guild.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'youtube': argument})
        await ctx.reply("I've updated your Youtube")
        logging.info(f"{ctx.author.name} has updated their youtube to {argument}")

    @update.command(case_insensitive=True)
    async def twitter(self, ctx, argument):
        logging.info(f"Recieved user update twitter {ctx.author.id} in {ctx.guild.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'twitter': argument})
        await ctx.reply("I've updated your Twitter")
        logging.info(f"{ctx.author.name} has updated their twitter to {argument}")

    @update.command(case_insensitive=True)
    async def reddit(self, ctx, argument):
        logging.info(f"Recieved user update reddit {ctx.author.id} in {ctx.guild.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'reddit': argument})
        await ctx.reply("I've updated your Reddit")
        logging.info(f"{ctx.author.name} has updated their reddit to {argument}")

    @update.command(case_insensitive=True)
    async def birthday(self, ctx, argument):
        logging.info(f"Recieved user update birthday {ctx.author.id} in {ctx.guild.name}")
        if ((bool(re.search(r"\d/", argument)))) is False:
            logging.info("Birthday input validation triggered")
            await ctx.reply("Oopsie, looks like you did a woopsie! uwu\n``Don't use characters expect for numbers and /``")
            return
        storer = argument.split('/')
        storer[0] = int(storer[0])
        storer[1] = int(storer[1])
        if(storer[1] > 12 or storer[1] < 1 or storer[0] > 31 or storer[0] < 1):
            logging.info("Birthday legitimacy triggered, date and/or month invalid")
            return await ctx.reply("That date doesn't make any sense!\n``Please use a legitimate date``")
        try: 
            print(int(len(storer[2])))
            if int(len(storer[2])) > 4 or int(len(storer[2])) < 4:
                logging.info("Birthday legitmacy triggered, year invalid")
                return await ctx.reply("That date doesn't make any sense!\n``Please use a legitimate year, or don't include one``")
        except IndexError:
            False
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'birthday': argument})
        await ctx.reply(f"I've updated your birthday to {argument}!")
        logging.info(f"{ctx.author.name} has updated their birthday to {argument}")

    @update.command(case_insensitive=True)
    async def hmd(self, ctx, *, argument):
        logging.info(f"Recieved user update hmd {ctx.author.id} in {ctx.guild.name}")
        valid_HMD_low = [x.lower() for x in self.bot.valid_HMD]
        try:
            pos = valid_HMD_low.index(argument.lower()) 
        except:
            logging.info(f"{argument} not in valid_HMD")
            return await ctx.reply(f"That HMD isn't valid!\n``Use {ctx.prefix}help update to check the valid HMDs``")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'hmd': self.bot.valid_HMD[pos]})
        await ctx.reply(f"I've updated your HMD to {self.bot.valid_HMD[pos]}!")
        logging.info(f"{ctx.author.name} has updated their status to {self.bot.valid_HMD[pos]}")

    @update.command(case_insensitive=True)
    async def pfp(self, ctx, argument):
        logging.info(f"Recieved user update pfp {ctx.author.id} in {ctx.guild.name}")
        if argument[:4] != "http":
            logging.info(f"Argument is not a link ({argument})")
            return await ctx.reply("You can only use links for your profile picture!")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'pfp': argument})
        await ctx.reply("I've updated your pfp")
        logging.info(f"{ctx.author.name} has updated their pfp to {argument}")

    @update.command(case_insensitive=True)
    async def status(self, ctx, *, argument):
        logging.info(f"Recieved user update status {ctx.author.id} in {ctx.guild.name}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'status': argument})
        await ctx.reply("I've updated your status")
        logging.info(f"{ctx.author.name} has updated their status to {argument}")

    @update.command(case_insensitive=True, aliases=["color"])  # Americans ew
    async def colour(self, ctx, argument):
        logging.info(f"Recieved user update colour {ctx.author.id} in {ctx.guild.name}")
        try:
            await commands.ColourConverter().convert(ctx, "0x"+argument)
        except Exception as e:
            await ctx.reply("Please use a valid hexadecimal colour value. uwu")
            return logging.info(f"expect triggered: {e}")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.update({
            'colour': argument})
        await ctx.reply("I've updated your colour")
        logging.info(f"{ctx.author.name} has updated their colour to {argument}")


def setup(bot):
    bot.add_cog(User(bot))
