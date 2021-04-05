import discord
import wavelink
from discord.ext import commands
from enum import Enum
import datetime as dt
import random
import typing as t
#import re
import asyncio
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}

class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0


"""class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            await ctx.send(f"Added {tracks[0].title} to the queue.")
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)
                await ctx.send(f"Added {track.title} to the queue.")

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)"""

class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f" Wavelink node `{node.identifier}` ready.")

    """@wavelink.WavelinkMixin.listener(event="on_track_stuck")            #
    @wavelink.WavelinkMixin.listener(event="on_track_end")              #
    @wavelink.WavelinkMixin.listener(event="on_track_exception")        #
    async def on_player_stop(self, node, payload):                      #
        if payload.player.queue.repeat_mode == RepeatMode.ONE:          #
            await payload.player.repeat_track()                         #
        else:                                                           #
            await payload.player.advance()                              #"""

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                              port=2333,
                                              rest_uri='http://127.0.0.1:2333',
                                              password='youshallnotpass',
                                              identifier='TEST',
                                              region='europe')

    """def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)"""

    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await player.connect(channel.id)

    @commands.command()
    async def play(self, ctx, *, query: str):
        async with ctx.typing():
            tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')
            if not tracks:
                tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')
            if not tracks:
                tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')
            if not tracks:
                return await ctx.send('Could not find any songs with that query.')
            # try three times to get tracks

            player = self.bot.wavelink.get_player(ctx.guild.id)
            if not player.is_connected:
                await ctx.invoke(self.connect_)
                await asyncio.sleep(1)

            track = tracks[0]
            player.ctx = ctx
            seconds = track.length // 1000
            minutes = seconds // 60
            seconds = seconds % 60
            if len(str(seconds)) == 1:
                seconds = f"0{seconds}"
            time = f"{minutes}:{seconds}"

            try:
                playertracks = player.tracks
            except:
                player.tracks = []
            track = {
                "Track": track,
                "Title": track.title,
                "Length": track.length,
                "Thumb": track.thumb,
                "Author": track.author,
                "Request": ctx.author,
                "Time": time
            }

            player.tracks.append(track)
            if player.tracks[0] == track:
                await player.play(track["Track"])
                tracks.pop(0)
                await ctx.invoke(self.np)
            else:
                await ctx.send(f"{track['Title']} added to queue.")

    @commands.command(name="disconnect", aliases=["leave"])
    async def disconnect_command(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.destroy()
        await ctx.send("Disconnect.")

    @commands.command()
    async def queue(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        embed = discord.Embed(title=f"Queue for {str(ctx.guild)}", color=0xEE8700)
        for track in player.tracks:
            embed.add_field(name=track["Title"], value=f"{track['Time']} | {track['Request'].mention}")

        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        track = player.tracks[0]
        if ctx.author == track["Request"]:
            await player.stop()
        else:
            await ctx.send("Only the person who requested the track can skip it.")

    @commands.command()
    async def resume(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.start_playback()

    @commands.command()
    async def seek(self, ctx, position):
        stamp = position
        try:
            position = int(position)
        except:
            split = position.split(":")
            if len(split) != 2:
                return await ctx.send("Please give either seconds or minutes:seconds.")
            seconds = int(split[0]) * 60
            seconds += int(split[1])
            position = seconds

        position = position * 1000
        player = self.bot.wavelink.get_player(ctx.guild.id)
        track = player.tracks[0]
        if track["Request"] != ctx.author:
            return await ctx.send("Only the person who requested the track can seek through it.")

        if position > track["Length"]:
            return await ctx.send("You entered a seek time longer than the track duration.")

        await player.seek(position)
        await ctx.send(f"Seeked to {stamp}.")

    async def on_lavalink_event(self, event):
        if isinstance(event, wavelink.events.TrackEnd):
            player = event.player

            player.tracks.pop(0)
            if player.tracks != []:
                await player.play(player.tracks[0]["Track"])
                await self.np(player.ctx)


    @commands.command()
    async def np(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        try:
            np = player.tracks[0]
        except:
            return await ctx.send("Nothing is playing right now.")

        if np is None:
            return await ctx.send("Nothing is playing right now.")

        time = int(player.position) // 1000
        minutes = time // 60
        seconds = time % 60
        if len(str(seconds)) == 1:
            seconds = f"0{seconds}"
        position = f"{minutes}:{seconds}"

        embed = discord.Embed(title=np["Title"], color=0xEE8700)
        embed.set_thumbnail(url=np["Thumb"])

        embed.add_field(name="Duration", value=np["Time"])
        embed.add_field(name="Position", value=position)
        embed.add_field(name="Channel", value=np["Author"])
        embed.add_field(name="Requested by", value=np["Request"].mention)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))