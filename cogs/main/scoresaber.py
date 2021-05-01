# https://new.scoresaber.com/api/player/76561198091128855/full
# https://new.scoresaber.com/api/static/covers/69E494F4A295197BF03720029086FABE6856FBCE.png
# URL = (f"https://new.scoresaber.com/api/player/{SS_id}/full") - Get UserData
# URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/top/{page}") - #Get Top Songs
# URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/recent/{page}") - #Get Recent Songs
# URL = (f"https://new.scoresaber.com/api/players/{page}") - #Get Global Rankings
# URL = (f"https://new.scoresaber.com/api/players/pages") - #Get Global
# Ranking Pages


from json.decoder import JSONDecodeError
import discord
import requests
import json
import logging
from random import randint
from discord.ext import commands
from firebase_admin import firestore


dab = firestore.client()
SS_id = None


# Makes the embed message for topSong and recentSong
async def songEmbed(self, ctx, arg_page, arg_user: discord.Member, type):
    if arg_user is not None:
        ctx.author = arg_user
        logging.info(f"Argument given, now {ctx.author.name}")
    ref = dab.collection("users").document(str(ctx.author.id)).get()
    if ref.exists is False:
        await ctx.reply("That user isn't in my database!")
        return logging.info("scoresaber is None")
    scoresaber = ref.get('scoresaber')
    SS_id = scoresaber[25:]
    page = (arg_page / 8)
    if page.is_integer() is False:
        page = int(page + 1)
    else:
        page = int(page)
    if type == "recentSong":
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/recent/{page}")
    elif type == "topSong":
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/top/{page}")
    URL1 = (f"https://new.scoresaber.com/api/player/{SS_id}/full")
    logging.info(URL+"\n"+URL1)
    try: 
        json_data = json.loads(requests.get(URL, headers=self.bot.header).text)
    except JSONDecodeError:
            logging.info("JSONDecodeError raised. ScoreSaber API likely dead")
            return await ctx.reply("ScoreSaber returned an invalid json object, meaning the API is probably dead")
    if "error" in json_data:
        logging.info(f"scoresaber api returned an error\n{json_data}")
        return await ctx.reply("ScoreSaber returned an error!\nCheck if your ScoreSaber link is valid")
    songsList = json_data["scores"]
    json_data = json.loads(requests.get(URL1, headers=self.bot.header).text)
    playerInfo = json_data["playerInfo"]
    if page > 1:
        while arg_page >= 8:
            arg_page = (arg_page - 8)
    Song = songsList[(arg_page - 1)]
    URL2 = (f"https://beatsaver.com/api/maps/by-hash/"+Song["songHash"])
    json_data = json.loads(requests.get(URL2, headers=self.bot.header).text)
    songBSLink = (f"https://beatsaver.com/beatmap/"+json_data["key"])
    if Song["maxScore"] == 0:
        songAcc = f"ScoreSaber API being fucky wucky,\nso you get {randint(0, 100)}"
    else:
        songAcc = round((int(Song["score"]) / int(Song["maxScore"])) * 100, 2)
    if Song["difficulty"] == 9:
        difficulty = "<:ExpertPlus_1:822072552268496917><:ExpertPlus_2:822072552506916884><:ExpertPlus_3:822072552514912328>"
    elif Song["difficulty"] == 7:
        difficulty = "<:Expert_1:822072552556855317><:Expert_2:822072552532738068>"
    elif Song["difficulty"] == 5:
        difficulty = "<:Hard_1:822072552288813108><:Hard_2:822072552452522035> "
    elif Song["difficulty"] == 3:
        difficulty = "<:Normal_1:822072552544927774><:Normal_2:822072552582021120><:Normal_3:822072552540864532> "
    elif Song["difficulty"] == 1:
        difficulty = "<:Easy_1:822072552570486804><:Easy_2:822072552407040051>"
    else:
        difficulty = "Please ping Sirspam, k thanks uwu"
    if Song["songSubName"] == '':
        title = Song["songName"]
    else:
        title = Song["songName"]+" - "+Song["songSubName"]
    message = discord.Embed(
        title=title,
        url=songBSLink,
        description="**"+Song["songAuthorName"]+" - "+Song["levelAuthorName"]+f"** {difficulty}",
        colour=0xffdc1b,
        timestamp=ctx.message.created_at
    )
    message.set_author(
        name=playerInfo["playerName"],
        url=scoresaber,
        icon_url="https://new.scoresaber.com" +
        playerInfo["avatar"]
    )
    message.add_field(
        name="Rank <a:PeepoWideBounce_1:822072554353197109><a:PeepoWideBounce_2:822072555614896138><a:PeepoWideBounce_3:822072554680090654>",
        value="#"+str(Song["rank"]),
        inline=False
    )
    message.add_field(
        name="Acc <:PeepoWideAcc_1:822072552767488040><:PeepoWideAcc_2:822072552884404234><:PeepoWideAcc_3:822072552733933579><:PeepoWideAcc_4:822072552930803712>",
        value=f"{songAcc}%",
        inline=False
    )
    message.add_field(
        name="Score <:AquaCollapsed_1:822072553245638696><:AquaCollapsed_2:822072553282732052><:AquaCollapsed_3:822072553433727036>",
        value=Song["score"],
        inline=False
    )
    if Song["pp"] == 0:
        message.add_field(
            name="PP <a:PogBurger_1:822072553237119016><a:PogBurger_2:822072551554940979><a:PogBurger_3:822072551722713099><a:pogburger_4:822072551341293628>",
            value="Unranked",
            inline=False
    )
    else:
        message.add_field(
            name="PP <a:PogBurger_1:822072553237119016><a:PogBurger_2:822072551554940979><a:PogBurger_3:822072551722713099><a:pogburger_4:822072551341293628>",
            value=round(Song["pp"],2),
            inline=False
    )
        message.add_field(
            name="Weighted PP ⚖️<a:PogBurger_1:822072553237119016><a:PogBurger_2:822072551554940979><a:PogBurger_3:822072551722713099><a:pogburger_4:822072551341293628>",
            value=round((Song["weight"] * Song["pp"]),2),
            inline=False
    )
    message.add_field(name="Time Set 🕕🕘", value=(Song["timeSet"])[:10], inline=False)
    message.set_image(url="https://new.scoresaber.com/api/static/covers/" + Song["songHash"] + ".png")
    await ctx.reply(embed=message)
    logging.info("embed message sent")


