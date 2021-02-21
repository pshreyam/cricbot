import os

import discord

from dotenv import load_dotenv
load_dotenv()

from provider import get_fixtures, get_recent_matches, get_score

class BotClient(discord.Client):
    async def on_connect(self):
        print('Connecting to discord!')
    
    async def on_ready(self):
        print(f'Connected to discord as : {self.user}')
    
    async def on_message(self, message):
        if message.author == self.user:
            return 
        else:
            if message.content.startswith('?'):
                cmd = str(message.content[1:])
                if cmd == 'help':
                    help_embed = discord.Embed(
                        title='Help for CricHelperBot!',
                        description='CricHelperBot is intended to help you with \
                        cricket scores and fixtures!',
                        color=discord.Color.blue()
                    )
                    help_embed.add_field(
                        name='?fixtures', 
                        value='get future cricket fixtures',
                        inline=True
                    )
                    help_embed.add_field(
                        name='?results', 
                        value='get results for recent matches',
                        inline=True
                    )
                    help_embed.add_field(
                        name='?score <match_id>', 
                        value='get score for the match with id',
                        inline=True
                    )
                    await message.reply(embed=help_embed)
                elif cmd == 'fixtures':
                    fixtures_embed = discord.Embed(
                        title='Fixtures',
                        description='Fixtures for a week',
                        color=discord.Color.dark_purple()
                    )
                    fixtures = get_fixtures() 
                    if fixtures:
                        for x in fixtures:
                            fixtures_embed.add_field(
                                name=x['name'],
                                value=x['date']
                            )
                    await message.reply(embed=fixtures_embed)
                elif cmd == 'results':
                    results_embed = discord.Embed(
                        title='Results',
                        description='Results for recent matches',
                        color=discord.Color.red()
                    )
                    matches = get_recent_matches()
                    if matches:
                        for x in matches:
                            results_embed.add_field(
                                name=x['game'],
                                value=x['utc_date']
                            )
                    await message.reply(embed=results_embed)
                elif cmd.startswith('score'):
                    if not ' ' in cmd:
                        return
                    _, match_id = cmd.split()
                    try:
                        score_embed = discord.Embed(
                            title=f'Score for match: {match_id}',
                            description=get_score(int(match_id)),
                            color=discord.Color.red()
                        )
                        await message.reply(embed=score_embed)
                    except:
                        await message.reply('Sorry! error encountered!')


client = BotClient()
client.run(os.getenv('CLIENT_TOKEN'))