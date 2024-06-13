# Activities-Manager-Discord-Bot
This is a robot that can manage activities, play music, and do other interesting things.

### Commands

**prefix commands (prefix: !):**<br>
| **Command** | **Slash** | **Admin** | **Parameters** |
| - | - | - | - |
| sync | No | Yes | **No parameter** |
| ping | Yes | No | **No parameter** |

**e.g.**<br>
`You: !ping`<br>
`Bot: Hi`<br><br><br>

**slash commands:**
| **Command** | **Admin** | **Parameters** |
| - | - | - |
| ping | No | **No parameter** |
| start_activity | Yes | **id**: Unique ID for an activity;<br>**description**: Details of the activity; |
| end_activity | Yes | **id**: The unique ID for an activity you want to stop the registration process; |
| query_activity | No | **id**: The unique ID for an activity you want to query; |
| list_all_activities | No | **No parameter** |
| forward | No | **content**: What you want the robot to relay for you |
| dice | No | **num_of_dice**： The number of dice you want to roll;<br>**low**: The lowest value of the dice;<br>**high**: The maximum value of the dice|
| play | No | **folder**: Folders with music you wish to play;<br>**index**: The index of the music you want to play(0 is the first music);<br>**play_mode**: The play mode you want;<br>**volume**: The Volume of your bot in the voice channel|
| leave | No | **No parameter** |
| skip | No | **No parameter** |
| list_all_songs | No | **folder**: The folder you want to check 

### <br>
### How to use<br>
**1.** Download the **exeFile** folder<br>
**2.** Get a robot on **https://discord.com/developers/applications**<br>
**3.** Invite your bot to your server<br>
**4.** Copy the token of your bot and past it to **bots.txt**(Make sure the Bot.exe and bots.txt are in the same folder)<br>
**5.** Double click **Bot.exe**<br><br>
**Then, the program will generate a file called ` activities.json ` which is human-readable**
