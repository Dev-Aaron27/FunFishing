import discord
from discord.ext import commands
import datetime
import psutil
import platform
import os
import sys
import random

# Setup bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Store bot's start time and recent message history for snipe
bot.start_time = datetime.datetime.utcnow()
bot.sniped_messages = {}


# Event that runs when the bot is ready
@bot.event
async def on_ready():
    # Get bot info
    bot_name = bot.user.name
    bot_id = bot.user.id
    bot_ping = round(bot.latency * 1000)  # Latency in milliseconds
    bot_status = str(bot.status).replace(
        "Status.", "")  # Get the bot's current status (e.g., "online")

    # Get system information
    python_version = platform.python_version()
    process = psutil.Process()
    memory_usage = process.memory_info(
    ).rss / 1024 / 1024  # Memory usage in MB

    # Print to console
    print(f"===============================")
    print(f"Bot Name: {bot_name}")
    print(f"Bot ID: {bot_id}")
    print(f"Bot Ping: {bot_ping}ms")
    print(f"Bot Status: {bot_status}")
    print(f"Python Version: {python_version}")
    print(f"Memory Usage: {memory_usage:.2f} MB")
    print(f"===============================")
    print(f"Bot is ready and online!")


# Command to change bot prefix
@bot.command()
async def prefix(ctx, new_prefix: str):
    """Set the bot's prefix (only for users with Manage Server permission)."""
    if ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(
            title="Prefix Changed",
            description=f"Bot prefix has been set to: `{new_prefix}`",
            color=discord.Color.green())
        await ctx.send(embed=embed)
        bot.command_prefix = new_prefix
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description=
            "You do not have permission to change the bot's prefix.",
            color=discord.Color.red())
        await ctx.send(embed=embed)


# Command to reboot bot (only for bot owner)
@bot.command()
async def reboot(ctx):
    """Reboots the bot (only for authorized users)."""
    if ctx.author.id == 1148212880722890783:  # Replace with your own Discord user ID
        embed = discord.Embed(title="Rebooting",
                              description="Rebooting the bot...",
                              color=discord.Color.orange())
        await ctx.send(embed=embed)
        os.execv(sys.executable, ['python'] + sys.argv)  # Reboot the bot
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You do not have permission to reboot the bot.",
            color=discord.Color.red())
        await ctx.send(embed=embed)


