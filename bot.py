import hikari
import lightbulb
import configparser

from help import HelpCommand


config = configparser.ConfigParser()
config.read("config.ini")


if __name__ == "__main__":
    bot = lightbulb.BotApp(
        token=config.get("BOT", "TOKEN"),
        prefix=lightbulb.when_mentioned_or(["campfire ", "camp "]),
        help_class=HelpCommand,
    )

    bot.load_extensions_from("./extensions")
    bot.run(
        activity=hikari.Activity(
            name="over your servers!", type=hikari.ActivityType.WATCHING
        ),
        status=hikari.Status.IDLE,
    )
