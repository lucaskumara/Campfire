import discord
import copy

from discord.ext import commands
from helpers import Pages


class HelpCommand(commands.HelpCommand):
    '''A custom help command to be used by the bot.'''

    def __init__(self):
        super().__init__()

    async def send_error_message(self, error_message):
        '''Send formatted error message.'''

        # Delete authors message if error happened in a guild
        if self.context.message.guild is not None:
            await self.context.message.delete()

        # Create error embed
        error_embed = discord.Embed(
            description=error_message.replace('"', '`'),
            colour=discord.Colour.red()
        )

        await self.get_destination().send(embed=error_embed, delete_after=5)

    async def send_bot_help(self, mapping):
        '''Called when the help command is called with no arguments.'''

        # Gets the valid command prefixes
        command_prefixes = await self.context.bot.get_prefix(self.context.message)

        # Create help embed
        help_embed = discord.Embed(
            colour=discord.Colour.orange(),
            timestamp=self.context.message.created_at
        )

        # Shows correct prefix for both dms and guilds
        if len(command_prefixes) == 2:  # <@bot id> and <@!bot id>
            command_prefix = '@Campfire '
            help_embed.description = f'Here is a complete list of all the bot commands. \nThe command prefix for the bot is `@Campfire`'
        else:
            command_prefix = command_prefixes[-1]
            help_embed.description = f'Here is a complete list of all the bot commands. \nThe command prefix for the bot is `{command_prefix}`'

        # Set embed author and footer
        help_embed.set_author(name='Campfire', icon_url=self.context.bot.user.avatar_url)
        help_embed.set_footer(text=f'Requested by {self.context.author}', icon_url=self.context.author.avatar_url)

        # Create pages list and counter
        pages = []
        counter = 0

        # Filter the cogs
        valid_cogs = [cog for cog in mapping if cog is not None and cog.qualified_name != 'Admin' and cog.get_commands() != []]

        # Create each page and add them to pages list
        for cog in valid_cogs:

            # Add field to help embed
            field_value = f'```\n{command_prefix}help {cog.qualified_name}```'
            help_embed.add_field(name=cog.qualified_name, value=field_value, inline=False)

            # Increment counter
            counter += 1

            # 3 cogs per page
            if counter == 1:
                counter = 0
                pages.append(copy.deepcopy(help_embed))
                help_embed.clear_fields()

        # Create last page if there is one
        if counter != 0:
            pages.append(help_embed)

        # Add page counts to pages
        page_count = len(pages)
        for i in range(page_count):
            pages[i].title = f'Page {i + 1}/{page_count}'

        # Use Pages to paginate the message
        paginator = Pages(self.context.bot, pages)
        await paginator.start(self.context)

    async def send_cog_help(self, cog):
        '''Called when the help command is called with a cog argument.'''

        # Don't show admin commands
        if cog.qualified_name == 'Admin' or cog.get_commands() == []:
            await self.send_error_message(f'No command called "{cog.qualified_name}" found.')
            return

        # Get command names
        command_names = []
        for command in cog.get_commands():
            command_names.append(command.name)

            # If command is a group, add subcommands
            if hasattr(command, 'commands'):
                for i, subcommand in enumerate(command.commands):
                    command_names.append(f'{command.name} {subcommand.name}')

        commands_string = '```\n' + '\n'.join(command_names) + '```'

        # Create cog embed
        cog_embed = discord.Embed(
            title=cog.qualified_name,
            description=cog.description,
            colour=discord.Colour.orange(),
            timestamp=self.context.message.created_at
        )

        cog_embed.set_author(name='Campfire', icon_url=self.context.bot.user.avatar_url)
        cog_embed.add_field(name='Commands', value=commands_string, inline=False)
        cog_embed.set_footer(text=f'Requested by {self.context.author}', icon_url=self.context.author.avatar_url)

        await self.context.reply(embed=cog_embed)

    async def send_group_help(self, group):
        '''Called when the help command is called with a group argument.'''

        # Don't show admin commands
        if group.cog.qualified_name == 'Admin':
            await self.send_error_message(f'No command called "{group.name}" found.')
            return

        # Gets the valid command prefixes
        command_prefixes = await self.context.bot.get_prefix(self.context.message)

        # Shows correct prefix for both dms and guilds
        if len(command_prefixes) == 2:  # <@bot id> and <@!bot id>
            command_prefix = '@Campfire '
        else:
            command_prefix = command_prefixes[-1]

        # Create command embed
        group_embed = discord.Embed(
            title=group.name.capitalize(),
            description=group.help,
            colour=discord.Colour.orange(),
            timestamp=self.context.message.created_at
        )

        group_embed.set_author(name='Campfire', icon_url=self.context.bot.user.avatar_url)
        group_embed.add_field(name='Usage', value=f'```\n{command_prefix}{group.usage}```', inline=False)
        group_embed.set_footer(text=f'Requested by {self.context.author}', icon_url=self.context.author.avatar_url)

        await self.context.reply(embed=group_embed)

    async def send_command_help(self, command):
        '''Called when the help command is called with a command argument.'''

        # Don't show admin commands
        if command.cog.qualified_name == 'Admin':
            await self.send_error_message(f'No command called "{command.name}" found.')
            return

        # Gets the valid command prefixes
        command_prefixes = await self.context.bot.get_prefix(self.context.message)

        # Shows correct prefix for both dms and guilds
        if len(command_prefixes) == 2:  # <@bot id> and <@!bot id>
            command_prefix = '@Campfire '
        else:
            command_prefix = command_prefixes[-1]

        # Create command embed
        command_embed = discord.Embed(
            title=command.name.capitalize(),
            description=command.help,
            colour=discord.Colour.orange(),
            timestamp=self.context.message.created_at
        )

        command_embed.set_author(name='Campfire', icon_url=self.context.bot.user.avatar_url)
        command_embed.add_field(name='Usage', value=f'```\n{command_prefix}{command.usage}```', inline=False)
        command_embed.set_footer(text=f'Requested by {self.context.author}', icon_url=self.context.author.avatar_url)

        await self.context.reply(embed=command_embed)