# Command to mute a member
@bot.command()
async def mute(ctx, member: discord.Member = None, *, reason: str = None):
    """Mute a member (requires 'Mute Members' permission)."""
    if not member or not reason:
        embed = discord.Embed(
            title="Missing Arguments",
            description="Please mention a user and provide a reason.",
            color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if ctx.author.guild_permissions.mute_members:
        await member.add_roles(discord.utils.get(ctx.guild.roles,
                                                 name="Muted"),
                               reason=reason)
        embed = discord.Embed(
            title="Muted",
            description=f"{member.mention} has been muted for: {reason}",
            color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You do not have permission to mute members.",
            color=discord.Color.red())
        await ctx.send(embed=embed)


# Command to unmute a member
@bot.command()
async def unmute(ctx, member: discord.Member = None):
    """Unmute a member (requires 'Mute Members' permission)."""
    if not member:
        embed = discord.Embed(title="Missing Arguments",
                              description="Please mention a user to unmute.",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if ctx.author.guild_permissions.mute_members:
        await member.remove_roles(
            discord.utils.get(ctx.guild.roles, name="Muted"))
        embed = discord.Embed(
            title="Unmuted",
            description=f"{member.mention} has been unmuted.",
            color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You do not have permission to unmute members.",
            color=discord.Color.red())
        await ctx.send(embed=embed)


# Command to kick a member
@bot.command()
async def kick(ctx, member: discord.Member = None, *, reason: str = None):
    """Kick a member (requires 'Kick Members' permission)."""
    if not member or not reason:
        embed = discord.Embed(
            title="Missing Arguments",
            description="Please mention a user and provide a reason.",
            color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Kicked",
            description=f"{member.mention} has been kicked for: {reason}",
            color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You do not have permission to kick members.",
            color=discord.Color.red())
        await ctx.send(embed=embed)


# Command to ban a member
@bot.command()
async def ban(ctx, member: discord.Member = None, *, reason: str = None):
    """Ban a member (requires 'Ban Members' permission)."""
    if not member or not reason:
        embed = discord.Embed(
            title="Missing Arguments",
            description="Please mention a user and provide a reason.",
            color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Banned",
            description=f"{member.mention} has been banned for: {reason}",
            color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You do not have permission to ban members.",
            color=discord.Color.red())
        await ctx.send(embed=embed)


# Command to clear messages (requires 'Manage Messages' permission)
@bot.command()
async def clear(ctx, amount: int = None):
    """Clear a specified number of messages."""
    if not amount:
        embed = discord.Embed(
            title="Missing Arguments",
            description="Please specify the number of messages to clear.",
            color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title="Messages Cleared",
                              description=f"{amount} messages cleared.",
                              color=discord.Color.green())
        await ctx.send(embed=embed, delete_after=3)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You do not have permission to clear messages.",
            color=discord.Color.red())
        await ctx.send(embed=embed)


# Command to flip a coin
@bot.command()
async def coinflip(ctx):
    """Flips a coin."""
    result = "Heads" if random.choice([True, False]) else "Tails"
    embed = discord.Embed(title="Coin Flip",
                          description=f"The result is: {result}",
                          color=discord.Color.green())
    await ctx.send(embed=embed)


# Command for Magic 8-Ball
@bot.command(aliases=['8ball'])
async def eightball(ctx, *, question: str = None):
    """Answers a question like a Magic 8-Ball (works for !eightball and !8ball)."""
    if not question:
        embed = discord.Embed(title="Missing Arguments",
                              description="Please ask a question.",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    responses = [
        "Yes", "No", "Maybe", "Ask again later", "Definitely not",
        "I don't know", "Yes, in the future", "Not a chance"
    ]
    answer = random.choice(responses)
    embed = discord.Embed(
        title="Magic 8-Ball",
        description=f"Your question: {question}\nAnswer: {answer}",
        color=discord.Color.green())
    await ctx.send(embed=embed)


# Command for showing bot status
@bot.command()
async def status(ctx, status: str = None):
    """Change the bot's status (e.g., 'online', 'dnd', 'idle', 'invisible')."""
    if status is None:
        embed = discord.Embed(
            title="Missing Arguments",
            description="Please specify a status (e.g., 'online', 'dnd', 'idle', 'invisible').",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    # Check if the user has permission to change the bot's status
    if ctx.author.id == 1148212880722890783:  # Replace with the bot owner's ID
        valid_statuses = ['online', 'idle', 'dnd', 'invisible']

        # Check if the status provided is valid
        if status.lower() in valid_statuses:
            if status.lower() == 'invisible':
                await bot.change_presence(status=discord.Status.invisible)
                embed = discord.Embed(
                    title="Status Changed",
                    description="Bot status has been set to: `Invisible`",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            elif status.lower() == 'dnd':
                await bot.change_presence(status=discord.Status.dnd)
                embed = discord.Embed(
                    title="Status Changed",
                    description="Bot status has been set to: `Do Not Disturb (DND)`",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            else:
                await bot.change_presence(status=discord.Status[status.lower()])
                embed = discord.Embed(
                    title="Status Changed",
                    description=f"Bot status has been set to: `{status}`",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Invalid Status",
                description="Please provide a valid status: 'online', 'idle', 'dnd', or 'invisible'.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You do not have permission to change the bot's status.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)





# Command to show the last deleted message (snipe)
@bot.command()
async def snipe(ctx):
    """Show the last deleted message in the channel."""
    if ctx.channel.id in bot.sniped_messages:
        message = bot.sniped_messages[ctx.channel.id]
        embed = discord.Embed(title="Last Deleted Message",
                              description=message.content,
                              color=discord.Color.orange())
        embed.set_footer(text=f"Deleted by: {message.author}")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="No Message to Snipe",
                              description="No messages to snipe!",
                              color=discord.Color.red())
        await ctx.send(embed=embed)


# Store deleted message for snipe command
@bot.event
async def on_message_delete(message):
    bot.sniped_messages[message.channel.id] = message


# Command to show bot stats
@bot.command()
async def stats(ctx):
    """Shows bot stats like uptime, ID, and more."""
    uptime = datetime.datetime.utcnow() - bot.start_time
    bot_id = bot.user.id
    bot_name = bot.user.name
    ping = round(bot.latency * 1000)

    embed = discord.Embed(title="Bot Stats",
                          description=f"**Bot Name:** {bot_name}\n"
                          f"**Bot ID:** {bot_id}\n"
                          f"**Uptime:** {str(uptime).split('.')[0]}\n"
                          f"**Ping:** {ping}ms",
                          color=discord.Color.green())
    await ctx.send(embed=embed)


# Run the bot

bot.run("MTMyNjI2MDg2MzQ2ODA0ODQ0Ng.G-DhuR.eV3safpDnNU5gDyNSyM5EYpqw_flG638dVkXwE")  # Replace with your actual bot token
