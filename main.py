import asyncio
import json
import logging
import sys
from datetime import datetime
from typing import Optional

import aiomysql
import discord
from aiohttp import ClientSession
from discord.ext import commands
from discord.ext.commands import when_mentioned_or

from src.constants import *
from src.db import Pool
from src.utils import dctt

MAX_RETRIES = 10

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
    __slots__ = (
        "intents",
        "http_session",
        "pool",
        "red",
        "green",
        "blue",
        "color",
        "color_str",
        "locales",
        "lyvego_url",
        "start_time",
        "_debug"
    )

    def __init__(self, *args, **kwargs):
        self.intents = discord.Intents(members=True, presences=True)
        self._debug = kwargs.get("debug", False)
        super().__init__(
            command_prefix=self._get_prefix,
            case_insensitive=True,
            activity=discord.Game(
                name="Starting..."
            ),
            status=discord.Status.dnd,
            intents=self.intents
        )
        super(Pool, self).__init__()
        self.http_session = None
        self.pool = None
        self.red = 0xde1616
        self.green = 0x17ad3f
        self.blue = 0x158ed4
        self.color = 0x6441a5
        self.color_str = str(hex(self.color))[2:]
        self.start_time = datetime.utcnow()
        self.locales = {}
        self.lyvego_url = "https://lyvego.com"
        self.load_locales()
        self.remove_command("help")
        self.load_cogs()

    async def _get_prefix(self, bot, message):
        try:
            prefix = await self.getg_prefix(message.guild.id)
        except:
            prefix = "!!"
        return when_mentioned_or(prefix)(bot, message)

    def load_cogs(self, reloading: Optional[bool] = False):
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
            acc = 0
            backoff_time = 2
            r = await self.http_session.request(
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
            while r.status not in range(200, 300) and acc < MAX_RETRIES:
                r = await self.http_session.request(
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
                await asyncio.sleep(backoff_time)
                backoff_time *= 1.12
                acc += 1
        except:
            print(f"{guild.name} cannot be added to the DB", file=sys.stderr)

        chan_logger = self.get_channel(739633667906732143)
        embed = discord.Embed(
            title="Bot added to " + guild.name,
            timestamp=dctt(),
            color=self.color
        )
        embed.add_field(
            name="<:users:693053423494365214> Members",
            value=len(guild.members)
        )
        embed.add_field(
            name="<:hashtag:693056105076621342> Channels",
            value=len(guild.channels)
        )
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(icon_url=guild.me.avatar_url)
        await chan_logger.send(embed=embed)

    async def on_guild_remove(self, guild: discord.Guild):
        try:
            await self.http_session.request(
                method="DELETE",
                url=f"{API_ROOT}bot/server/{guild.id}",
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
            await ctx.send(self.locales[lang]["error_ratelimited"].format(ctx.author.mention, error.retry_after))
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
        acc_removed = 0
        acc_added = 0
        for bguild in self.guilds:
            bot_guilds_ids.append(str(bguild.id))
            if not self._value_exist(servers, str(bguild.id)):
                try:
                    acc_added += 1
                    await self.http_session.request(
                        method="POST",
                        url=f"{API_ROOT}bot/server",
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
                    await asyncio.sleep(.4)
                except Exception as e:
                    logger.exception(e, exc_info=True)
        for bdsid in servers:
            if not self._value_exist(bot_guilds_ids, bdsid):
                try:
                    acc_removed += 1
                    # await self.http_session.request(
                    #     method="DELETE",
                    #     url=f"{API_ROOT}bot/server/{bdsid}",
                    #     headers={"Authorization": AUTHORIZATION}
                    # )
                    # logger.info(f"{bdsid} removed by verifier")
                except Exception as e:
                    logger.exception(e, exc_info=True)
        await asyncio.sleep(1)
        logger.info(
            f"{acc_removed} / {len(self.guilds)} should be REMOVED and {acc_added} / {len(self.guilds)} should be ADDED")

    def load_locales(self):
        for file in os.listdir("locales/"):
            with open(f"locales/{file}", "r") as f:
                self.locales[file[:2]] = json.load(f)

    async def update_role(self, member: discord.Member, is_adding):
        role_name = await self.get_server_role_activity(member.guild.id)
        role = discord.utils.get(member.guild.roles, name=role_name)
        if role != None:
            if is_adding:
                await member.add_roles(role, reason=self.locales["activity_start_streaming"])
            else:
                await member.remove_roles(role, reason=self.locales["activity_stop_streaming"])

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        print(before.name, before.activities, after.activities, sep="\n")
        if discord.ActivityType.streaming is after.activity and before.activity is not after.activity:
            await self.update_role(after, True)
        elif discord.ActivityType.streaming is before.activity and before.activity is not after.activity:
            await self.update_role(after, False)

    async def startup_tasks(self):
        if self.http_session is None:
            # Create http session
            self.http_session = ClientSession(loop=self.loop)
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
                        autocommit=True
                    )
                    # TODO : make more secure way to verify guilds
                    # self.loop.create_task(self._verify_servers())
                    logger.info("Pool created")
                except Exception as e:
                    logger.exception(e, exc_info=True)

        except Exception as e:
            logger.exception(e, exc_info=True)

    async def on_ready(self):
        await self.startup_tasks()
        await self.change_presence(
            activity=discord.Activity(
                name="!!help | lyvego.com",
                type=discord.ActivityType.watching
            )
        )
        logger.info("Lyvego ready")

    def _exit(self):
        try:
            self.loop.run_until_complete(self._close())
            logger.info("Pool closed")
        except Exception as e:
            logger.exception(e, exc_info=True)
            sys.exit(1)
        finally:
            logger.info("Lyvego has been shutted down")
            sys.exit(0)

    def run(self, *args, **kwargs):
        try:
            super().run(TOKEN if not self._debug else TOKEN_DEBUG, *args, **kwargs)
        except KeyboardInterrupt:
            self._exit()

    # async def run(self, token, *args, **kwargs):
    #     try:
    #         await self.start(token, *args, **kwargs)
    #     except KeyboardInterrupt:
    #         self._exit()


def multi_tokens_runner(loop: asyncio.AbstractEventLoop, bot: Lyvego, *tokens):
    for token in tokens:
        loop.create_task(bot.run(token, reconnect=True))
        logger.info(f"BOT {token} is now running")


if __name__ == "__main__":
    try:
        # Debugger
        import sentry_sdk
        from sentry_sdk.integrations.aiohttp import AioHttpIntegration

        sentry_sdk.init(
            SENTRY_TOKEN,
            traces_sample_rate=1.0,
            integrations=[AioHttpIntegration()]
        )
    except Exception as e:
        logger.exception(e, exc_info=True)
    bot = Lyvego(debug=True)
    bot.run(reconnect=True)
