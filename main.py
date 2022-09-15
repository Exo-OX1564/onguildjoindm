import discord, os, logging, asyncio, json, sys
from discord.ext import commands, tasks


_i = discord.Intents.all()
client = commands.Bot(command_prefix = "$", intents = _i)

"""
_i = discord.Intents.default()
_i.members = True
#i.presences = True 
#Only enable above if you have presence.
client = commands.Bot(command_prefix = commands.when__mentioned, intents = _i, shard_count = 1) # Set shard count here.
"""


with open("./config.json", "r") as file:
  config = json.load(file)
  embedFooterText = config["embedFooterText"]
  embedFootericonURL = config['embedFootericonURL']
  embedImageURL = config['embedImageURL']
  embedThumbnailURL = config['embedThumbnailURL']
  botToken = config['token']

class _AnsiColorizer(object):
    _colors = dict(black=30, red=31, green=32, yellow=33,
                   blue=34, magenta=35, cyan=36, white=37)

    def __init__(self, stream):
        self.stream = stream

    @classmethod
    def supported(cls, stream=sys.stdout):
        if not stream.isatty():
            return False  
        try:
            import curses
        except ImportError:
            return False
        else:
            try:
                try:
                    return curses.tigetnum("colors") > 2
                except curses.error:
                    curses.setupterm()
                    return curses.tigetnum("colors") > 2
            except:
                raise
                return False

    def write(self, text, color):

        color = self._colors[color]
        self.stream.write('\x1b[%s;1m%s\x1b[0m' % (color, text))

class ColorHandler(logging.StreamHandler):
    def __init__(self, stream=sys.stderr):
        super(ColorHandler, self).__init__(_AnsiColorizer(stream))

    def emit(self, record):
        msg_colors = {
            logging.DEBUG: "green",
            logging.INFO: "blue",
            logging.WARNING: "yellow",
            logging.ERROR: "red"
        }

        color = msg_colors.get(record.levelno, "blue")
        self.stream.write(record.msg + "\n", color)


logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(ColorHandler())

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
for handler in LOG.handlers:
    LOG.removeHandler(handler)

LOG.addHandler(ColorHandler())


@client.event
async def on_connect():
  logging.info('[INFO] [Connected to the API.]')

@client.event
async def on_ready():
  await client.change_presence(status= discord.Status.online, activity = discord.Game(name="A status here..."))
  logging.debug(f"[INFO] {client.user} is online.")


@client.event
async def on_guild_join(guild):
  """
  guilds = open('guilds.txt', 'r').read().splitlines()
  if str(guild.id) in guilds:
    logging.error(f"[INGORING] [{guild.id}] | Server already dmed, ignoring")
    return
  else:
  """
  blacklisted = open('blacklisted.txt', 'r').read().splitlines()
  logging.debug(f'[INFO] Joined a guild, starting DMALL | [{guild.id}] [{guild.name}]')
  """
  with open('guilds.txt', 'a') as file:
    file.write(f"{guild.id}\n")
  """
  members = guild.members
  for member in members:
    try:
      if member == client.user: #or str(member.id) in blacklisted:
        logging.error(f"[IGNORING] [{client.user}] | Cannot DM this user - DMs Closed Or Bot.")
        return
      else:
        #Start of Embed Here.
        dmEmbed = discord.Embed(title="Embed title", description = "A description here with an emoji. :thumbsup: Custom emojis are supported.", color = 0xFF0000) # Change the description, title as you wish. The hex code will be after the 0x
        dmEmbed.set_image(url=embedImageURL) #Set the bots image of embed in config.json [embedImageURL]
        dmEmbed.set_footer(text=embedFooterText or "-", icon_url =embedFootericonURL or "https://media.discordapp.net/attachments/980486928472342558/1019661366296051752/unknown.png") #Set embed footer icon URL in config.json [embedFootericonURL] and set embed footer text in config.json [embedFooterText]
        dmEmbed.set_thumbnail(url=embedThumbnailURL or "https://media.discordapp.net/attachments/980486928472342558/1019661366296051752/unknown.png") #Set embed thumbnail icon URL in config.json [embedThumbnailURL] 
        if str(member.id) not in blacklisted:
          await member.send(embed=dmEmbed)
        #End of embed, don't touch anything below.
        #--------END OF EMBED.------
          logging.debug(f"[SUCCESS] Sent a DM to {member}")
          await asyncio.sleep(.7)
    except discord.HTTPException:
        logging.error(f"[IGNORING] [{member}] | Cannot DM this user - DMs Closed Or Bot.")
    except Exception as BroadException:
        logging.error(f"An error was raised: {BroadException}")
  await client.process_commands(guild)






if __name__ == '__main__':
  client.run(botToken)
