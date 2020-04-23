import asyncio
import logging
import os
import time
import signal

import discord
from aiohttp import ClientSession
from discord.ext import commands
from discord.ext.commands import when_mentioned_or


logger = logging.getLogger("lyvego")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
        filename='lyvego.log',
        encoding='utf-8',
        mode='w'
    )
handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
        )
    )
logger.addHandler(handler)


class Lyvego(commands.AutoShardedBot):
    def __init__(self, *args, loop=None, **kwargs):
        super().__init__(
            command_prefix="!",
            activity=discord.Game(
                name="Starting..."
            ),
            status=discord.Status.dnd
        )
        self.remove_command("help")
        self.loader()
        self.http_session = None

    def loader(self, reloading: bool=False):
        for file in os.listdir("cogs/"):
            try:
                if file.endswith(".py"):
                    if reloading:
                        self.reload_extension(f'cogs.{file[:-3]}')
                    else:
                        self.load_extension(f'cogs.{file[:-3]}')
                    logger.info(f"{file} loaded")
            except Exception:
                logger.exception(f"Fail to load {file}")

    async def on_guild_join(self, guild: discord.Guild):
        pass # TODO: request API

    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('{} This command is ratelimited, please try again in {:.2f}s'.format(ctx.author.mention, error.retry_after))
        else:
            raise error

    async def on_command(self, ctx: commands.Context):
        print(ctx.author)

    async def on_ready(self):
        if self.http_session is None:
            self.http_session = ClientSession()
        await self.wait_until_ready()
        while not self.is_closed():
            await self.change_presence(
                activity=discord.Game(
                    name=f"[!help] | Waiting alerts from {len(self.guilds)} servers"
                )
            )
            await asyncio.sleep(60)

    async def sig_handler(self, sig, _):
        print("dsq")
        try:
            await self.http_session.close()
            logger.info("Closing http session")
        except Exception as e:
            logger.exception(e, exc_info=True)
        finally:
            logger.info("Lyvego has been shutted down")

    def run(self, token, *args, **kwargs):
        signal.signal(signal.SIGINT, self.sig_handler)
        super().run(token, *args, **kwargs)
        logger.info("qsd")



if __name__ == "__main__":
    bot = Lyvego()
    bot.run(os.environ["TOKEN"], reconnect=True)
# logger = logging
