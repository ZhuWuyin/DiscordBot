import discord, random
from Server import Server
from discord.ext import commands
from Activity import *

with open("bots.txt", "r") as read:
    token = read.readline()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents,
                   allowed_mentions=discord.AllowedMentions.none())


@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Done")


@bot.command()
async def ping(ctx):
    await ctx.send("Hi")


@bot.hybrid_command()
@commands.has_permissions(administrator=True)
async def start_activity(ctx, id: str, description: str = ""):
    try:
        activity = activityDict[id]
        await ctx.send("这个ID的活动已经存在啦~\n\n")
        await activity.activity_query(ctx)
    except KeyError:
        newActivity = Activity(id=id, status=True, description=description)
        activityDict[id] = newActivity
        await newActivity.activity_query(ctx)
        await update()


@bot.hybrid_command()
async def query_activity(ctx, id: str):
    try:
        await activityDict[id].activity_query(ctx)
    except KeyError:
        await ctx.send("这个活动不存在哦~")


@bot.hybrid_command()
@commands.has_permissions(administrator=True)
async def end_activity(ctx, id: str):
    try:
        await activityDict[id].activity_end(ctx)
        await update()
    except KeyError:
        await ctx.send("这个活动不存在哦~")


@bot.hybrid_command()
async def list_all_activities(ctx):
    activityList: list[Activity] = activityDict.values()
    if not activityList:
        await ctx.send("没有任何活动")
    else:
        result = ""
        for i in activityList:
            result += i.get_str()+"\n-----------------------------------\n"
        await ctx.send(result)


@bot.hybrid_command()
async def forward(ctx, content: str):
    await ctx.send(content)

@bot.hybrid_command()
async def dice(ctx, num_of_dice: int, low: int, high: int):
    result = []
    total = 0
    for i in range(num_of_dice):
        num = random.randint(low, high)
        total += num
        result.append("骰子 {0} 号：{1}".format(i+1, num))
    await ctx.send("\n".join(result) + "\n\n总和：{0}".format(total))

async def playNext(ctx, voice_channel: discord.VoiceClient, serverBot: Server):
    filename = serverBot.getNext()
    path = serverBot.folder+"/"+filename

    if voice_channel.is_playing():
        voice_channel.stop()

    voice_channel.play(discord.FFmpegPCMAudio(
        executable="ffmpeg.exe", source=path))
    voice_channel.source = discord.PCMVolumeTransformer(
        voice_channel.source, volume=serverBot.volume)

    await ctx.send("\n正在播放："+filename+"\n\n音量："+str(serverBot.volume*100)+"%")


server: dict[discord.Guild, Server] = {}

@bot.hybrid_command(help="play_mode: 随机播放 --> random；循环播放 --> loop；单曲循环 --> single")
async def play(ctx, folder: str, index: int, play_mode: str, volume: float):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("您需要在语音频道中才能使用该命令")
        return

    voice_channel = ctx.voice_client
    serverUser = ctx.guild
    serverBot = None
    if voice_channel is None:
        try:
            serverBot = Server("C:/Users/cos_z/"+folder,
                               play_mode, index, volume)
        except (IndexError, RuntimeError, FileNotFoundError) as e:
            await ctx.send(f"{e}")
            return

        voice_channel = await ctx.author.voice.channel.connect()
        server[serverUser] = serverBot
    else:
        serverBot = server[serverUser]

    if voice_channel.is_playing():
        await ctx.send("机器人正在播放音频")
        return

    while voice_channel.is_connected():
        if not voice_channel.is_playing():
            await playNext(ctx, voice_channel, serverBot)
        await asyncio.sleep(2)


@bot.hybrid_command()
async def leave(ctx):
    voice_channel = ctx.voice_client
    if voice_channel is None:
        await ctx.send("机器人不在语音频道里")
        return

    await voice_channel.disconnect()
    await ctx.send("机器人已离开")


@bot.hybrid_command()
async def skip(ctx):
    voice_channel = ctx.voice_client
    if voice_channel is None:
        await ctx.send("机器人不在语音频道里")
        return

    serverBot = server[ctx.guild]

    await ctx.send(ctx.author.name+" 跳过了当前歌曲")
    await playNext(ctx, voice_channel, serverBot)


@bot.hybrid_command()
async def list_all_songs(ctx, folder):
    try:
        result = ""
        playlist = Server.getPlayList("C:/Users/cos_z/"+folder)
        for i in range(0, len(playlist)):
            result += str(i)+": "+playlist[i]+"\n"
        await ctx.send(result)
    except FileNotFoundError:
        await ctx.send("没有这个文件夹")


bot.run(token)
