import os
from disnake.ext import commands
import disnake
import asyncio

intents = disnake.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

GUILD_ID = 1043647302272827412
LOG_CHANNEL_ID = 1050550574652858429
async def get_log_channel(guild):
    return guild.get_channel(LOG_CHANNEL_ID)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\n------")

@bot.slash_command(name="help", description="Displays a list of available commands.")
async def help(ctx):
    embed = disnake.Embed(title="Available Commands", color=0xD3D3D3)
    for command in bot.slash_commands:
        embed.add_field(name=f"/{command.name}", value=command.description, inline=False)
    await ctx.send(embed=embed)
    guild = bot.get_guild(GUILD_ID)
    log_channel = await get_log_channel(guild)
    embed = disnake.Embed(title="Command Executed", color=0xD3D3D3)
    embed.add_field(name="User", value=f"{ctx.author.name}#{ctx.author.discriminator} (<@{ctx.user.id}>)")
    embed.add_field(name="Command", value="/help")
    
    await log_channel.send(embed=embed)

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
