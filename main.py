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
        disnake.SelectOption(label="Python", value="python"),
        disnake.SelectOption(label="HTML", value="html"),
        disnake.SelectOption(label="CSS", value="css"),
        disnake.SelectOption(label="JavaScript", value="javascript"),
    ]
    select = disnake.ui.Select(
        placeholder="Select a language to learn",
        options=options,
        min_values=1,
        max_values=1
    )
    view = disnake.ui.View()
    view.add_item(select)
    view.add_item(disnake.ui.Button(label="Cancel", custom_id="cancel", style=disnake.ButtonStyle.danger))

    message = await ctx.send("Choose a language you'd like to learn!", view=view)

    def check(interaction: disnake.Interaction):
        return interaction.message.id == message.id and interaction.author.id == ctx.author.id

    try:
        interaction = await bot.wait_for("select_option", timeout=60.0, check=check)
    except asyncio.TimeoutError:
        return await message.edit(content="You took too long to respond!", view=None)

    if interaction.custom_id == "cancel":
        return await message.edit(content="You canceled the command.", view=None)

    tutorial = ""
    for value in interaction.values:
        if value == "python":
            tutorial += "Python tutorial goes here!\n"
        elif value == "html":
            tutorial += "HTML tutorial goes here!\n"
        elif value == "css":
            tutorial += "CSS tutorial goes here!\n"
        elif value == "javascript":
            tutorial += "JavaScript tutorial goes here!\n"

    if not tutorial:
        return await message.edit(content="You didn't select a valid option.", view=None)
    if message.view is not None:
        await message.edit(content="You took too long to respond!", view=None)
        
    await message.edit(content=tutorial, view=None)

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