async def songsEmbed(self, ctx, arg_page, arg_user: discord.Member, type):
    if arg_user is not None:
        ctx.author = arg_user
        logging.info(f"Argument given, now {ctx.author.name}")
    ref = dab.collection("users").document(str(ctx.author.id)).get()
    if ref.exists is False:
        await ctx.reply("That user isn't in my database!")
        return logging.info("scoresaber is None")
    scoresaber = ref.get('scoresaber')
    SS_id = scoresaber[25:]
    if type == "recentSongs":
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/recent/{arg_page}")
        requestType = ("Recent Songs")
    elif type == "topSongs":
        URL = (f"https://new.scoresaber.com/api/player/{SS_id}/scores/top/{arg_page}")
        requestType = ("Top Songs")
    URL1 = (f"https://new.scoresaber.com/api/player/{SS_id}/full")
    logging.info(URL+"\n"+URL1)
    response = requests.get(URL, headers=self.bot.header)
    try:
        json_data = json.loads(response.text)
    except JSONDecodeError:
        logging.info("JSONDecodeError raised. ScoreSaber API likely dead")
        return await ctx.reply("ScoreSaber returned an invalid json object, meaning the API is probably dead")
    if "error" in json_data:
        message = discord.Embed(
            title="Uh Oh, the codie wodie did an oopsie woopsie! uwu",
            description="Check if your ScoreSaber link is valid <:AYAYASmile:789578607688417310>",
            colour=0xff0000)
        return message
    songsList = json_data["scores"]
    json_data = json.loads(requests.get(URL1, headers=self.bot.header).text)
    playerInfo = json_data["playerInfo"]
    songsMessage = ""
    count = 0
    while count != len(songsList):
        Song = songsList[count]
        if Song["songSubName"] == '':
            songTitle = Song["songName"]
        else:
            songTitle = Song["songName"]+" - "+Song["songSubName"]
        songScore = Song["score"]
        if Song["maxScore"] == 0:
            acc = randint(0, 100)
            songAcc = f"ScoreSaber API being fucky wucky, so you get {acc}"
        else:
            songAcc = round((int(songScore) / int(Song["maxScore"])) * 100, 2)
        if Song["pp"] == 0:
            songPP = "Unranked"
            songWeightedPP = "Unranked"
        else:
            songPP = Song["pp"]
            songPP == round(songPP, 2)
            songWeightedPP = round((Song["weight"] * Song["pp"]), 2)
        if Song["difficulty"] == 9:
            difficulty = "Expert+"
        elif Song["difficulty"] == 7:
            difficulty = "Expert"
        elif Song["difficulty"] == 5:
            difficulty = "Hard"
        elif Song["difficulty"] == 3:
            difficulty = "Normal"
        elif Song["difficulty"] == 1:
            difficulty = "Easy"
        else:
            difficulty = "Please ping Sirspam thanks uwu"
        songMessage = (
            f"```Song: {songTitle}, "+Song["songAuthorName"]+" - "+Song["levelAuthorName"]+f" ({difficulty})\nRank: #"+str(Song["rank"])+f"\nAcc: {songAcc}%\nScore: {songScore}\nPP: {songPP}\nWeighted PP: {songWeightedPP}\nTime Set: "+(Song["timeSet"])[:10]+"```")
        songsMessage = songsMessage + songMessage
        count = count + 1
    message = discord.Embed(
        title=playerInfo["playerName"]+f"'s {requestType}",
        url=scoresaber,
        description=songsMessage,
        colour=0xffdc1b,
        timestamp=ctx.message.created_at
    )
    await ctx.reply(embed=message)
    logging.info("embed message sent")


