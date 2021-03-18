import discord
import logging

log_channel_id = 822049696960610304

async def log_info(self, message):
    logging.info(message)
    await self.bot.get_channel(log_channel_id).send(f"INFO: {message}")

async def log_warning(self, message):
    logging.warning(message)
    await self.bot.get_channel(log_channel_id).send(f"WARNING: {message}")

async def log_error(self, message):
    logging.warning(message)
    await self.bot.get_channel(log_channel_id).send(f"ERROR: {message}")