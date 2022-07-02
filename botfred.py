from unicodedata import name
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
@bot.command(name='addgame')
async def add_game(ctx, game, image, description):
    '''
    !add_game "somegame" "(URL for the image)" "game description"  you must wrap all parameters in quotes. This command will add a game, image, and a description. 
    '''
    game = game.upper()
    if ctx.message.author.guild_permissions.administrator:
        if list_of_games.find_one({"game":game}):
            await ctx.send(f"That game already exists in the database!", delete_after=60)
            await ctx.message.delete(delay=1)
        else:   
            add_game_to_DB(game, image, description)
            await ctx.send(f"SUCCESS!", delete_after=60)
            await ctx.message.delete(delay=1)
    else:
        await ctx.send(f"Only an administrator can add a game", delete_after=60)
        await ctx.message.delete(delay=1)

# add game to DB
def add_game_to_DB(game,image, description):
    game = game.upper()
    record = {
            'game': game,
            'name': [],
            'number': [],
            'image': image,
            'description': description,
            }
    list_of_games.insert_one(record)

# List games command
@bot.command(name = 'listgames')
async def list_games(ctx):
    '''
    !list_games  This command will list the Titles, image, description and gamers of all the games in the DataBase.
    '''
    games = list_of_games.find({})
    for game in games: 
        gamers = game['name']
        gamers_list = (', ').join(map(str, gamers))
        # Card for games with gamers
        embed = discord.Embed(
        title = 'Game Card',
        description = f'🕹 🎮\n Gamers: {make_title_case(gamers_list)} ',
        color = discord.Color.red()
        )
        embed.add_field(
            name=f'{make_title_case(game["game"])}:',
            value = f'{game["description"]}',
            inline=False
        )
        embed.set_image(url=f'{game["image"]}')
        # card for games with no gamers
        empty_gamers = discord.Embed(
        title = 'Game Card',
        description = f'🕹 🎮\n No gamers are assigned currently!',
        color = discord.Color.red()
        )
        empty_gamers.add_field(
            name=f'{make_title_case(game["game"])}:',
            value = f'{game["description"]}',
            inline=False
        )
        empty_gamers.set_image(url=f'{game["image"]}')
        if gamers_list != '':
            user = bot.get_user(ctx.author.id) or await bot.fetch_user(ctx.author.id)
            await user.send(embed=embed)
            await ctx.message.delete(delay=1)
        else:
            await user.send(embed=empty_gamers)
            await ctx.message.delete(delay=1)
    return
#remove games command
@bot.command(name = 'removegame')
async def remove_game(ctx, game):
    '''
    **ADMIN ONLY** !remove_game  This command will remove the game and its contents in the DataBase.
    
    '''
    game = game.upper()
    if ctx.message.author.guild_permissions.administrator:
        games = list_of_games.find({})
        for title in games:
            target = title['game']
        if game in target:
            list_of_games.delete_one({'game': game})
            await ctx.send(f'{make_title_case(target)} was deleted', delete_after=60)
            await ctx.message.delete(delay=1)
        else:
            await ctx.send(f'The game {make_title_case(target)} was not found', delete_after=60)    
            await ctx.message.delete(delay=1)
    else:
        await ctx.send(f'Bitch, you are not an administrator!', delete_after=60)
        await ctx.message.delete(delay=1)    

# add a user to the game list command
@bot.command(name ='addtogame')
async def add_to_game(ctx, game):
    '''
    !add_to_game  This command will add you to a games list.
    
    '''
    game = game.upper()
    if ctx.author == ctx.author:
        games = list_of_games.find({})
        for title in games:
            obj_id = title['_id']
            target = title['game']
            if game in target:
                if game not in target:
                    await ctx.send(f'That {make_title_case(target)} does not exist!')
                elif game in target and ctx.author.name not in title['name']:
                    list_of_games.update_one({"_id":ObjectId(obj_id)},{"$push":{"number":ctx.author.id, 'name':ctx.author.name}})
                    await ctx.send(f'{ctx.author.name} was added to the {make_title_case(target)}\'s list', delete_after=60)
                    await ctx.message.delete(delay=1)
                else:
                    await ctx.send(f'{ctx.author.name} is already on {make_title_case(target)}\'s game list', delete_after=60),
                    await ctx.message.delete(delay=1)   
    else:
        await ctx.send(f'{ctx.author.name} are you who you say you are? 🤐', delete_after=60)
        await ctx.message.delete(delay=1)
