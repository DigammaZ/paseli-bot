import discord
from discord.ext.commands import Bot
import logging

from discord_credentials import TOKEN
from constants import PREFIX

from cogs.paseli import Paseli
from cogs.japan import Japan
from cogs.sdvx import Sdvx
from cogs.remind import Remind
from cogs.misc import Miscellaneous

cogs = [Paseli, Japan, Sdvx, Remind, Miscellaneous]

class PaseliBot(Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(command_prefix=PREFIX, description='Paseli Bot for 2MF.')

    # Logging
    self.logger = logging.getLogger('discord')
    self.logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    self.logger.addHandler(handler)

  async def on_ready(self):
    print('Logged in as {0.user.name}'.format(self))

  def run(self, token):
    for cog in cogs:
      try:
        self.add_cog(cog(self))
        print('{0} has been loaded.'.format(cog))
      except discord.ClientException as CE:
        print('Client Exception: {0}'.format(CE))
      except ImportError as IE:
        print('Import Error: {0}'.format(IE))

    super().run(token)

if __name__ == '__main__':
  bot = PaseliBot()
  @Bot.listen(name='on_command_error', self=bot)
  async def on_command_error(ctx, error):
    await ctx.send('{0}\nUsage: `{1}{2}`'.format(error, PREFIX, ctx.command.usage))
  bot.run(TOKEN)
