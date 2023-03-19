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

@bot.slash_command(name="help", description="Displays a list of available commands.")
async def help(ctx):
    embed = disnake.Embed(title="Available Commands", color=0xD3D3D3)
    for command in bot.slash_commands:
        embed.add_field(name=f"/{command.name}", value=command.description, inline=False)
    await ctx.send(embed=embed)
    
@bot.slash_command(name="get_started", description="This is the start of your coding career.")
async def get_started(ctx):
    embed = disnake.Embed(title="Welcome to Coding 101!", description="Are you ready to get started with your coding journey?", color=0x00ff00)
    embed.set_footer(text="Step 1 of 3")
    message = await ctx.send(embed=embed, components=[disnake.ui.Button(label="Next Step", custom_id="next_step")])
    
    def check(interaction):
        return interaction.message.id == message.id and interaction.user.id == ctx.author.id
    
    try:
        interaction = await bot.wait_for("button_click", timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await message.edit(components=[disnake.ui.Button(label="Next Step (Timed Out)", disabled=True)])
    else:
        embed.description = "Great! The first step in your coding journey is to learn a programming language. Which language would you like to start with?"
        embed.set_footer(text="Step 2 of 3")
        await interaction.response.edit_message(embed=embed, components=[disnake.ui.Button(label="Next Step", custom_id="next_step")])
        
        try:
            interaction = await bot.wait_for("button_click", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await message.edit(components=[disnake.ui.Button(label="Next Step (Timed Out)", disabled=True)])
        else:
            embed.description = "Excellent choice! Now it's time to start learning the basics of programming. There are many great resources out there, so take your time and find what works best for you."
            embed.set_footer(text="Step 3 of 3")
            await interaction.response.edit_message(embed=embed, components=[disnake.ui.Button(label="Finish", custom_id="finish")])
            
            try:
                interaction = await bot.wait_for("button_click", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await message.edit(components=[disnake.ui.Button(label="Finish (Timed Out)", disabled=True)])
            else:
                await interaction.response.edit_message(content="Congratulations! You've completed your first coding lesson. Happy coding!")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
