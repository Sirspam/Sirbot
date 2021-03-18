import discord
import os
import logging
import firebase_admin
from discord.ext import commands
from firebase_admin import credentials
from dotenv import load_dotenv
from utils import jskp

cwd = os.getcwd()
load_dotenv(f"{cwd}/config.env")

cred = credentials.Certificate(f"{cwd}/sirbot-ede0f-firebase-adminsdk-gtv4c-f1fbbcf054.json")
firebase_admin.initialize_app(cred)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!s ",intents=intents,case_insensitive=True,allowed_mentions=discord.AllowedMentions(replied_user=False))

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
    "cogs.text"
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



bot.run(os.getenv("TOKEN"))