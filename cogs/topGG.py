import asyncio
import datetime
import logging
import os

import dbl
import discord
from discord.ext import commands

logger = logging.getLogger("lyvego")


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ["DBL_TOKEN"] # set this to your DBL token
        # try:
        # self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/webhook', webhook_auth='mE5iPShY2qrymFGeV2MD', webhook_port=5000) # Autopost will post your guild count every 30 minutes
        # except Exception as e:
        #     logger.exception(e, exc_info=True)
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        while True:
            try:
                await self.dblpy.post_guild_count(shard_count=self.bot.shard_count)
            except Exception as e:
                logger.exception(e, exc_info=True)
            await asyncio.sleep(1800)

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print(data)
        user = self.bot.get_user(int(data['user']))
        await user.send("tested")

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        try:
            user = self.bot.get_user(int(data['user']))
            logger.info("voted")
            embed = discord.Embed(
                title="TOP.GG upvote",
                description="Your vote has been register! Thank you❤️! You can vote again in 12 hours on the same [link](https://top.gg/bot/702648685263323187/vote).\nIf you have any question come over my [discord server](https://discord.gg/E4nVPd2)",
                timestamp=datetime.datetime.utcnow(),
                color=utils.COLOR
            )
            embed.set_thumbnail(url="https://top.gg/images/dblnew.png")
            embed.set_footer(
                text="Made by Taki#0853 (WIP)",
                icon_url=user.avatar_url
            )
            await user.send(embed=embed)
        except Exception as e:
            logger.exception(e, exc_info=True)


def setup(bot):
    bot.add_cog(TopGG(bot))
