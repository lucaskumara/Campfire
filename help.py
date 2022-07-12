import lightbulb


class HelpCommand(lightbulb.BaseHelpCommand):
    async def send_bot_help(self, context):
        await context.respond("No arguments.")

    async def send_plugin_help(self, context, plugin):
        await context.respond("Plugin argument.")

    async def send_command_help(self, context, command):
        await context.respond("Command argument.")

    async def send_group_help(self, context, group):
        await context.respond("Group argument.")

    async def object_not_found(self, context, obj):
        await context.respond("Unknown argument.")
