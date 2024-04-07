import logging
import discord

logging.basicConfig(level=logging.INFO)


logger = discord.logging.getLogger("discord")
logger.addHandler(logging.FileHandler("discord.log", "w", "utf-8"))