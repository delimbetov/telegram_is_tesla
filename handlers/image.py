from asyncio import sleep
from telethon.events import NewMessage, StopPropagation
from logger import get_logger
from classifier import Classifier
from PIL import Image as PILImage
import io


class ImageHandler:
    def __init__(self, classifier: Classifier):
        self.classifier = classifier

    # CallableHandlerWithStorage
    async def __call__(self, event: NewMessage.Event):
        get_logger().info(msg=f"image handler called; chat_id={event.chat_id}; photo={event.photo}")

        # Download image
        data = await event.download_media(file=bytes)

        # DEBUG:
        image = PILImage.open(io.BytesIO(data))
        get_logger().info(msg=f"photo2={event.photo}")

        # Send stupid jokes
        await event.message.respond(f"Firing up a GPU cluster . . .")
        await sleep(3)
        await event.message.respond(f"Charging your credit card for AWS bills . . .")
        await sleep(3)
        await event.message.respond(f"And the answer is . . .")
        await sleep(2)

        # Classify image
        image_class = self.classifier.classify(image=image)
        get_logger().info(
            msg=f"image handler called; chat_id={event.chat_id}; photo={event.photo}; result={image_class}")

        # Send the result
        await event.respond(image_class.value)

        raise StopPropagation
