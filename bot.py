from telethon import TelegramClient, events
from handlers.image import ImageHandler
from handlers.text import TextHandler
from classifier import Classifier
from logger import get_logger


class BotConfig:
    def __init__(
            self,
            api_id: int,
            api_hash: str,
            token: str,
            path_to_model: str):
        if api_id is None:
            raise RuntimeError("Api id must be set")

        if api_hash is None or len(api_hash) < 1:
            raise RuntimeError("Invalid api_hash: " + api_hash)

        if token is None or len(token) < 1:
            raise RuntimeError("Invalid token: " + token)

        if path_to_model is None or len(token) < 1:
            raise RuntimeError("Invalid path_to_model: " + path_to_model)

        self.api_id = api_id
        self.api_hash = api_hash
        self.token = token
        self.path_to_model = path_to_model

    def __repr__(self):
        return "App id=***, app hash=***, token=***, path_to_model=" + self.path_to_model


class Bot:
    def __init__(self, config: BotConfig):
        if config is None:
            raise RuntimeError("No config passed")

        self.config = config
        get_logger().info(msg="Creating Bot object with config: {}".format(self.config))

        self.client = TelegramClient(
            'is_tesla_bot',
            api_id=config.api_id,
            api_hash=config.api_hash).start(bot_token=config.token)

        # Load classifier
        self.classifier = Classifier(path_to_model=self.config.path_to_model)

        # Add text handler
        self.client.add_event_handler(
            callback=TextHandler(),
            event=events.NewMessage(incoming=True, outgoing=False, func=lambda event: event.photo is None))

        # Add image handler
        self.client.add_event_handler(
            callback=ImageHandler(classifier=self.classifier),
            event=events.NewMessage(incoming=True, outgoing=False, func=lambda event: event.photo is not None))

    async def arun(self):
        get_logger().info("Awaiting on run_until_disconnected")
        await self.client.run_until_disconnected()

    def run(self):
        get_logger().info("Starting run loop ...")

        with self.client:
            get_logger().info("Starting async run loop ... ")
            self.client.loop.run_until_complete(self.arun())
            get_logger().info("... async run loop is stopped")

        get_logger().info("... run loop is stopped")
