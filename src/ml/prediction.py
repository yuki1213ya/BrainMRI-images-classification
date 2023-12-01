"""サンプルデータと画像分類モデル"""
import json
from logging import getLogger
from dataclasses import dataclass
import numpy as np
import onnxruntime
import torch
from PIL import Image
from torchvision import transforms
from src.configurations import ModelConfigurations


logger = getLogger(__name__)

@dataclass
class ImageData:
    """サンプルデータのデータクラス"""
    image_filepath: str = "./sample_images/yes_1.jpg"


class Classifier():
    """MRI画像の分類モデル"""
    def __init__(self, model_filepath: str, label_file_path: str) -> None:
        self.model_filepath = model_filepath
        self.label_filepath = label_file_path
        self.classifier = None
        self.label = {}
        self.input_name = ""
        self.output_name = ""
        self.load_model()
        self.load_label()
        self.input_shape = self.classifier.get_inputs()[0].shape

    def transform_image(self, image_filepath: str) -> torch.Tensor:
        """"リクエストされた画像をモデルの入力に合うように変換する"""
        raw_image = Image.open(image_filepath)
        transform = transforms.Compose([transforms.Resize((self.input_shape[2],
                                                           self.input_shape[3])),
                                        transforms.ToTensor(),
                                        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        img_tensor = transform(raw_image)
        img_tensor = img_tensor.unsqueeze(dim=0)
        img_numpy = img_tensor.numpy()
        return img_numpy

    def load_model(self):
        """分類モデルをロードする"""
        logger.info("load model in %s", self.model_filepath)
        self.classifier = onnxruntime.InferenceSession(self.model_filepath)
        self.input_name = self.classifier.get_inputs()[0].name
        self.output_name = self.classifier.get_outputs()[0].name
        logger.info("initialized model")

    def load_label(self):
        """ラベルのjsonファイルをロードする"""
        logger.info("load label in %s", self.label_filepath)
        with open(self.label_filepath, "r", encoding="utf8") as f:
            self.label = json.load(f)
        logger.info("label:%s", self.label)

    def predict(self, image_filepath: str) -> np.ndarray:
        """推論結果を返す"""
        numpy_image = self.transform_image(image_filepath=image_filepath)
        prediction = self.classifier.run(None, {self.input_name: numpy_image})
        prediction = torch.sigmoid(torch.tensor(prediction[0][0]))
        prediction = np.array([prediction[0]/(prediction[0]+prediction[1]),
                               prediction[1]/(prediction[0]+prediction[1])])
        output = np.array(prediction)
        logger.info("predict proba %s", output)
        return output

    def predict_label(self, image_filepath: str) -> str:
        """推論したラベルを返す"""
        prediction = self.predict(image_filepath=image_filepath)
        argmax = np.argmax(prediction)
        return self.label[str(argmax)]


classifier = Classifier(
    model_filepath=ModelConfigurations().model_filepath,
    label_file_path=ModelConfigurations().label_filepath)
