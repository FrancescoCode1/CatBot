# Important Notice
I'm not working on this bot anymore. All functionalities are currently ported to [hikari](https://github.com/hikari-py/hikari) + [lightbulb](https://github.com/tandemdude/hikari-lightbulb) a new Discord API and its command handler. I'll probably create a new repository for it.


## CatBot
This is my Discord Bot. I developed it to be more independend. It served me quite well and I add features based on my own demand.

Currently it's divided into 3 parts
-
### Fun commands like sending funny pictures of cats

- !givecat #outputs random picture of cat
- !stats {playername} #outputs PLP player stats
- !status #outputs status of a mc server. 

### Music commands with Wavelink as a lavalink wrapper
 
- !play {youtube} #plays music from youtube link in voice channel

### Moderation update is now live. Basic commands like kick, ban and tban will worl

- !kick
- !ban
- !tban
- (Planned: massive overhaul + user cards --> user info et alia.))
- You can type !help to see a list of all commands + description

How to run this bot
-
This bot is written in python using [Discord.py](https://github.com/Rapptz/discord.py) library. Additionally you'll need Java jdk13 and [Lavalink](https://github.com/Frederikam/Lavalink) for the music stuff.

If you host it yourself make sure to edit the linux stuff out (deprecated). Hosting on cloud is strongly recommended
