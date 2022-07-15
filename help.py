import lightbulb
import typing

from utils import info_response, EmbedField


class HelpCommand(lightbulb.BaseHelpCommand):
    """The help command to be sent by the bot."""

    async def send_bot_help(
        self, context: typing.Union[lightbulb.SlashContext, lightbulb.PrefixContext]
    ) -> None:
        """Reponds with a list of all commands associated with the bot.

        Arguments:
            context: The context of the help command.

        Returns:
            None.
        """
        plugins = get_plugins(context)
        plugins.sort(key=lambda plugin: plugin.name)
        embed_fields = []

        # Generate the embed fields
        for plugin in plugins:
            field = create_plugin_field(plugin)

            if field is not None:
                embed_fields.append(field)

        # Embed details
        help_title = "General Help"
        help_description = (
            "Here are a list of features available with the Campfire discord bot. Pass "
            "in the name of a category or command to view further information about it."
        )

        await info_response(
            context,
            help_title,
            help_description,
            fields=embed_fields,
        )

    async def send_plugin_help(
        self,
        context: typing.Union[lightbulb.SlashContext, lightbulb.PrefixContext],
        plugin: lightbulb.Plugin,
    ) -> None:
        """Reponds with a list of all commands associated with the plugin.

        Arguments:
            context: The context of the help command.
            plugin: The plugin to get the commands of.

        Returns:
            None.
        """
        field = create_plugin_field(plugin)

        if field is None:
            await self.object_not_found(context, plugin.name)
            return

        await info_response(
            context,
            "Plugin Help",
            "Sample plugin help",
            fields=[field],
        )

    async def send_command_help(
        self,
        context: typing.Union[lightbulb.SlashContext, lightbulb.PrefixContext],
        command: lightbulb.Command,
    ) -> None:
        """Reponds with the description and usage of a particular command.

        Arguments:
            context: The context of the help command.
            command: The command to display information about.

        Returns:
            None.
        """
        await context.respond("Command argument.")

    async def send_group_help(
        self,
        context: typing.Union[lightbulb.SlashContext, lightbulb.PrefixContext],
        group: typing.Union[lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup],
    ) -> None:
        """Reponds with a list of all subcommands associated with the group.

        Arguments:
            context: The context of the help command.
            group: The group to get the subcommands of.

        Returns:
            None.
        """
        await context.respond("Group argument.")

    async def object_not_found(
        self,
        context: typing.Union[lightbulb.SlashContext, lightbulb.PrefixContext],
        object: str,
    ) -> None:
        """Reponds with an error message as the object could not be found.

        Arguments:
            context: The context of the help command.
            object: The object that could not be found.

        Returns:
            None.
        """
        await context.respond("Unknown argument.")


def create_plugin_field(plugin: lightbulb.Plugin) -> typing.Optional[EmbedField]:
    """Creates an EmbedField containing the list of plugin commands.

    Pulls all commands and subcommands from the plugin and creates an EmbedField with a
    nicely formatted string of command names associated with the plugin.

    Arguments:
        plugin: The plugin to get the commands of.

    Returns:
        The EmbedField if the plugin has commands, otherwise None.
    """
    plugin_commands = get_plugin_commands(plugin)
    plugin_subcommands = get_plugin_subcommands(plugin)
    command_names = []

    # Create list of command names
    for command in plugin_commands:
        command_names.append(command.name)

    for subcommand in plugin_subcommands:
        command_names.append(subcommand.qualname)

    command_names.sort()

    # If there are commands to display, create an embed field
    if command_names != []:
        field_description = format_command_names(command_names)
        return EmbedField(plugin.name, field_description, False)


def format_command_names(command_names: typing.List[str]) -> str:
    """Formats the command names to be used as an embed field description.

    Arguments:
        command_names: The list of command names

    Returns:
        The formatted string of command names.
    """
    command_names = [f"`{name}`" for name in command_names]
    command_string = ", ".join(command_names)
    return command_string


def get_plugins(
    context: typing.Union[lightbulb.SlashContext, lightbulb.PrefixContext]
) -> typing.List[lightbulb.Plugin]:
    """Gets a list of all bot plugins given a context.

    Arguments:
        context: The context to take the plugins from.

    Returns:
        The list of plugins.
    """
    plugin_mapping = context.app.plugins
    plugins = [plugin_mapping[plugin_name] for plugin_name in plugin_mapping]

    return plugins


def get_plugin_commands(
    plugin: lightbulb.Plugin,
) -> typing.List[lightbulb.SlashCommand]:
    """Gets a list of all commands associated with a plugin.

    Arguments:
        plugin: The plugin to get the commands of.

    Returns:
        The list of commands.
    """
    commands = plugin.all_commands
    output_commands = []

    # Add strict slash commands (no slash command groups)
    for command in commands:
        is_slash_command = isinstance(command, lightbulb.SlashCommand)
        is_slash_command_group = isinstance(command, lightbulb.SlashCommandGroup)

        if is_slash_command and not is_slash_command_group:
            output_commands.append(command)

    return output_commands


def get_plugin_subcommands(
    plugin: lightbulb.Plugin,
) -> typing.List[lightbulb.SlashSubCommand]:
    """Gets a list of all group subcommands associated with a plugin.

    Arguments:
        plugin: The plugin to get the commands of.

    Returns:
        The list of subcommands.
    """
    commands = plugin.all_commands
    output_commands = []

    # Add subcommands from slash command groups
    for command in commands:
        if isinstance(command, lightbulb.SlashCommandGroup):
            output_commands += get_command_subcommands(command)

    return output_commands


def get_command_subcommands(
    command: lightbulb.SlashCommandGroup,
) -> typing.List[lightbulb.SlashSubCommand]:
    """Gets a list of all subcommands associated with a command group.

    Arguments:
        command: The command group to get the subcommands from.

    Returns:
        The list of subcommands.
    """
    return [command.subcommands[subcommand] for subcommand in command.subcommands]