@bot.command(name = 'removefromgame')
async def remove_from_game(ctx, game):
    '''
    !remove_from_game  This command will remove you from a games list.
    
    '''
    game = game.upper()
    if ctx.author == ctx.author:
        games = list_of_games.find({})
        for title in games:
            obj_id= title['_id']
            target = title['game']
            if game in target and ctx.author.name in title['name']:
                list_of_games.update_one({"_id":ObjectId(obj_id)},{"$pull" : {"number":ctx.author.id, "name":ctx.author.name}})
                await ctx.send(f'{ctx.author.name} removed from {make_title_case(target)}!', delete_after=60)
                await ctx.message.delete(delay=1)    
            elif  game in target and ctx.author.name not in title['name']:
                await ctx.send(f'You are not on {make_title_case(target)}\'s game list!', delete_after=60)
                await ctx.message.delete(delay=1)
    else:
        await ctx.send(f'{ctx.author.name}, are you who you say you are?! 😵', delete_after=60)
        await ctx.message.delete(delay=1)


# List your games command
@bot.command(name='mygames')
async def my_games(ctx):
    '''
    !my_games This command will send you a list of the games you are apart of.
    '''
    if ctx.author == ctx.author:
        games = list_of_games.find({})
        for title in games:
            embed = discord.Embed(
            title = 'Game Card',
            description = '🕹 🎮',
            color = discord.Color.red()
            )
            embed.add_field(
            name=f'{make_title_case(title["game"])}',
            value = f'{title["description"]}',
            inline=False
            )
            embed.set_image(url=f'{title["image"]}')
            if 'name' in title and ctx.author.name in title['name'] and 'image' in title:
                user = bot.get_user(ctx.author.id) or await bot.fetch_user(ctx.author.id)
                await user.send(embed=embed)
                await ctx.message.delete(delay=1)
        return
    else:
        await ctx.send(f'{ctx.author.name}, are you who you say you are?! 😵', delete_after=60)
        await ctx.message.delete(delay=1)
@bot.command()
async def gamers(ctx,game):
    '''
    !gamers somegame This command alerts all users in the game list you are online and playing the game specified.
    '''
    msg = 'This game list is pretty lonely 😢'
    game = game.upper()
    author = ctx.author
    games = list_of_games.find({})
    for dict in games:
        num = dict.get('number')
        if game in dict['game'] and author.id in num:
            num.remove(author.id)
            id_list_as_string = '> <@'.join(map(str, num))
            new_id_list = None if id_list_as_string == '' else f'<@{id_list_as_string}>'
            if new_id_list is not None:
                msg = f'{new_id_list}, {author.name} is on playing {make_title_case(dict["game"])}'
            try:
                await ctx.send(msg, delete_after=1200)
                await ctx.message.delete(delay=1)
            except Exception as e:
                print(f'await error: {e}')
    return

# BotFred apologizes for master
@bot.command()
async def apologize(ctx, user):
    '''
    !apologize **ADMIN ONLY**
    '''
    if ctx.message.author.guild_permissions.administrator:
        if user:
            await ctx.send(f'Apologies <@{user}>, my master is busy and will not be able to game at this time.', delete_after=600)
            await ctx.message.delete(delay=1)  
    else:
        await ctx.send(f'Bitch, you are not my master! Toss me a beer on your way out.', delete_after=60)
        await ctx.message.delete(delay=1)

# Change the default !help command
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title = 'The Help Section',
        description = 'Welcome to the help section. Here you will find all of the commands for the server.',
        color = discord.Color.red()
    )
    embed.add_field(
        name='!addgame "somegame" "(URL for the image)" "game description" **ADMIN ONLY**',
        value = 'You must wrap all parameters in quotes. This command will add a game, image, and a description.',
        inline=False
    )
    embed.add_field(
        name='!listgames',
        value = 'This command will list the Titles, image, description and gamers of all the games in the DataBase.',
        inline=False
    )
    embed.add_field(
        name='!removegame "somegame" **ADMIN ONLY**',
        value = 'This command will remove the game and its contents in the DataBase.',
        inline=False
    )
    embed.add_field(
        name='!addtogame "somegame"',
        value = 'This command will add you to a games list. Use quotes if there are games that are similarly named. ',
        inline=False
    )
    embed.add_field(
        name='!removefromgame "somegame"',
        value = 'This command will remove you from a games list',
        inline=False
    )
    embed.add_field(
        name='!mygames',
        value = 'This command will send you a list of the games you are apart of.',
        inline=False
    )
    embed.add_field(
        name='!gamers "somegame"',
        value = 'This command alerts all users in the game list you are online and playing the game specified.',
        inline=False
    )
    embed.add_field(
        name = '!apologize userid  **ADMIN ONLY**',
        value ='Must input the users ID. This command apologizes to the users id that is inserted into the command.',
        inline=False
    )
    await ctx.send(embed=embed, delete_after=60)
    await ctx.message.delete(delay=1)

def make_title_case(variable):
    '''
    Takes a variable and returns it in  Title Case
    '''
    return variable.title()
bot.run(TOKEN)

mongodb.close()