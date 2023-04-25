from library.bot import bot
import nextcord
import asyncio



VERSION = "0.0.5"

async def main():

    await bot.run(VERSION)


asyncio.run(main())