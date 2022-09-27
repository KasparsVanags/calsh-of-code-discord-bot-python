# bot.py
import asyncio
import os
import codingame
import discord
from codingame.http import HTTPError
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# cookie expires after 1 year and has to be updated
COOKIE = os.getenv('CODINGAME_COOKIE')

client = codingame.Client()
client.login(remember_me_cookie=COOKIE)

intent = discord.Intents.default()
intent.message_content = True
bot = commands.Bot(intents=intent, command_prefix='!')

validLanguages = ["Any"] + client.get_language_ids()
validModes = ["RANDOM", "FASTEST", "REVERSE", "SHORTEST"]

TIMEOUT = 60
leaveAfter = TIMEOUT


async def wait_for_players(handle):
    global leaveAfter
    leaveAfter -= 1
    if len(client.get_clash_of_code(handle).players) > 1 or leaveAfter < 1:
        leaveAfter = TIMEOUT
        try:
            client.request("ClashOfCode", "leaveClashByHandle", [client.codingamer.id, handle])
        except Exception as e:
            print(e)
        return
    await asyncio.sleep(1)
    await wait_for_players(handle)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!clash mode lang"))


@bot.command()
async def clash(ctx, mode, language):
    language = language.lower()
    mode = mode.lower()

    if mode == "random":
        mode = ["FASTEST", "REVERSE", "SHORTEST"]
    else:
        try:
            mode_id = [item.lower() for item in validModes].index(mode)
            mode = [validModes[mode_id]]
        except ValueError:
            await clash_error(ctx, commands.CommandError(f'"{mode}" is not a valid mode'))
            return

    if language == "any":
        language = []
    else:
        try:
            language_id = [item.lower() for item in validLanguages].index(language)
            language = [validLanguages[language_id]]
        except ValueError:
            await clash_error(ctx, commands.CommandError(f'"{language}" is not a valid language'))
            return

    try:
        lobby = client.request("ClashOfCode", "createPrivateClash", [client.codingamer.id, language, mode])
        handle = lobby['publicHandle']
        if len(mode) > 1:
            mode = [":game_die: Random"]
        if len(language) == 0:
            language = ["Any language"]
        mode = mode[0].replace("FASTEST", ":rocket: Fastest").replace("REVERSE", ":brain: Reverse") \
            .replace("SHORTEST", ":scroll: Shortest")
        await ctx.message.delete()
        await ctx.send(f"{mode}  -  {language[0]}  -  Started by {ctx.message.author.mention}\n"
                       f"https://www.codingame.com/clashofcode/clash/{handle}\n"
                       f":rotating_light: This message will self-destruct in 15 minutes", delete_after=900)
        await wait_for_players(handle)
    except HTTPError:
        await ctx.send("I've been logged out or couldn't connect to Codingame")


@clash.error
async def clash_error(ctx, error):
    print(error)
    await ctx.send(f"{error}!clash mode language\n\n"
                   "Modes - " + " | ".join(validModes).lower() + "\n\n"
                   "Languages - " + " | ".join(validLanguages))


bot.run(TOKEN)
