import asyncio
import atexit
import logging
import os
import sys
import time
from typing import Optional

import discord
from aiohttp import ClientSession
from discord.ext import commands
from discord.ext.commands import when_mentioned_or

from src.db import Pool

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


class Lyvego(commands.AutoShardedBot, Pool):
    def __init__(self, *args, loop=None, **kwargs):
        super().__init__(
            command_prefix="!",
            activity=discord.Game(
                name="Starting..."
            ),
            status=discord.Status.dnd
        )
        super(Pool, self).__init__()
        self.http_session = None
        self._pool_created = False
        self.connected = False
        self.pool = None
        self.color = 0x6441a5
        self.color_str = str(hex(self.color))[2:]
        self.red = 0xde1616
        self.green = 0x17ad3f
        self.blue = 0x158ed4
        self.pool_loop = asyncio.get_event_loop()
        self.remove_command("help")
        self.loader()


    def loader(self, reloading: Optional[bool]=False):
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
        await self.wait_until_ready()
        r = await self.http_session.request(
            method="POST",
            url="https://api.lyvego.com/v1/bot/server",
            json={
                "discord_id": guild.id,
                "owner_id": guild.owner_id,
                "name": guild.name,
                "icon": guild.icon_url._url,
                "region": guild.region.name
            }
        )
        print("new guild")

    async def on_guild_remove(self, guild: discord.Guild):
        await self.wait_until_ready()
        r = await self.http_session.request(
            method="DELETE",
            url=f"https://api.lyvego.com/v1/bot/server/{guild.id}",
        )
        print(f"{guild.name} removed")

    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('{} This command is ratelimited, please try again in {:.2f}s'.format(ctx.author.mention, error.retry_after))
        else:
            await ctx.send(error)
            raise error

    async def on_ready(self):
        if self.http_session is None:
            self.http_session = ClientSession()
        if self.pool is None:
            await self.main()
        await self.wait_until_ready()
        print(self.pool_loop)


        await self.change_presence(
            activity=discord.Activity(
                name=f"lyvego.com | [!help]",
                type=discord.ActivityType.watching
            )
        )

    def _exiting(self):
        print("dsq")
        try:
            self.logout()
            self.close()
            logger.info("Logout")
        except Exception as e:
            logger.exception(e, exc_info=True)
        finally:
            logger.info("Lyvego has been shutted down")
            sys.exit(0)

    def run(self, token, *args, **kwargs):
        # atexit.register(self._exiting)
        super().run(token, *args, **kwargs)



if __name__ == "__main__":
    bot = Lyvego()
    bot.run(os.environ["TOKEN"], reconnect=True)
# logger = logging
