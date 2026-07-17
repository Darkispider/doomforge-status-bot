import os,discord
from discord.ext import tasks,commands
from mcstatus import JavaServer
from dotenv import load_dotenv
load_dotenv()
TOKEN=os.getenv("TOKEN")
SERVER=os.getenv("SERVER")
CHANNEL_ID=int(os.getenv("CHANNEL_ID"))
bot=commands.Bot(command_prefix="!",intents=discord.Intents.default())
msg=None
@bot.event
async def on_ready():
    global msg
    ch=bot.get_channel(CHANNEL_ID)
    async for m in ch.history(limit=20):
        if m.author==bot.user:
            msg=m;break
    if not msg: msg=await ch.send("Loading...")
    update.start()
@tasks.loop(minutes=1)
async def update():
    global msg
    try:
        s=JavaServer.lookup(SERVER);st=s.status()
        e=discord.Embed(title="🟢 DoomForgeSMP",color=discord.Color.green())
        e.add_field(name="Status",value="Online")
        e.add_field(name="Players",value=f"{st.players.online}/{st.players.max}")
        e.add_field(name="Version",value=st.version.name,inline=False)
    except:
        e=discord.Embed(title="🔴 DoomForgeSMP",description="Offline",color=discord.Color.red())
    await msg.edit(embed=e)
bot.run(TOKEN)
