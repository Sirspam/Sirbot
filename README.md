Sirbot has been archived as I no longer want to continue this project. As a result of a handful of issues regarding API interaction in the other cogs, I've decided to remove them all and keep the fun cog for the hosted version of Sirbot (since this bot is mainly used for cat girl pictures lmao.) This version of Sirbot is in the 'fun' branch.

# Sirbot
[![CodeFactor](https://www.codefactor.io/repository/github/sirspam/sirbot/badge)](https://www.codefactor.io/repository/github/sirspam/sirbot)

[Discord invite link](https://discord.com/api/oauth2/authorize?client_id=822029618969182218&permissions=313408&scope=bot)

Sirbot's main function is interaction with the [ScoreSaber](https://scoresaber.com/) API, although it does feature some other functions. 

## How to use Sirbot
Sirbot's default prefix is **.** although a server admin can change this to a custom prefix. Mentioning the bot is also a valid prefix.

The rest of the bot is just your usual discord bot, put in the prefix then the command you want. "But what commands does Sirbot have?" I hearing you asking, well that leads us onto our next header, **Sirbot Commands**.

## Sirbot Commands
This'll be an excessively long list, so go grab some popcorn
### Help Commands
You know, commands for when you need help with Sirbot.
| Command | Description |
| --- | --- |
| help | Posts an embed which will basically give you the same amount of information which this readme is giving you. |
| help user | Help for the user command and it's subcommands |
| help update | A massive ass list of the things you can change with your user embed |
| help scoresaber | Makes the bot leave the guild. Requires admin privilages. |
| help waifu | Help for the neko command and it's subcommands. Damn right this bot posts cat girls |

### User Commands
| Command | Description |
| --- | --- |
| user | Posts your user embed, or a different user if mentioned |
| user add <ScoreSaber link> | Adds you to Sirbot's database, requires a valid user link from [ScoreSaber](https://scoresaber.com/) |
| user update <field> | Updates your user info. Refer to the big ass list below this for the valid fields |
| user remove | Removes you from the database |
  
### User Update
| Command | Description |
| --- | --- |
| username | Updates your username within the user embed to whatever is specified |
| scoresaber/steam/twitch/youtube/twitter/reddit | Updates your link for the service specified |
| HMD | Updates what Head Mounted Display you're using |
| birthday | Updates your birthday |
| status | Updates your status |
| pfp | Updates your profile picture, the kwarg has to be a link going to an image |
| colour | Updates your profile's embed colour |

Color is an alias for colour, in case your country spells colour incorrectly.
  
### ScoreSaber Commands
| Command | Description |
| --- | --- |
| scoresaber | Gets a user's ScoreSaber data |
| scoresaber topsong | Gets a user's top song |
| scoresaber recentsong | Gets a user's most recent song |
| scoresaber topsongs | Gets a user's page of top songs |
| scoresaber recentsongs | Gets a user's page of most recent songs |
| scoresaber compare <first user> <second user> | Compares two users together |

The embed for scoresaber compare is incredibly scuffed kekw
  
### Waifu Commands
Clearly the best part about this bot
| Command | Description |
| --- | --- |
| waifu | Posts a kawaii waifu |
| neko | Posts a kawaii neko |
| awoo | Posts a kawaii awoo |
| nsfw | Posts an NSFW waifu. (NSFW channel only) |

### General Commands
| Command | Description |
| --- | --- |
| beatsaver <key> <diff> | Posts information about a beatsaver map |
| beatsaver search <query> | Searches for maps on BeatSaver |
| links | Posts an embed with important links relating to Sirbot |
| amogus | ![amogus](https://cdn.discordapp.com/emojis/826403430905937941.png?v=1) |

### Admin Only Commands
| Command | Description |
| --- | --- |
| set_prefix "prefix" | Changes Sirbot's prefix |

## Images
Just going to post images of Sirbot here

![user embed](https://cdn.discordapp.com/attachments/822033695778799616/826755754278518784/unknown.png)
![ScoreSaber embed](https://cdn.discordapp.com/attachments/822033695778799616/826760855223271454/unknown.png)
![BeatSaver embed](https://cdn.discordapp.com/attachments/823851280212557845/842345339692646400/unknown.png)

ok, that it

that's the end of the readme

thanks for reading it

hope you had fun

bye bye
