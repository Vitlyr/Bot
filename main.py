import os
from disnake.ext import commands
import disnake
import asyncio

intents = disnake.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\n------")
    
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.slash_command(name="request", description="Request a song to be played.")
    async def request_song(self, ctx: commands.SlashContext, song_link: str):
        # Add the requested song to the queue
        self.queue.append(song_link)

        # Send a confirmation message with the song information
        embed = disnake.Embed(title="Song Requested", color=0xD3D3D3)
        embed.add_field(name="Song Link", value=song_link, inline=False)
        embed.add_field(name="Queue Position", value=len(self.queue), inline=False)
        await ctx.send(embed=embed)

        # Check if the bot is already playing music, if not, start playing the first song in the queue
        if not self.bot.voice_clients:
            await self.play_song(ctx)

    async def play_song(self, ctx: commands.SlashContext):
        # Connect to the voice channel
        channel = ctx.author.voice.channel
        voice = await channel.connect()

        # Start playing the first song in the queue
        song_link = self.queue.pop(0)
        source = await disnake.FFmpegOpusAudio.from_probe(song_link, **FFMPEG_OPTIONS)
        voice.play(source)

        # Send a message indicating that the song is playing
        embed = disnake.Embed(title="Now Playing", color=0xD3D3D3)
        embed.add_field(name="Song Link", value=song_link, inline=False)
        await ctx.send(embed=embed)

        # Wait for the song to finish playing and disconnect from the voice channel
        while voice.is_playing():
            await asyncio.sleep(1)
        await voice.disconnect()

        # Check if there are any songs remaining in the queue, if so, play the next one
        if self.queue:
            await self.play_song(ctx)

bot.add_cog(Music(bot))


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
