import os
from dotenv import load_dotenv
import discord
from discord.ext import commands



load_dotenv()
intents = discord.Intents.all()
intents.message_content = True
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready(): 
    print("bot ready")


@bot.command()
async def ping(context):
    await context.send('pong')

@bot.command()
async def follow(context, member: discord.Member=None):
    if member == None:
        member = context.author
    await context.send(member.status) 

@bot.event
async def on_presence_update(before,after):
    if before.id != (543494691790913706):
        print(before.id)
        return
    else:            
        channel = bot.get_channel(1098615350381248684)
        print("updated")
        embed = discord.Embed(title=f"{before.nick}'s status is was {before.status} but is now {after.status}", color=0x00ff00)
        embed.add_field(name="Username:", value=after.name, inline=True)
        embed.add_field(name="ID:", value=after.id, inline=True)
        embed.add_field(name="Status:", value=after.status, inline=True)
        embed.add_field(name="Highest Role:", value=after.top_role, inline=True)
        embed.add_field(name="Joined:", value=after.joined_at, inline=True)
        embed.set_thumbnail(url=before.avatar)
        await channel.send(embed=embed)





bot.run(os.getenv('TOKEN'))