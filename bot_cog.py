import discord
from discord.ext import commands
from get_tts import get_etts
from get_tts import get_gtts
import get_vits


class BotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tts_settings = {}
        self.tts_channels = {}

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
            await ctx.send("음성 채널에 접속했습니다.")
        else:
            await ctx.send("먼저 음성 채널에 접속해 주세요.")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("음성 채널에서 나갔습니다.")
        else:
            await ctx.send("음성 채널에 접속해 있지 않습니다.")

    @commands.command()
    async def set(self, ctx, tts_type):
        if tts_type not in ['google', 'edge', 'milk']:
            await ctx.send("TTS 유형이 잘못되었습니다. 'google', 'edge', 'milk' 중에서 선택하세요.")
            return

        self.tts_settings[ctx.channel.id] = tts_type
        await ctx.send(f"이 채널의 TTS 유형이 설정되었습니다. {tts_type}.")

    @commands.command()
    async def setCH(self, ctx):
        self.tts_channels[ctx.guild.id] = ctx.channel.id
        await ctx.send(f"이 서버의 TTS 채널이 설정되었습니다. {ctx.channel.name}.")

    @commands.command()
    async def tts(self, ctx, *, message):
        if ctx.channel.id not in self.tts_settings:
            self.tts_settings[ctx.channel.id] = 'edge'

        tts_type = self.tts_settings[ctx.channel.id]
        if tts_type == 'google':
            get_gtts(message, ctx.channel.id)
        elif tts_type == 'edge':
            await get_etts(message, ctx.channel.id)
        elif tts_type == 'milk':
            get_vits.tts_fn = get_vits.create_tts_fn(get_vits.net_g, get_vits.hps, get_vits.speaker_ids)
            get_vits.tts_fn(message, "Milk", 1.0, "한국어", ctx.channel.id)
        source = discord.FFmpegPCMAudio(f"output/{ctx.channel.id}_output.wav")
        ctx.voice_client.play(source)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.startswith(self.bot.command_prefix):
            return
        if message.channel.id == self.tts_channels.get(message.guild.id):
            ctx = await self.bot.get_context(message)
            await self.tts(ctx, message=message.content)


async def setup(bot):
    await bot.add_cog(BotCog(bot))
