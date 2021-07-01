import logging
from asyncio import TimeoutError as asyncio_TimeoutError
from re import search
from json import loads, JSONDecodeError

from discord import Embed, Member, Colour
from firebase_admin import firestore

from discord.ext import commands


dab = firestore.client()


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(invoke_without_command=True, aliases=["u"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def user(self, ctx, argument: Member = None):
        if argument is not None:
            ctx.author = argument
        ref = dab.collection("users").document(str(ctx.author.id)).get()
        if ref.exists is False:
            logging.info(f"User not found")
            if argument is None:
                return await ctx.reply(f"You're not in my database\nUse ``{ctx.prefix} user add`` to get started!")
            if argument is not None:
                return await ctx.reply("That person isn't in my database")
        scoresaber = ref.get("scoresaber")
        user_links = ref.get("user_links")
        user_fields = ref.get("user_fields")
        links_message = f"[Scoresaber]({scoresaber}) "
        for field in user_links:
            links_message = f"{links_message}| [{field.capitalize()}]({user_links[field]}) "
        colour = Colour.random()
        if "colour" in user_fields:
            colour = colour = await commands.ColourConverter().convert(ctx, "0x"+user_fields["colour"])
        username = ctx.author.name
        if "username" in user_fields:
            username = user_fields["username"]
        embed = Embed(title=username, colour=colour)
        embed.add_field(name="Links", value=links_message, inline=False)
        # Couldn't for loop this because of the inline :(
        if "hmd" in user_fields:
            embed.add_field(name="HMD", value=user_fields["hmd"], inline=True)
        if "birthday" in user_fields:
            embed.add_field(name="Birthday", value=user_fields["birthday"], inline=True)
        if "status" in user_fields:
            embed.add_field(name="Status", value=user_fields["status"], inline=False)
        if "pfp" in user_fields:
            embed.set_thumbnail(url=user_fields["pfp"])
        else:
            embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)


    @user.command(aliases=["link"])
    async def add(self, ctx, argument=None):
        col_ref = dab.collection('users').document('collectionlist').get().get('array')
        if str(ctx.author.id) in col_ref:
            return await ctx.reply(f"You're already in the database!\nUse ``{ctx.prefix}user update`` instead")
        if argument is None:
            sent = await ctx.reply('What is your scoresaber link?')
            try:
                msg = await self.bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                scoresaber = msg.content
            except asyncio_TimeoutError:
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
                json_data = loads(await resp.text())
        except JSONDecodeError:
            logging.info("JSONDecodeError raised. ScoreSaber API likely dead")
            return await ctx.reply("ScoreSaber returned an invalid json object, meaning the API is probably dead")
        if "error" in json_data:
            await ctx.reply("That scoresaber link seems to be invalid!\nPlease try again and use a valid link!")
            return
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.set({
            "user_fields": dict(),
            "user_links": dict(),
            "scoresaber": scoresaber,
        })
        col_ref.append(str(ctx.author.id))
        col_ref.sort()
        dab.collection('users').document('collectionlist').update({'array': col_ref})
        await ctx.reply(f'{ctx.author.name} has sucessfully been added to the database!\nUse ``{ctx.prefix}user update`` to add optional customisation')
        logging.info(f"Successfully added {ctx.author.name} to the database")
    
    # @commands.Cog.listener("on_member_remove")
    # async def on_member_remove(self, member):
    #     return 
        # Need to make this work accross multiple servers

    @user.group(invoke_without_command=True, case_insensitive=True)
    async def remove(self, ctx):
        col_ref = dab.collection('users').document('collectionlist').get().get('array')
        col_ref.remove(str(ctx.author.id))
        dab.collection('users').document('collectionlist').update({'array': col_ref})
        dab.collection("users").document(str(ctx.author.id)).delete()
        await ctx.reply(f"{ctx.author.name} has been successfully removed from the database")
        logging.info(f"Successfully removed {ctx.author.id} from the database")

    @user.group(invoke_without_command=True, case_insensitive=True)
    async def update(self, ctx):
        await ctx.reply(f"You need to state what you want to update!\nUse ``{ctx.prefix}help update`` to check the valid arguments")
        logging.info("no sub command given")

    @update.command(case_insensitive=True)
    async def username(self, ctx, *, argument):
        ref = dab.collection("users").document(str(ctx.author.id))
        temp = ref.get().get("user_fields")
        temp.update({"username": argument})
        ref.update({"user_fields": temp})
        await ctx.reply(f"I've updated your username to {argument}!")
        logging.info(f"{ctx.author.name} has updated their username to {argument}")

    @update.command(case_insensitive=True)
    async def scoresaber(self, ctx, argument):
        if argument.isdigit():
            argument = "https://scoresaber.com/u/"+argument
        else:
            argument = argument.split("?", 1)[0]
            argument = argument.split("&", 1)[0]
        ref = dab.collection("users").document(str(ctx.author.id))
        ref.update({'scoresaber': argument})
        await ctx.reply("I've updated your Scoresaber")
        logging.info(f"{ctx.author.name} has updated their scoresaber to {argument}")

    @update.command(case_insensitive=True)
    async def steam(self, ctx, argument):
        ref = dab.collection("users").document(str(ctx.author.id))
        temp = ref.get().get("user_links")
        temp.update({"steam": argument})
        ref.update({"user_links": temp})
        await ctx.reply("I've updated your Steam")
        logging.info(f"{ctx.author.name} has updated their steam to {argument}")

    @update.command(case_insensitive=True)
    async def twitch(self, ctx, argument):
        ref = dab.collection("users").document(str(ctx.author.id))
        temp = ref.get().get("user_links")
        temp.update({"twitch": argument})
        ref.update({"user_links": temp})
        await ctx.reply("I've updated your Twitch")
        logging.info(f"{ctx.author.name} has updated their twitch to {argument}")

    @update.command(case_insensitive=True)
    async def youtube(self, ctx, argument):
        ref = dab.collection("users").document(str(ctx.author.id))
        temp = ref.get().get("user_links")
        temp.update({"youtube": argument})
        ref.update({"user_links": temp})
        logging.info(f"{ctx.author.name} has updated their youtube to {argument}")

    @update.command(case_insensitive=True)
    async def twitter(self, ctx, argument):
        ref = dab.collection("users").document(str(ctx.author.id))
        temp = ref.get().get("user_links")
        temp.update({"twitter": argument})
        ref.update({"user_links": temp})
        await ctx.reply("I've updated your Twitter")
        logging.info(f"{ctx.author.name} has updated their twitter to {argument}")

    @update.command(case_insensitive=True)
    async def reddit(self, ctx, argument):
        ref = dab.collection("users").document(str(ctx.author.id))
        temp = ref.get().get("user_links")
        temp.update({"reddit": argument})
        ref.update({"user_links": temp})
        logging.info(f"{ctx.author.name} has updated their reddit to {argument}")

    @update.command(case_insensitive=True)
    async def birthday(self, ctx, argument):
        if ((bool(search(r"\d/", argument)))) is False:
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
            pass
        ref = dab.collection("users").document(str(ctx.author.id))
        temp = ref.get().get("user_fields")
        temp.update({"birthday": argument})
        ref.update({"user_fields": temp})
        await ctx.reply(f"I've updated your birthday to {argument}!")
        logging.info(f"{ctx.author.name} has updated their birthday to {argument}")

    @update.command(case_insensitive=True)
    async def hmd(self, ctx, *, argument):
        valid_HMD_low = [x.lower() for x in self.bot.valid_HMD]
        try:
            pos = valid_HMD_low.index(argument.lower()) 
        except ValueError:
            logging.info(f"{argument} not in valid_HMD")
            return await ctx.reply(f"That HMD isn't valid!\n``Use {ctx.prefix}help update to check the valid HMDs``")
        ref = dab.collection("users").document(str(ctx.author.id))
        temp = ref.get().get("user_fields")
        temp.update({"hmd": self.bot.valid_HMD[pos]})
        ref.update({"user_fields": temp})
        await ctx.reply(f"I've updated your HMD to {self.bot.valid_HMD[pos]}!")
        logging.info(f"{ctx.author.name} has updated their status to {self.bot.valid_HMD[pos]}")

    @update.command(case_insensitive=True)
    async def pfp(self, ctx, argument):
        if argument[:4] != "http":
            logging.info(f"Argument is not a link ({argument})")
            return await ctx.reply("You can only use links for your profile picture!")
        ref = dab.collection("users").document(str(ctx.author.id))
        temp = ref.get().get("user_fields")
        temp.update({"pfp": argument})
        ref.update({"user_fields": temp})
        await ctx.reply("I've updated your pfp")
        logging.info(f"{ctx.author.name} has updated their pfp to {argument}")

    @update.command(case_insensitive=True)
    async def status(self, ctx, *, argument):
        ref = dab.collection("users").document(str(ctx.author.id))
        temp = ref.get().get("user_fields")
        temp.update({"status": argument})
        ref.update({"user_fields": temp})
        await ctx.reply("I've updated your status")
        logging.info(f"{ctx.author.name} has updated their status to {argument}")

    @update.command(aliases=["color"])  # Americans ew
    async def colour(self, ctx, argument):
        logging.info(f"Recieved user update colour {ctx.author.id} in {ctx.guild.name}")
        try:
            await commands.ColourConverter().convert(ctx, "0x"+argument)
        except Exception as e:
            await ctx.reply("Please use a valid hexadecimal colour value. uwu")
            return logging.info(f"expect triggered: {e}")
        ref = dab.collection("users").document(str(ctx.author.id))
        temp = ref.get().get("user_fields")
        temp.update({"colour": argument})
        ref.update({"user_fields": temp})
        await ctx.reply("I've updated your colour")
        logging.info(f"{ctx.author.name} has updated their colour to {argument}")


def setup(bot):
    bot.add_cog(User(bot))
