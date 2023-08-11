import discord
import asyncio
import json

async def update() -> None: ...

class Activity(discord.ui.View):
    button=discord.ui.button

    def __init__(self, *, timeout: float | None = 180, id, status, description, nameList: dict = {}):
        super().__init__(timeout=timeout)
        self.id=id
        self.status=status
        self.msg=description
        self.nameList=nameList

    def serialization(self):
        return {"id": self.id, "status": self.status, "description": self.msg, "nameList": list(self.nameList.keys())}

    def get_nameList(self):
        return "已报名名单："+"、".join(self.nameList.keys())
    
    def get_str(self):
        id="ID: "+self.id
        status="状态："+("进行中" if self.status else "已结束")
        msg="描述："+self.msg
        return '\n'.join([id, status, msg])
    
    async def activity_query(self, ctx):
        if self.status:
            await ctx.send(self.get_str()+"\n"+self.get_nameList(), view=self)
        else :
            await ctx.send("这个活动已经结束啦~")
    
    async def activity_end(self, ctx):
        self.status=False
        await ctx.send(self.get_str())

    @button(label="点击报名", style=discord.ButtonStyle.blurple)
    async def signUp(self, interaction: discord.Interaction, button: discord.ui.Button):
        username=interaction.user.name
        content=""
        try :
            self.nameList[username]
            content=self.get_str()+"\n"+self.get_nameList()+"\n\n"+username+"已报名"
        except KeyError:
            self.nameList[username]=None
            await update()
            content=self.get_str()+"\n"+self.get_nameList()+"\n\n"+username+"报名成功"
        await interaction.response.edit_message(content=content)

activityDict: dict[str, Activity] = {}

async def update():
    with open("activities.json", "w", encoding="utf-8") as sync:
        serialize={}
        keys=activityDict.keys()
        for k in keys:
            serialize[k]=activityDict[k].serialization()
        sync.write(json.dumps(serialize, ensure_ascii=False, indent=4))

async def loadAction():
    with open("activities.json", "r", encoding="utf-8") as loadFile:
        lines=""
        for l in loadFile:
            lines+=l
        tempDict: dict = json.loads(lines)
        keys=tempDict.keys()
        for k in keys:
            infoDict=tempDict[k]
            id=infoDict["id"]
            status=infoDict["status"]
            description=infoDict["description"]
            nameList={name:None for name in infoDict["nameList"]}
            activityDict[k]=Activity(id=id, status=status, description=description, nameList=nameList)

async def loadActivities():
    try :
        await loadAction()
    except FileNotFoundError:
        await update()

loop = asyncio.get_event_loop()
loop.run_until_complete(loadActivities())