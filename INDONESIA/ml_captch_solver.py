import numpy as np
import cv2
import typing
from mltu.configs import BaseModelConfigs
from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder
from PIL import Image
import os
import sys

cur_dir = os.path.dirname(__file__)


class ImageToWordModel(OnnxInferenceModel):
    def __init__(self, char_list: typing.Union[str, list], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.char_list = char_list

    def predict(self, image: np.ndarray):
        image = cv2.resize(image, self.input_shape[:2][::-1])
        # image = cv2.resize(image, [5000, 4])
        image_pred = np.expand_dims(image, axis=0).astype(np.float32)
        preds = self.model.run(None, {self.input_name: image_pred})[0]
        text = ctc_decoder(preds, self.char_list)[0]
        return text

def captcha_ml_solver():
    retry=3
    for _ in range(retry):
        try:
            image = cv2.imread("captcha.png")
            configs = BaseModelConfigs.load("configs.yaml")
            model = ImageToWordModel(model_path="model.onnx", char_list=configs.vocab)
            captcha_text = model.predict(image)
            # print('Solved: ' + str(captcha_text))
            return captcha_text
        except Exception as e:
            print(e)
            continue



if __name__ == "__main__":
    print(str(captcha_ml_solver()))
