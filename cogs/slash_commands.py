
from discord.ext import commands
from discord_slash import SlashContext, cog_ext, manage_commands

import src.commands as bot_commands
from main import Lyvego


class SlashCommands(commands.Cog):
    """Implentation of basic commands as slash commands"""
    __slots__ = ("bot")

    def __init__(self, bot: Lyvego):
        self.bot: Lyvego = bot

    @cog_ext.cog_slash(
        name="follow",
        description="Add follow event about a streamer"
    )
    async def _follow(self, ctx: SlashContext, streamer, message=""):
        await bot_commands.add_follow_command(self.bot, ctx, streamer, message)

    @cog_ext.cog_slash(
        name="clips",
        description="Add clips event about a streamer"
    )
    async def _clips(self, ctx: SlashContext, streamer):
        await bot_commands.add_clip_command(self.bot, ctx, streamer)

    @cog_ext.cog_slash(
        name="stream",
        description="Add stream event about a streamer"
    )
    async def _stream(self, ctx: SlashContext, streamer, message=""):
        await bot_commands.add_streamer_command(self.bot, ctx, streamer, message)

    @cog_ext.cog_slash(
        name="remove",
        description="Remove event notification",
        options=[
            manage_commands.create_option(
                name="event",
                description="Event type",
                option_type=3,
                required=True,
                choices=[
                     manage_commands.create_choice(
                        name="Stream event",
                        value="stream"
                     ),
                    manage_commands.create_choice(
                        name="Follow event",
                        value="follow"
                     ),
                    manage_commands.create_choice(
                        name="Clips event",
                        value="clips"
                     )
                ]
            ),
            manage_commands.create_option(
                name="streamer",
                description="Streamer name",
                option_type=3,
                required=True
            )
        ]
    )
    async def _remove(self, ctx: SlashContext, event, streamer):
        await bot_commands.remove_event_command(self.bot, ctx, event, streamer)

    @cog_ext.cog_slash(
        name="help",
        description="Show information about the bot"
    )
    async def _help(self, ctx: SlashContext):
        await bot_commands.help_command(self.bot, ctx)

    @cog_ext.cog_slash(
        name="vote",
        description="Get link to vote for the bot"
    )
    async def _vote(self, ctx: SlashContext):
        await bot_commands.vote_command(self.bot, ctx)

    @cog_ext.cog_slash(
        name="invite",
        description="Get link to invite the bot"
    )
    async def _invite(self, ctx: SlashContext):
        await bot_commands.invite_command(self.bot, ctx)


def setup(bot):
    bot.add_cog(SlashCommands(bot))
