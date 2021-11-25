from telethon.events import NewMessage, StopPropagation
from logger import get_logger


class TextHandler:
    def __init__(self):
        self.counters = dict()

    async def __call__(self, event: NewMessage.Event):
        if event.chat_id not in self.counters:
            self.counters[event.chat_id] = 0

        self.counters[event.chat_id] += 1
        count = self.counters[event.chat_id]
        get_logger().info(
            msg=f"text handler called; chat_id={event.chat_id} count={count}; text={event.message.message}")

        base_msg = "send a photo you want to classify. Bot will try to tell between teslas, other cars and hotdogs. " \
                   "Please choose \"Compress Images\" on send for everything to work propetly :)"

        if count % 10 == 1:
            await event.message.respond(f"Sup, please {base_msg}")
        else:
            await event.message.respond(f"Please {base_msg}")

        raise StopPropagation
