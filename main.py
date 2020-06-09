import asyncio
import atexit
import json
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

from src.constants import HOST, PASSWORD, PORT, TOKEN, USER
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



class Lyvego(commands.AutoShardedBot, Pool):
    def __init__(self, *args, loop=None, **kwargs):
        super().__init__(
            command_prefix=self._get_prefix,
            activity=discord.Game(
                name="Starting..."
            ),
            status=discord.Status.dnd
        )
        super(Pool, self).__init__()
        self.http_session = None
        self.pool = None
        self.red = 0xde1616
        self.green = 0x17ad3f
        self.blue = 0x158ed4
        self.color = 0x6441a5
        self.color_str = str(hex(self.color))[2:]
        self.locales = self.init_locales()
        self.lyvego_url = "https://lyvego.com"
        self.remove_command("help")
        self.loader()

    async def _get_prefix(self, bot, message):
        prefix = await self.getg_prefix(message.guild.id)
        return when_mentioned_or(prefix)(bot, message)

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
        if str(ctx.command) in ("help"):
            return
        if isinstance(error, commands.CommandOnCooldown):
            try:
                await ctx.message.add_reaction("<a:loading:709745917343039530>")
            except:
                pass
            lang = await self.getg_lang(ctx.guild.id)
            await ctx.send(self.bot.locales[lang]["error_ratelimited"].format(ctx.author.mention, error.retry_after))
        else:
            try:
                await ctx.message.add_reaction("<a:wrong_checkmark:709737435889664112>")
            except:
                pass
            try:
                await ctx.send(error.original)
            except AttributeError:
                await ctx.send(error)

    @staticmethod
    def _value_exist(L, v):
        try:
            return isinstance(L.index(v), int)
        except ValueError:
            return False

    async def _verify_servers(self):
        servers = await self.get_guilds_registered()
        bot_guilds_ids = []
        for bguild in self.guilds:
            bot_guilds_ids.append(str(bguild.id))
            if not self._value_exist(servers, str(bguild.id)):
                try:
                    await self.http_session.request(
                        method="POST",
                        url="https://api.lyvego.com/v1/bot/server",
                        headers={"Authorization": AUTHORIZATION},
                        json={
                            "discord_id": bguild.id,
                            "owner_id": bguild.owner_id,
                            "name": bguild.name,
                            "icon": bguild.icon_url._url,
                            "region": bguild.region.name
                        }
                    )
                    logger.info(f"{bguild.id} added by verifier")
                except:
                    pass
        for bdsid in servers:
            if not self._value_exist(bot_guilds_ids, bdsid):
                try:
                    await self.http_session.request(
                        method="DELETE",
                        url=f"https://api.lyvego.com/v1/bot/server/{bdsid}",
                        headers={"Authorization": AUTHORIZATION}
                    )
                    logger.info(f"{bdsid} removed by verifier")
                except:
                    pass

    def init_locales(self):
        locales = {}
        for file in os.listdir("locales/"):
            with open(f"locales/{file}", "r") as f:
                locales[file[:2]] = json.load(f)
        return locales

    async def on_ready(self):
        if self.http_session is None:
            # Create http session
            self.http_session = ClientSession()

        try:
            # Create pool
            if self.pool is None:
                try:
                    self.pool = await aiomysql.create_pool(
                            host=HOST,
                            port=PORT,
                            user=USER,
                            password=PASSWORD,
                            db=USER,
                            loop=self.loop,
                            maxsize=20,
                            autocommit=True
                        )
                    await self._verify_servers()
                    logger.info("Guilds verified")
                except Exception as e:
                    logger.exception(e, exc_info=True)

        except Exception as e:
            logger.exception(e, exc_info=True)

        await self.change_presence(
            activity=discord.Activity(
                name="!!help | lyvego.com",
                type=discord.ActivityType.watching
            )
        )
        logger.info("Lyvego ready")

    def _exit(self):
        try:
            self._close()
            logger.info("Pool closed")
        except Exception as e:
            logger.exception(e, exc_info=True)
            sys.exit(1)
        finally:
            logger.info("Lyvego has been shutted down")
            sys.exit(0)

    def run(self, token, *args, **kwargs):
        try:
            super().run(token, *args, **kwargs)
        except KeyboardInterrupt:
            self._exit()


if __name__ == "__main__":
    bot = Lyvego()
    bot.run(TOKEN, reconnect=True)
