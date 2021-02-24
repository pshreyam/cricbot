import os

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv

from provider import get_fixtures, get_results, get_score

load_dotenv()

BOT_PREFIX = '%'

bot = commands.Bot(
    command_prefix=BOT_PREFIX, 
    description='Helps with cricket scores!'
)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to discord!')

@bot.command(name='fixtures')
async def send_fixtures(ctx, *args):
    fixtures = discord.Embed(
        title='Fixtures',
        description='Fixtures for the next 7 days',
        color=discord.Color.dark_purple()
    )

    fixtures_list = get_fixtures() 
    
    if fixtures_list:
        for fixture in fixtures_list:
            fixtures.add_field(
                name=fixture['name'],
                value=fixture['date']
            )

    await ctx.send(embed=fixtures)

@bot.command(name='results')
async def send_results(ctx, *args):
    results = discord.Embed(
        title='Results',
        description='Results for recent matches',
        color=discord.Color.red()
    )

    results_list = get_results()
    
    if results_list:
        for result in results_list:
            results.add_field(
                name=result['game'],
                value=result['utc_date']
            )

    await ctx.send(embed=results)

@bot.command(name='score')
async def send_match_score(ctx, *args):
    err_msg = 'Please provide a valid match id!'

    if not args:
        await ctx.send(err_msg)
        return

    try:
        match_id = int(args[0])
    except ValueError:
        await ctx.send(err_msg)
        return

    score = discord.Embed(
        title=f'Score for match: {match_id}',
        description=get_score(match_id),
        color=discord.Color.red()
    )

    await ctx.send(embed=score)

@bot.command(name='help')
async def send_help(ctx, *args):
    help = discord.Embed(
        title='Help for CricHelperBot!',
        description=('CricHelperBot is intended to help you with '
        'cricket scores and fixtures!'),
        color=discord.Color.blue()
    )

    help.add_field(
        name=f'{BOT_PREFIX}fixtures', 
        value='get future cricket fixtures',
        inline=True
    )

    help.add_field(
        name=f'{BOT_PREFIX}results', 
        value='get results for recent matches',
        inline=True
    )

    help.add_field(
        name=f'{BOT_PREFIX}score <match_id>', 
        value='get score for the match with id',
        inline=True
    )

    await ctx.send(embed=help)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(('Sorry! No such command. '
        f'Try running {BOT_PREFIX}help to check out '
        'the list of available commands.'))
        return

    raise error

bot.run(os.getenv('CLIENT_TOKEN'))