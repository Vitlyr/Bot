import os
from disnake.ext import commands
import disnake
import asyncio

intents = disnake.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

@bot.command(name="hello", description="Sends a warm welcome message.")
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command(name="info", description="Displays some information about the bot.")
async def info(ctx):
    embed = disnake.Embed(title='Bot Information', color=0x3498db)
    embed.add_field(name='Version', value='1.0.0')
    await ctx.send(embed=embed)

@bot.command(name="ping", description="Pong!")
async def ping(ctx):
    latency = bot.latency * 1000
    embed = disnake.Embed(title='Pong!', description=f'My latency is {latency:.2f}ms', color=0x2ecc71)
    await ctx.send(embed=embed)

@bot.command(name="help", description="Shows all the available commands.")
async def help(ctx):
    embed = disnake.Embed(title='Bot Commands', color=0xf1c40f)
    embed.add_field(name='!hello', value='Says hello', inline=False)
    embed.add_field(name='!info', value='Displays bot information', inline=False)
    embed.add_field(name='!ping', value='Displays bot latency', inline=False)
    embed.add_field(name='!help', value='Displays this message', inline=False)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
