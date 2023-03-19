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

@bot.slash_command(name="get_started", description="This is the start of your coding career.")
async def get_started(ctx):
    options = [
        disnake.ui.Button(label="Python", custom_id="python"),
        disnake.ui.Button(label="HTML", custom_id="html"),
        disnake.ui.Button(label="CSS", custom_id="css"),
        disnake.ui.Button(label="JavaScript", custom_id="javascript"),
    ]
    embed = disnake.Embed(title="Select a language to learn", description="Choose a language you'd like to learn!", color=0x00ff00)
    view = disnake.ui.View()
    view.add_item(disnake.ui.Button(label="Cancel", custom_id="cancel", style=disnake.ui.ButtonStyle.danger))
    view.add_item(*options) # Use * operator to unpack the list
    message = await ctx.send(embed=embed, view=view)

    def check(interaction: disnake.Interaction):
        return interaction.message.id == message.id and interaction.user.id == ctx.author.id

    try:
        interaction = await bot.wait_for("button_click", timeout=60.0, check=check)
    except asyncio.TimeoutError:
        return await message.edit(embed=disnake.Embed(title="Timed out", description="You took too long to respond!", color=0xff0000), view=None)

    if interaction.custom_id == "cancel":
        return await message.edit(embed=disnake.Embed(title="Canceled", description="You canceled the command.", color=0xff0000), view=None)

    if interaction.custom_id == "python":
        tutorial = "Python tutorial goes here!"
    elif interaction.custom_id == "html":
        tutorial = "HTML tutorial goes here!"
    elif interaction.custom_id == "css":
        tutorial = "CSS tutorial goes here!"
    elif interaction.custom_id == "javascript":
        tutorial = "JavaScript tutorial goes here!"
    else:
        return await message.edit(embed=disnake.Embed(title="Invalid option", description="You selected an invalid option.", color=0xff0000), view=None)

    embed = disnake.Embed(title="Tutorial", description=tutorial, color=0x00ff00)
    await message.edit(embed=embed, view=None)

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