class ScoreSaber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["ss"])
    async def scoresaber(self, ctx, argument: discord.Member=None):
        logging.info(f"Recieved scoresaber {argument} in {ctx.guild.name}")
        if argument is not None:
            ctx.author = argument
            logging.info(f"Argument given, now {ctx.author.name}")
        async with ctx.channel.typing():
            ref = dab.collection("users").document(str(ctx.author.id)).get()
            if ref.exists is False:
                await ctx.reply("That user isn't in my database!")
                return logging.info("scoresaber is None")
            scoresaber = ref.get('scoresaber')
            SS_id = scoresaber[25:]
            URL = (f"https://new.scoresaber.com/api/player/{SS_id}/full")
            logging.info(URL)
            response = requests.get(URL, headers=self.bot.header)
            try:
                json_data = json.loads(response.text)
            except JSONDecodeError:
                logging.info("JSONDecodeError raised. ScoreSaber API likely dead")
                return await ctx.reply("ScoreSaber returned an invalid json object, meaning the API is probably dead")
            if "error" in json_data:
                return await ctx.reply("ScoreSaber returned an error!\nCheck if your ScoreSaber link is valid")
            playerInfo = json_data["playerInfo"]
            scoreStats = json_data["scoreStats"]
            embed = discord.Embed(
                title=playerInfo["playerName"]+"'s ScoreSaber Stats <:PeepoWideHappy_1:822072552683470879><:PeepoWideHappy_2:822072552964882472><:PeepoWideHappy_3:822072553014165573><:PeepoWideHappy_4:822072552800256061>",
                url=scoresaber,
                colour=0xffdc1b,
                timestamp=ctx.message.created_at
            )
            embed.add_field(
                name="Global Rank 🌐",
                value=playerInfo["rank"],
                inline=True
            )
            embed.add_field(
                name=f"Country Rank :flag_"+playerInfo["country"].lower()+":",
                value=playerInfo["countryRank"],
                inline=True
            )
            embed.add_field(
                name="PP <a:PogLick:822072557389217842>",
                value=playerInfo["pp"],
                inline=True
            )
            embed.add_field(
                name="Ranked Acc <:PeepoAcc:822072552326430760>",
                value=str(round(scoreStats["averageRankedAccuracy"], 2))+"%",
                inline=True
            )
            embed.add_field(
                name="Total Play Count <a:PeepoSabers:822072551416922142>",
                value=scoreStats["totalPlayCount"],
                inline=True
            )
            embed.add_field(
                name="Ranked Play Count 🧑‍🌾",
                value=scoreStats["rankedPlayCount"],
                inline=True
            )
            embed.set_thumbnail(
                url="https://new.scoresaber.com" + playerInfo["avatar"]
            )
        await ctx.reply(embed=embed)
        logging.info("Response: ScoreSaber UserData embed")

    @scoresaber.command(aliases=["rs"])
    async def recentsong(self, ctx, argument1=1, argument2=None):
        logging.info(f"Recieved scoresaber recentsong in {ctx.guild.name}")
        async with ctx.channel.typing():
            await songEmbed(self, ctx, argument1, argument2, type="recentSong")
        logging.info("Finished")

    @scoresaber.command(aliases=["ts"])
    async def topsong(self, ctx, argument1=1, argument2=None):
        logging.info(f"Recieved >scoresaber topsong in {ctx.guild.name}")
        async with ctx.channel.typing():
            await songEmbed(self, ctx, argument1, argument2, type="topSong")
        logging.info("Finished")

    @scoresaber.command(aliases=["rss"])
    async def recentsongs(self, ctx, argument1=1, argument2=None):
        logging.info(f"Recieved >scoresaber recentSongs in {ctx.guild.name}")
        async with ctx.channel.typing():
            await songsEmbed(self, ctx, argument1, argument2, type="recentSongs")
        logging.info("Response: ScoreSaber recentSongs embed")

    @scoresaber.command(aliases=["tss"])
    async def topsongs(self, ctx, argument1=1, argument2=None):
        logging.info(f"Recieved >scoresaber topSongs in {ctx.guild.name}")
        async with ctx.channel.typing():
            await songsEmbed(self, ctx, argument1, argument2, type="topSongs")
        logging.info("Response: ScoreSaber topSongs embed")

    @scoresaber.command(aliases=["com"])
    async def compare(self, ctx, argument1: discord.Member=None, argument2: discord.Member=None):
        logging.info(f"Recieved compare {argument1} {argument2} in {ctx.guild.name}")
        if argument1 is None:
            return await ctx.reply("You need to mention someone for me to compare you against!")
        elif argument1 is not None and argument2 is None:
            argument2 = argument1
            argument1 = ctx.author
        async with ctx.channel.typing():
            user1 = dab.collection("users").document(str(argument1.id)).get()
            user2 = dab.collection("users").document(str(argument2.id)).get()
            if user1.exists is False or user2.exists is False:
                await ctx.reply("That user isn't in my database!")
                return logging.info("scoresaber is None")
            scoresaber1 = user1.get('scoresaber')
            scoresaber2 = user2.get('scoresaber')
            SS_id1 = scoresaber1[25:]
            SS_id2 = scoresaber2[25:]
            URL1 = (f"https://new.scoresaber.com/api/player/{SS_id1}/full")
            URL2 = (f"https://new.scoresaber.com/api/player/{SS_id2}/full")
            logging.info(f"{URL1}\n{URL2}")
            response1 = requests.get(URL1, headers=self.bot.header)
            response2 = requests.get(URL2, headers=self.bot.header)
            json_data1 = json.loads(response1.text)
            json_data2 = json.loads(response2.text)
            if "error" in json_data1 or "error" in json_data2:
                return await ctx.reply("ScoreSaber returned an error!\nCheck if your ScoreSaber link is valid")
            playerInfo1 = json_data1["playerInfo"]
            scoreStats1 = json_data1["scoreStats"]
            playerInfo2 = json_data2["playerInfo"]
            scoreStats2 = json_data2["scoreStats"]
            val1 = int(playerInfo1["rank"])
            val2 = int(playerInfo2["rank"])
            if val1 < val2:
                val1 = f"__{val1}__"
            elif val1 > val2:
                val2 = f"__{val2}__"
            message = f"{val1} - 🌐 **Global Rank** 🌐 - {val2}\n"
            val1 = int(playerInfo1["countryRank"])
            val2 = int(playerInfo2["countryRank"])
            if val1 < val2:
                val1 = f"__{val1}__"
            elif val1 > val2:
                val2 = f"__{val2}__"
            message = message + f"{val1} - :flag_"+playerInfo1["country"].lower()+": **Country Rank** :flag_"+playerInfo2["country"].lower()+f": - {val2}\n"
            val1 = int(playerInfo1["pp"])
            val2 = int(playerInfo2["pp"])
            if val1 > val2:
                val1 = f"__{val1}__"
            elif val1 < val2:
                val2 = f"__{val2}__"
            message = message + f"{val1} - <a:PogLick:822072557389217842> **Performance Points** <a:PogLick:822072557389217842> - {val2}\n"
            val1 = float(round(scoreStats2["averageRankedAccuracy"], 2))
            val2 = float(round(scoreStats1["averageRankedAccuracy"], 2))
            if val1 > val2:
                val1 = f"__{val1}__"
            elif val1 < val2:
                val2 = f"__{val2}__"
            message = message + f"{val1}% - <:PeepoAcc:822072552326430760> **Ranked Acc** <:PeepoAcc:822072552326430760> - {val2}%\n"
            val1 = int(scoreStats1["totalPlayCount"])
            val2 = int(scoreStats2["totalPlayCount"])
            if val1 > val2:
                val1 = f"__{val1}__"
            elif val1 < val2:
                val2 = f"__{val2}__"
            message = message + f"{val1} -  <a:PeepoSabers:822072551416922142> **Total Play Count**  <a:PeepoSabers:822072551416922142> - {val2}\n"
            val1 = int(scoreStats1["rankedPlayCount"])
            val2 = int(scoreStats2["rankedPlayCount"])
            if val1 > val2:
                val1 = f"__{val1}__"
            elif val1 < val2:
                val2 = f"__{val2}__"
            message = message + f"{val1} -  🧑‍🌾 **Ranked Play Count**  🧑‍🌾 - {val2}\n"
            embed = discord.Embed(
                title=playerInfo1["playerName"]+" 🆚 "+playerInfo2["playerName"],
                description=message,
                colour=0xffdc1b,
                timestamp=ctx.message.created_at
            )
            await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(ScoreSaber(bot))
