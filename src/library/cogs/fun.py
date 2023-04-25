from nextcord.ext.commands import Cog, commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.stdout.send("fun cog :D")
        print("fun cog ready")


def setup(bot):
    bot.load_extension(Fun(bot))