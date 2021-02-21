import os

import discord

from dotenv import load_dotenv
load_dotenv()

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
                        color=discord.Color.blue(),
                    )
                    help_embed.add_field(
                        name='?fixtures', 
                        value='get future cricket fixtures',
                        inline=True
                    )
                    help_embed.add_field(
                        name='?scores', 
                        value='get scores for currently active matches',
                        inline=True
                    )
                    await message.reply(embed=help_embed)
                elif cmd == 'fixtures':
                    await message.reply(
                        'Sorry! \'fixtures\' feature of this bot is currently under development!'
                    )
                elif cmd == 'scores':
                    await message.reply(
                        'Sorry! \'scores\' feature of this bot is currently under development!'
                    )

client = BotClient()
client.run(os.getenv('CLIENT_TOKEN'))