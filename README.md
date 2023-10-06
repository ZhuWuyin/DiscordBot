# Activities-Manager-Discord-Bot
This is a robot that can manage activities.

### Commands

**prefix: !**<br><br>
**e.g.**<br>
`You: !ping`<br>
`Bot: Hi`<br>
<br>
| **Command** | **Slash** | **Admin** | **Parameters** |
| - | - | - | - |
| sync | No | Yes | **No parameter** |
| ping | Yes | No | **No parameter** |
| start_activity | Yes | Yes | **id**: Unique ID for an activity;<br>**description**: Details of the activity; |
| end_activity | Yes | Yes | **id**: The unique ID for an activity you want to stop the registration process; |
| query_activity | Yes | No | **id**: The unique ID for an activity you want to query; |
| list_all_activities | Yes | No | **No parameter** |

### How to use<br>
**1.** Download the **exeFile** folder<br>
**2.** Get a robot on **https://discord.com/developers/applications**<br>
**3.** Invite your bot to your server<br>
**4.** Copy the token of your bot and past it to **bots.txt**(Make sure the Bot.exe and bots.txt are in the same folder)<br>
**5.** Double click **Bot.exe**<br><br>
**Then, the program will generate a file called ` activities.json ` which is human-readable**
