import discord
import os
import logging
import firebase_admin
from discord.ext import commands
from firebase_admin import credentials
from dotenv import load_dotenv
from utils import jskp
from utils import prefixes

cwd = os.getcwd()
load_dotenv(f"{cwd}/config.env")

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "sirbot-ede0f",
  "private_key_id": "f1fbbcf05486794a193588e3bf07e1b77c784e18",
  "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
  "client_email": "firebase-adminsdk-gtv4c@sirbot-ede0f.iam.gserviceaccount.com",
  "client_id": "110941093760249580602",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-gtv4c%40sirbot-ede0f.iam.gserviceaccount.com"
})
firebase_admin.initialize_app(cred)

async def prefix(bot, ctx):
    try:
        result = await prefixes.get_prefix(bot, ctx)
        if result is None:
            return ">"
        else:
            return result
    except:
        return ">"

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True, help_command=None, allowed_mentions=discord.AllowedMentions(replied_user=False))

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

bot.header = {"User-Agent": "Sirbot (https://github.com/sirspam/Sirbot)"} # Just guessing the url, need to update it after creating the repo
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
    "cogs.error_handler",
    "cogs.user",
    "cogs.scoresaber",
    "cogs.neko",
    "cogs.text",
    "cogs.help"
]

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
        logging.info(f"Successfully loaded {cog}")
    except Exception as e:
        logging.error(f"Failed to load cog {cog}: {e}")

@bot.event
async def on_ready():
    logging.info('Bot has successfully launched as {0.user}'.format(bot))
    await prefixes.cache_prefixes()


bot.run(os.getenv("TOKEN"))
