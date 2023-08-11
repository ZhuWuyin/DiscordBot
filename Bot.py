import discord
from discord.ext import commands
from Activity import *

with open("bots", "r") as read:
    token=read.readline()

intents=discord.Intents.default()
intents.message_content=True
bot=commands.Bot(command_prefix="!", intents=intents)

@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Done")

@bot.hybrid_command()
async def ping(ctx):
    await ctx.send("Hi")

@bot.hybrid_command()
@commands.has_permissions(administrator=True)
async def start_activity(ctx, id: str, description: str = ""):
    try :
        activity=activityDict[id]
        await ctx.send("这个ID的活动已经存在啦~\n\n")
        await activityDict[id].activity_query(ctx)
    except KeyError:
        newActivity=Activity(id=id, status=True, description=description)
        activityDict[id]=newActivity
        await newActivity.activity_query(ctx)
        update()
    
@bot.hybrid_command()
async def query_activity(ctx, id: str):
    try :
        await activityDict[id].activity_query(ctx)
    except KeyError:
        await ctx.send("这个活动不存在哦~")

@bot.hybrid_command()
@commands.has_permissions(administrator=True)
async def end_activity(ctx, id: str):
    try :
        await activityDict[id].activity_end(ctx)
        update()
    except KeyError:
        await ctx.send("这个活动不存在哦~")

@bot.hybrid_command()
async def list_all_activities(ctx):
    activityList: list[Activity] =activityDict.values()
    if not activityList:
        await ctx.send("没有任何活动")
    else:
        result=""
        for i in activityList:
            result+=i.get_str()+"\n-----------------------------------\n"
        await ctx.send(result)

bot.run(token)