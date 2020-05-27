import asyncio
import atexit
import logging
import os
import sys
import time
from typing import Optional

import aiomysql
import discord
from aiohttp import ClientSession
from discord.ext import commands
from discord.ext.commands import when_mentioned_or

from src.db import Pool
from src.utils import AUTHORIZATION


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

HOST = os.environ["HOST"]
PORT = 3306
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]

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
        self.pool = None
        self.color = 0x6441a5
        self.color_str = str(hex(self.color))[2:]
        self.red = 0xde1616
        self.green = 0x17ad3f
        self.blue = 0x158ed4
        self.lyvego_url = "https://lyvego.com"
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
        try:
            await self.http_session.request(
                method="POST",
                url="https://api.lyvego.com/v1/bot/server",
                headers={"Authorization": AUTHORIZATION},
                json={
                    "discord_id": guild.id,
                    "owner_id": guild.owner_id,
                    "name": guild.name,
                    "icon": guild.icon_url._url,
                    "region": guild.region.name
                }
            )
        except Exception as e:
            logger.exception(e, exc_info=True)

    async def on_guild_remove(self, guild: discord.Guild):
        try:
            await self.http_session.request(
                method="DELETE",
                url=f"https://api.lyvego.com/v1/bot/server/{guild.id}",
                headers={"Authorization": AUTHORIZATION}
            )
        except Exception as e:
            logger.exception(e, exc_info=True)

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            try:
                await ctx.message.add_reaction("<a:loading:709745917343039530>")
            except:
                pass
            await ctx.send('{} This command is ratelimited, please try again in {:.2f}s'.format(ctx.author.mention, error.retry_after))
        else:
            try:
                await ctx.message.add_reaction("<a:wrong_checkmark:709737435889664112>")
            except:
                pass
            try:
                await ctx.send(error.original)
            except AttributeError:
                await ctx.send(error)

    async def on_ready(self):
        # Create http session
        if self.http_session is None:
            self.http_session = ClientSession()
        # Create pool
        if self.pool is None:
            self.pool = await aiomysql.create_pool(
                    host=HOST,
                    port=PORT,
                    user=USER,
                    password=PASSWORD,
                    db=USER,
                    loop=self.loop,
                    maxsize=30
                )
            logger.info("pool created")
        logger.info("bot ready")

        await self.change_presence(
            activity=discord.Activity(
                name="!help | lyvego.com",
                type=discord.ActivityType.watching
            )
        )

    def _exiting(self):
        try:
            self._close()
            logger.info("pool closed")
        except Exception as e:
            logger.exception(e, exc_info=True)
            sys.exit(1)
        finally:
            logger.info("Lyvego has been shutted down")
            sys.exit(0)

    def run(self, token, *args, **kwargs):
        atexit.register(self._exiting)
        super().run(token, *args, **kwargs)


if __name__ == "__main__":
    bot = Lyvego()
    bot.run(os.environ["TOKEN"], reconnect=True)
