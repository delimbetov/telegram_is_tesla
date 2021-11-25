from bot import Bot, BotConfig
from logger import configure_logging
import sys


def main():
    # Configure logging
    configure_logging(name="is_tesla_bot")

    # Parse command line args
    # 0 - prog name
    # 1 - api id
    # 2 - api hash
    # 3 - bot token
    # 4 - path_to_model
    if len(sys.argv) != 5:
        raise RuntimeError("Api id, api hash, token, path_to_model are required to be passed as command line argument")

    api_id = int(sys.argv[1])
    api_hash = sys.argv[2]
    token = sys.argv[3]
    path_to_model = sys.argv[4]

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
