import logging
from os import getcwd, getenv
from asyncio import get_event_loop

from discord import Intents, AllowedMentions
from firebase_admin import initialize_app
from aiohttp import ClientSession
from dotenv import load_dotenv

from discord.ext import commands
from firebase_admin import credentials
from utils import prefixes


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', level=logging.INFO)

load_dotenv(getcwd()+"/.env")

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "sirbot-ede0f",
  "private_key_id": "f1fbbcf05486794a193588e3bf07e1b77c784e18",
  "private_key": getenv("PRIVATE_KEY").replace('\\n', '\n'),
  "client_email": "firebase-adminsdk-gtv4c@sirbot-ede0f.iam.gserviceaccount.com",
  "client_id": "110941093760249580602",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-gtv4c%40sirbot-ede0f.iam.gserviceaccount.com"
})
initialize_app(cred)


async def prefix(bot, ctx):
    result = await prefixes.get_prefix(ctx)
    if result is None:
        return commands.when_mentioned_or(bot.default_prefix)(bot, ctx)
    return commands.when_mentioned_or(result)(bot, ctx)


intents = Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=prefix, 
    intents=intents, 
    case_insensitive=True, 
    allowed_mentions=AllowedMentions(
        everyone=False,
        roles=False,
        replied_user=False
    )
)

bot.default_prefix = getenv("DEFAULT_PREFIX")
bot.github_repo = getenv("GITHUB_REPO_URL")
bot.logging_channel_id = int(getenv("LOGGING_CHANNEL_ID"))
bot.valid_HMD = [
            "CV1",
            "Rift S",
            "Quest",
            "Quest 2",
            "Index",
            "Vive",
            "WMR"
            ]


initial_cogs = [
    "jishaku",
    "cogs.admin",
    "cogs.beatsaver",
    "cogs.error_handler",
    "cogs.fun",
    "cogs.information",
    "cogs.help",
    "cogs.listeners",
    "cogs.scoresaber",
    "cogs.status"
]

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
        logging.info(f"Successfully loaded {cog}")
    except Exception as e:
        logging.error(f"Failed to load cog {cog}: {e}")

async def startup():
    await bot.wait_until_ready()
    bot.session = ClientSession(loop=get_event_loop(), headers={"User-Agent": "Sirbot (https://github.com/sirspam/Sirbot)"})
    bot.owner_id = (await bot.application_info()).owner.id
    await prefixes.cache_prefixes()

bot.loop.create_task(startup())


@bot.before_invoke
async def before_invoke(ctx):
    logging.info(f"Invoked {ctx.command} in {ctx.guild.name} by {ctx.author.name} ({ctx.message.content})" )
@bot.after_invoke
async def after_invoke(ctx):
    logging.info(f"Concluded {ctx.command}")


bot.run(getenv("TOKEN"))
