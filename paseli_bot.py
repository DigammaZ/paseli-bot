import discord
from discord.ext.commands import Bot

from discord_credentials import TOKEN
from constants import PREFIX

from cogs.paseli import Paseli
from cogs.japan import Japan
from cogs.sdvx import Sdvx
from cogs.remind import Remind
from cogs.roles import Roles
from cogs.misc import Miscellaneous

cogs = [Paseli, Japan, Sdvx, Remind, Roles, Miscellaneous]


class PaseliBot(Bot):
  def __init__(self):
    super().__init__(command_prefix=PREFIX, description='Paseli Bot for 2MF.')

  async def on_ready(self):
    print('Logged in as {0.user.name}'.format(self))
    Roles.cache_roles()

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
