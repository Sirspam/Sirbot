import logging
from json import loads

from discord import Embed, Colour
from datetime import datetime

from discord.ext import commands, menus
from utils.emotes import diff_emotes


async def diff_sort(difficulties):
    diff_order = diff_copy = ["easy","normal","hard","expert","expertPlus"]
    for diff in diff_order:
        if diff not in difficulties:
            diff_copy.remove(diff)
    return [x for _,x in sorted(zip(difficulties,diff_copy))]


class SearchMenu(menus.ListPageSource):
    def __init__(self, data, embed):
        super().__init__(data, per_page=6)
        self.embed = embed

    async def format_page(self, menu, entries):
        self.embed.clear_fields()
        self.embed.set_footer(text=f"Page {(menu.current_page+1)}/{self.get_max_pages()}")
        gap_check = True
        for entry in entries:
            self.embed.add_field(
                name=entry[0],
                value=entry[1],
                inline=True
            )
            if gap_check is True:
                self.embed.add_field(
                    name="\u200b",
                    value="\u200b",
                    inline=True
                )
                gap_check = False
            else:
                gap_check = True
        return self.embed


class BeatSaver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.group(invoke_without_command=True, aliases=["bs","bsr"])
    async def beatsaver(self, ctx, key, diff=None):
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatsaver.com/api/maps/detail/{key}") as resp:
                if await resp.text() == "Not Found":
                    raise commands.BadArgument
                response = loads(await resp.text())
            difficulties = list()
            for x in response["metadata"]["difficulties"]:
                if response["metadata"]["difficulties"][x] is True:
                    difficulties.append(x)
            difficulties = await diff_sort(difficulties)
            if diff is not None and diff in difficulties:
                diff_stats = response["metadata"]["characteristics"][0]["difficulties"][diff]
            else:
                diff = difficulties[-1]
                diff_stats = response["metadata"]["characteristics"][0]["difficulties"][diff]
            if response["metadata"]["songSubName"] == '':
                title = response["metadata"]["songName"]
            else:
                title = response["metadata"]["songName"]+" - "+response["metadata"]["songSubName"]
            m, s = divmod(response["metadata"]["duration"], 60)
            embed = Embed(
                title=title,
                url=f"https://beatsaver.com/beatmap/{key}",
                description=f"**{response['metadata']['songAuthorName']}**",
                colour=Colour.dark_blue()
            )
            message=str()
            for difficulty in difficulties:
                message=f"{message} {diff_emotes[difficulty]}"
            embed.add_field(
                name="Map Stats",
                value=f"Duration: {m:02d}:{s:02d}\nBPM: {response['metadata']['bpm']}\nMapper: {response['metadata']['levelAuthorName']}\n{message}",
                inline=True
            )
            embed.add_field(
                name="BeatSaver Stats",
                value=f"🔑: {response['key']}\n💾: {response['stats']['downloads']:,}\n💯: {int(response['stats']['rating']*100)}%\n📅: {(datetime.fromisoformat(response['uploaded'][:-1])).strftime('%Y/%m/%d')}",
                inline=True
            )
            embed.add_field(name="\u200B",value="\u200B",inline=True)
            embed.add_field(
                name=f"Difficulty Stats {diff_emotes[diff]}",
                value=f"NPS: {round(diff_stats['notes']/diff_stats['length'],2)}\nNJS: {diff_stats['njs']}\nNotes: {diff_stats['notes']}\nBombs: {diff_stats['bombs']}",
                inline=True
            )
            embed.add_field(
                name="Links",
                value=f"[Preview Map](https://skystudioapps.com/bs-viewer/?id={response['key']})\n[Download Map](https://beatsaver.com/api/download/key/{response['key']})\n[Song on Youtube](https://www.youtube.com/results?search_query={response['metadata']['songAuthorName'].replace(' ','+')}+{title.replace(' ','+')})\n[Song on Spotify](https://open.spotify.com/search/{response['metadata']['songName'].replace(' ','%20')})",
                inline=True
            )
            embed.add_field(name="\u200B",value="\u200B",inline=True)
            embed.set_image(url="https://beatsaver.com"+response["coverURL"])
            await ctx.reply(embed=embed)


    @beatsaver.command(aliases=["s", "map"])
    async def search(self, ctx, *, query):
        async with ctx.channel.typing():
            query = query.replace(' ','%20')
            async with self.bot.session.get(f"https://beatsaver.com/api/search/text/0?q={query}&?automapper=1") as resp:
                response = loads(await resp.text())
        embed = Embed(colour=Colour.dark_blue())
        embed.set_thumbnail(url="https://beatsaver.com"+response["docs"][0]["coverURL"])
        embed.set_author(
            name="BeatSaver Search",
            url=f"https://beatsaver.com/search?q={query}"
        )
        data = list()
        for result in response["docs"]:
            if result["metadata"]["songSubName"] == '':
                title = result["metadata"]["songName"]
            else:
                title = result["metadata"]["songName"]+" - "+result["metadata"]["songSubName"]
            if result['metadata']['levelAuthorName'] == "Beat Sage":
                author_emote = "🤖"
            else:
                author_emote = "🥰"
            difficulties = list()
            for x in result["metadata"]["difficulties"]:
                if result["metadata"]["difficulties"][x] is True:
                    difficulties.append(x)
            difficulties = await diff_sort(difficulties)
            diff_message = str()
            for difficulty in difficulties:
                diff_message = f"{diff_message} {diff_emotes[difficulty]}"
            m, s = divmod(result["metadata"]["duration"], 60)
            message = f"""🔑 {result['key']}
            {author_emote} {result['metadata']['levelAuthorName']}
            💾 {result['stats']['downloads']:,}
            💯 {int(result['stats']['rating']*100)}%
            ⏱ {m:02d}:{s:02d}
            📅 {(datetime.fromisoformat(result['uploaded'][:-1])).strftime('%Y/%m/%d')}
            {diff_message}
            [BS Page](https://beatsaver.com/beatmap/{result['key']})"""
            data.append((title, message))
        pages = menus.MenuPages(source=SearchMenu(data, embed), clear_reactions_after=True)
        await pages.start(ctx)


    @beatsaver.error
    async def beatsaver_error(self, ctx, error):
        logging.info("beatsaver local error handler invoked")
        if isinstance (error, commands.BadArgument):
            logging.info("BadArgument handler ran")
            return await ctx.reply(embed=Embed(
                title="Bad Argument",
                description="You should totally try ``e970`` though <:AYAYATroll:839891422140432405>",
                colour=Colour.red()
            ))
        if isinstance (error, commands.MissingRequiredArgument):
            logging.info(f"MissingRequiredArgument handler ran")
            return await ctx.reply(embed=Embed(
                title="Missing Required Arguments",
                description="You should totally try ``e970`` though <:AquaTroll:845802819634462780>",
                colour=Colour.red()
            ))
        logging.info("Error unhandled by local handler")
        return delattr(ctx.command, "on_error")


def setup(bot):
    bot.add_cog(BeatSaver(bot))