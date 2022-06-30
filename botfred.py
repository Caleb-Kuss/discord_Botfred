import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()
TOKEN = os.getenv('TOKEN')
URI = os.getenv('URI')

# Command that initiates BOT
bot = commands.Bot(command_prefix='!')

# Remove default helper command
bot.remove_command('help')
# Connecting to DB
try:
    mongodb = MongoClient(URI)
    print('connected to MongoDB')
except:
    print('could not connect to MongoDB')

# Accessing the DB Named played_games
db = mongodb.played_games
# Accessing the DB Collection inside of played_games
list_of_games = db.games_list

# add game command
@bot.command()
async def add_game(ctx, game):
    '''
    !add_game somegame This command will add a game DO NOT use spaces in the Title. 
    '''
    game = game.lower()
    if ctx.message.author.guild_permissions.administrator:
        if list_of_games.find_one({"game":game}):
            await ctx.send(f"The game {game} already exists in the database!")
        else:    
            add_game_to_DB(game)
            await ctx.send(f"SUCCESS!")
    else:
        await ctx.send(f"Only an administrator can add a game")

# add game to DB
def add_game_to_DB(game):
    game = game.lower()
    record = {
            'game': game,
            'name': [],
            'number': [],
            }
    list_of_games.insert_one(record)

# List games command
@bot.command()
async def list_games(ctx):
    '''
    !list_games  This command will list the Titles of all the games in the DataBase
    '''
    # whats going on with the if statement?
    games = list_of_games.find({})
    for game in games: 
        if game:
            await ctx.send(f'{game["game"]}')
        else:
            await ctx.send('There are no games yet!')
  
#remove games command
@bot.command()
async def remove_game(ctx, game):
    '''
    **ADMIN ONLY** !remove_game  This command will remove the Title of the game in the DataBase
    
    '''
    game = game.lower()
    if ctx.message.author.guild_permissions.administrator:
        games = list_of_games.find({})
        for title in games:
            target = title['game']
        if game == target:
            list_of_games.delete_one({'game': game})
            await ctx.send(f'{game} was deleted')
        else:
            await ctx.send(f'The game {game} was not found')    
    else:
        await ctx.send(f'Bitch, you are not an administrator!')    

# add a user to the game list command
@bot.command()
async def add_to_game(ctx, game):
    '''
    !add_to_game  This command will add you to a games list
    
    '''
    game = game.lower()
    if ctx.author == ctx.author:
        games = list_of_games.find({})
        for title in games:
            obj_id = title['_id']
            target = title['game']
            if target == game:
                if game not in target:
                    await ctx.send(f'This {game} does not exist!')
                elif game in target and ctx.author.name not in title['name']:
                    list_of_games.update_one({"_id":ObjectId(obj_id)},{"$push":{"number":ctx.author.id, 'name':ctx.author.name}})
                    await ctx.send(f'{ctx.author.name} added to {game}')
                else:
                    await ctx.send(f'{ctx.author.name} is already on {game}\'s game list')   
    else:
        await ctx.send(f'You can only add yourself to a game!')
@bot.command()
async def remove_from_game(ctx, game):
    '''
    !remove_from_game  This command will remove you from a games list
    
    '''
    if ctx.author == ctx.author:
        games = list_of_games.find({})
        for title in games:
            obj_id= title['_id']
            target = title['game']
            if target == game and ctx.author.name in title['name']:
                list_of_games.update_one({"_id":ObjectId(obj_id)},{"$pull" : {"number":ctx.author.id, "name":ctx.author.name}})
                await ctx.send(f'{ctx.author.name} removed from {game}!')    
            elif  target == game and ctx.author.name not in title['name']:
                await ctx.send(f'You are not on {game}\'s game list!')
    else:
        await ctx.send(f'Are you who you say you are?! 😵')


# List your games command
@bot.command()
async def my_games(ctx):
    '''
    !my_games command will list the games you are apart of.
    '''
    if ctx.author == ctx.author:
        games = list_of_games.find({})
        for title in games:
            target = title['game']
            if 'name' in title and ctx.author.name in title['name']:
                await ctx.send(f'{target}')
        return
    else:
        await ctx.send(f'Are you who you say you are?! 😵')

@bot.command()
async def gamers(ctx,game):
    '''
    !gamers somegame alerts all users in the game list you are online and playing the game specified.
    '''
    msg = 'This game list is pretty lonely 😢'
    game = game.lower()
    author = ctx.author
    games = list_of_games.find({})
    for dict in games:
        num = dict.get('number')
        if game == dict['game'] and author.id in num:
            print(f'id: {author.id}')
            num.remove(author.id)
            print(f'num: {num}')
            id_list_as_string = '> <@'.join(map(str, num))
            print(f'list string: {id_list_as_string}')
            new_id_list = None if id_list_as_string == '' else f'<@{id_list_as_string}>'
            if new_id_list is not None:
                msg = f'{new_id_list}, {author.name} is on playing {game}'
            try:
                await ctx.send(msg)
            except Exception as e:
                print(f'await error: {e}')
    return

# BotFred apologizes for master
@bot.command()
async def apologize(ctx, user):
    '''
    !apologize This is for NoPurps
    '''
    if ctx.message.author.guild_permissions.administrator:
        if user:
            await ctx.send(f'Apologies <@{user}>, my master is busy and will not be able to game at this time.')  
    else:
        await ctx.send(f'Bitch, you are not my master! Toss me a beer on your way out.')




# Change the default !help command
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title = 'The Help Section',
        description = 'Welcome to the help section. Here you will find all of the commands for the server.',
        color = discord.Color.red()
    )
    embed.add_field(
        name='!add_game "somegame" **ADMIN ONLY**',
        value = 'This command will add a game to the list of games DO NOT use spaces in the title of the game.',
        inline=False
    )
    embed.add_field(
        name='!list_games',
        value = 'This command will list the Titles of all the games in the DataBase.',
        inline=False
    )
    embed.add_field(
        name='!remove_game "somegame" **ADMIN ONLY**',
        value = 'This command will remove the Title of the game in the DataBase.',
        inline=False
    )
    embed.add_field(
        name='!add_to_game "somegame"',
        value = 'This command will add you to a games list.',
        inline=False
    )
    embed.add_field(
        name='!remove_from_game "somegame"',
        value = 'This command will remove you from a games list',
        inline=False
    )
    embed.add_field(
        name='!my_games',
        value = 'command will list the games you are apart of.',
        inline=False
    )
    embed.add_field(
        name='!gamers "somegame"',
        value = 'alerts all users in the game list you are online and playing the game specified.',
        inline=False
    )
    embed.add_field(
        name = '!apologize',
        value ='This is for NoPurps',
        inline=False
    )
    await ctx.send(embed=embed)

bot.run(TOKEN)

mongodb.close()