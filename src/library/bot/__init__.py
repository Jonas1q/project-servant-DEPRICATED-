from datetime import datetime
from glob import glob

from nextcord import Intents, Embed, File
from nextcord.ext.commands import Bot as BotBase
from nextcord.ext.commands import CommandNotFound, Command

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import os
from dotenv import load_dotenv

from ..db import db

PREFIX = "!"
OWNER_IDS = [560199790298660865]
COGS =  [path.split("\\")[-1][:-3] for path in glob("./library/cogs/*.py")]

class Bot(BotBase):
    def __init__(self):
        load_dotenv()
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        
        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=PREFIX, 
            owner_ids=OWNER_IDS,
            intents = Intents.all()
        )

    async def setup(self):
        for cog in COGS:
            await self.load_extension(f"src.library.cogs.{cog}")
            print(f"{cog} cog loaded")

        print("setup done")

    async def run(self, version):
        self.VERSION = version
        self.TOKEN = str(os.getenv('TOKEN'))

        print("running setup...")
        self.setup()
        super().run(self.TOKEN, reconnect=True)

    async def print_message(self):
        await self.stdout.send("Im a timed notif")
    
    async def on_connect(self):
        print("alive")

    async def on_disconnect(self):
        print("dead")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(745773485690847233)
            self.stdout = self.get_channel(1098919725469290507)
            #self.scheduler.add_job(self.print_message, CronTrigger(second="0,15,30,45"))
            self.scheduler.start()

            
            await self.stdout.send("Now online :D")

            #embed = Embed(title="Now online :D", description="We are now ready to serve", color=0xA020F0, timestamp=datetime.now())
            #fields = [("Name", "Value", True), ("Some other field", "Im next to you", True), ("Im not inline", "Im gonna appear on my own", False)]
            #for name, value, inline in fields:
            #    embed.add_field(name = name, value = value, inline = inline)
            #embed.set_footer(text = "im a footer")
            #embed.set_author(name = "Cactus", icon_url = self.guild.icon)
            #embed.set_thumbnail(url = self.guild.icon)
            #embed.set_image(url = self.guild.icon)
            #await channel.send(embed=embed)
            #await channel.send(file=File("src/data/images/red_omen.jpg"))
            print("bot ready")

        else:
            print("bot reconnecting...")

    async def on_error(self, error, *args, **kwargs):
        if error == "on_command_error":
            await args[0].send("Something is wrong")
        await self.stdout.send("An error occured")
        raise

    async def on_command_error(self, context, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exc, "original"):
            raise exc.original
        else: 
            raise exc
        
    async def on_message(self, message):
        pass

bot = Bot()