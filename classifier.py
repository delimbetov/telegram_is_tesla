from enum import Enum
from logger import get_logger
from fastai.learner import load_learner
from fastai.vision.core import Image as FastAiImage
from PIL import Image as PILImage


class Class(Enum):
    TESLA_3 = "Tesla Model 3"
    TESLA_CYBERTRUCK = "C Y B E R T R U C K"
    TESLA_S = "Tesla Model S"
    TESLA_X = "Tesla Model X"
    TESLA_Y = "Tesla Model Y"
    HOTDOG = "Not a tesla, but at least it's a god damn hot dog"
    OTHER_CAR = "Shitty car or something"


def pil2fast(image: PILImage):
    if type(PILImage) is not type(FastAiImage):
        raise RuntimeError("Types must match")

    return image


class Classifier:
    def __init__(self, path_to_model: str):
        get_logger().info(msg="Loading classifier from path={}".format(path_to_model))

        # load model
        self.model = load_learner(path_to_model)

        # load vocabulary
        self.vocabulary = {
            '3': Class.TESLA_3,
            'Cybertruck': Class.TESLA_CYBERTRUCK,
            'S': Class.TESLA_S,
            'X': Class.TESLA_X,
            'Y': Class.TESLA_Y,
            'hotdog': Class.HOTDOG,
            'not_tesla': Class.OTHER_CAR
        }

    def classify(self, image: PILImage):
        # run inference
        result_tuple = self.model.predict(pil2fast(image))
        get_logger().info(msg="Inference output: {}".format(result_tuple))

        return self.vocabulary[result_tuple[0]]
