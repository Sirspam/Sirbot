from json.decoder import JSONDecodeError
import logging
from json import loads

from discord import Embed, Colour
from datetime import datetime

from discord.ext import commands, menus
from discord.ext.commands.errors import BadArgument
from utils.emotes import diff_emotes, diff_stats_emotes


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
    """Get information on BeatMaps"""
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.group(invoke_without_command=True, aliases=["bs","bsr"], help="Gets information on a certain BeatMap")
    async def beatsaver(self, ctx, beatmap_key, difficulty=None):
        async with self.bot.session.get(f"https://beatsaver.com/api/maps/beatsaver/{beatmap_key}") as resp:
            try:
                response = loads(await resp.text())
            except JSONDecodeError:
                raise commands.BadArgument
        if "error" in response:
            if response["error"] != "Not Found":
                logging.error(response["error"])
            raise commands.BadArgument
        m, s = divmod(response["metadata"]["duration"], 60)
        embed = Embed(
            title=response["name"],
            url=f"https://beatsaver.com/maps/{beatmap_key}",
            colour=Colour.dark_blue()
        )
        if difficulty is None:
            diff_stats = response["versions"][0]["diffs"][-1]
        else:
            for diff in response["versions"][0]["diffs"]:
                if diff["difficulty"].lower() == difficulty.lower():
                    diff_stats = diff
                    break
            if not diff_stats:
                raise BadArgument
        # Could be improved, logic errors if map has more than one characteristic
        # Low prioty issue though since majority of maps now a days all use the standard characteristic
        diff_emotes_message = str()
        for diff in response["versions"][0]["diffs"]:
            diff_name = diff['difficulty']
            diff_emotes_message=f"{diff_emotes_message} {diff_emotes[diff_name]}"
        embed.add_field(
            name="Map Stats",
            value=f"Duration: {m:02d}:{s:02d}\nBPM: {response['metadata']['bpm']}\nMapper: {response['metadata']['levelAuthorName']}\n{diff_emotes_message}",
            inline=True
        )
        embed.add_field(
            name="BeatSaver Stats",
            value=f"🔑: {response['id']}\n💾: {response['stats']['downloads']:,}\n💯: {int(response['stats']['score']*100)}%\n📅: {(datetime.fromisoformat(response['uploaded'][:-1])).strftime('%Y/%m/%d')}",
            inline=True
        )
        embed.add_field(name="\u200B",value="\u200B",inline=True)
        value = f"{diff_stats_emotes['nps']}: {round(diff_stats['nps'],2)}\n{diff_stats_emotes['njs']}: {diff_stats['njs']}\n{diff_stats_emotes['notes']}: {diff_stats['notes']}\n{diff_stats_emotes['bombs']}: {diff_stats['bombs']}"
        if "stars" in diff_stats:
            value = f"{diff_stats_emotes['star']}: {diff_stats['stars']}\n" + value
        embed.add_field(
            name=f"Difficulty Stats {diff_emotes[(diff_stats['difficulty'])]}",
            value=value,
            inline=True
        )
        embed.add_field(
            name="Links",
            value=f"[Preview Map](https://skystudioapps.com/bs-viewer/?id={response['id']})\n[Download Map]({response['versions'][0]['downloadURL']})\n[Song on Youtube](https://www.youtube.com/results?search_query={response['metadata']['songAuthorName'].replace(' ','+')}+{response['name'].replace(' ','+')})\n[Song on Spotify](https://open.spotify.com/search/{response['name'].replace(' ','%20')})",
            inline=True
        )
        embed.add_field(name="\u200B",value="\u200B",inline=True)
        embed.set_image(url=response['versions'][0]['coverURL'])
        await ctx.reply(embed=embed)


    @beatsaver.command(aliases=["s"], help="Searches for BeatMaps")
    async def search(self, ctx, *, query):
        async with ctx.channel.typing():
            query = query.replace(' ','%20')
            async with self.bot.session.get(f"https://beatsaver.com/api/search/text/0?sortOrder=Relevance&q={query}") as resp:
                response = loads(await resp.text())
        embed = Embed(colour=Colour.dark_blue())
        embed.set_thumbnail(url=f"https://cdn.beatmaps.io/{response['docs'][0]['versions'][0]['hash']}.jpg")
        embed.set_author(
            name="BeatSaver Search",
            url=f"https://beatsaver.com/?q={query}"
        )
        data = list()
        for result in response["docs"]:
            if result["automapper"] is True:
                author_emote = "🤖"
            else:
                author_emote = "🥰"
            diff_message = str()
            for diff in result["versions"][0]["diffs"]:
                diff_name = diff['difficulty']
                diff_message=f"{diff_message} {diff_emotes[diff_name]}"
            m, s = divmod(result["metadata"]["duration"], 60)
            message = f"""🔑 {result['id']}
            {author_emote} {result['metadata']['levelAuthorName']}
            💾 {result['stats']['downloads']:,}
            💯 {int(result['stats']['score']*100)}%
            ⏱ {m:02d}:{s:02d}
            📅 {(datetime.fromisoformat(result['uploaded'][:-1])).strftime('%Y/%m/%d')}
            {diff_message}
            [BS Page](https://beatsaver.com/maps/{result['id']})"""
            data.append((result["name"], message))
        pages = menus.MenuPages(source=SearchMenu(data, embed), clear_reactions_after=True)
        await pages.start(ctx)

    @beatsaver.command(aliases=["l"], help="Gets the latest BeatMaps")
    async def latest(self, ctx):
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatsaver.com/api/maps/latest") as resp:
                response = loads(await resp.text())
        embed = Embed(colour=Colour.dark_blue())
        embed.set_thumbnail(url=f"https://cdn.beatmaps.io/{response['docs'][0]['versions'][0]['hash']}.jpg")
        embed.set_author(
            name="BeatSaver Latest",
            url=f"https://beatsaver.com/"
        )
        data = list()
        for result in response["docs"]:
            if result["automapper"] is True:
                author_emote = "🤖"
            else:
                author_emote = "🥰"
            diff_message = str()
            for diff in result["versions"][0]["diffs"]:
                diff_name = diff['difficulty']
                diff_message=f"{diff_message} {diff_emotes[diff_name]}"
            m, s = divmod(result["metadata"]["duration"], 60)
            message = f"""🔑 {result['id']}
            {author_emote} {result['metadata']['levelAuthorName']}
            💾 {result['stats']['downloads']:,}
            💯 {int(result['stats']['score']*100)}%
            ⏱ {m:02d}:{s:02d}
            📅 {(datetime.fromisoformat(result['uploaded'][:-1])).strftime('%Y/%m/%d')}
            {diff_message}
            [BS Page](https://beatsaver.com/maps/{result['id']})"""
            data.append((result["name"], message))
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