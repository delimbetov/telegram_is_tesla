from bot import Bot, BotConfig
from logger import configure_logging
import sys


def main():
    # Configure logging
    configure_logging(name="is_tesla_bot")

    # Parse command line args
    # 0 - prog name
    # 1 - path_to_model
    # 2 - api id
    # 3 - api hash
    # 4 - bot token
    if len(sys.argv) != 5:
        raise RuntimeError("Path to model, api id, api hash, token are required to be passed as command line "
                           "argument. sys.argv: {}".format(sys.argv))

    path_to_model = sys.argv[1]
    api_id = int(sys.argv[2])
    api_hash = sys.argv[3]
    token = sys.argv[4]

    # Load configs
    bot_config = BotConfig(
        api_id=api_id,
        api_hash=api_hash,
        token=token,
        path_to_model=path_to_model)

    # Create bot obj
    bot = Bot(config=bot_config)

    # Run the bot
    bot.run()


if __name__ == '__main__':
    main()
