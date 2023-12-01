"""APIのルーター"""
import uuid
from logging import getLogger
from typing import Any, Dict, List
import torch

from fastapi import APIRouter
from src.ml.prediction import ImageData, classifier

logger = getLogger(__name__)
router = APIRouter()

@router.get("/health")
def health_check() -> Dict[str, str]:
    """APIのヘルスチェック"""
    return {"health": "ok"}

@router.get("/metadata")
def metadata() -> Dict[str, Any]:
    """メタデータを返す"""
    return {
      "input_type": "torch.tensor",
      "input_structure": "(1, 3, 480, 480)",
      "prediction_type": "float32",
      "prediction_structure": "(1,2)",
      "prediction_sample": [0.8, 0.2],
    }

@router.get("/label")
def label() -> Dict[int, str]:
    """予測するラベルの一覧を返す"""
    return classifier.label

@router.get("/predict/test")
def predict_test() -> Dict[str, List[float]]:
    """サンプルデータを使って予測できるかテストする"""
    job_id = str(uuid.uuid4())
    prediction = classifier.predict(image_filepath=ImageData().image_filepath)
    prediction_list = list(prediction)
    logger.info("test %s:%s", job_id, prediction_list)
    return {"prediction": prediction_list}

@router.post("/predict")
def predict(image_filepath: ImageData) -> Dict[str, List[float]]:
    """脳のMRI画像データをリクエストして、腫瘍の有無の確率を予測する"""
    job_id = str(uuid.uuid4())
    prediction = classifier.predict(image_filepath=image_filepath.image_filepath)
    prediction_list = list(prediction)
    logger.info("test %s:%s", job_id, prediction_list)
    return {"prediction": prediction_list}

@router.post("/predict/label")
def predict_label(image_filepath: ImageData) -> Dict[str, str]:
    """脳のMRI画像データをリクエストして、腫瘍の有無を予測する"""
    job_id = str(uuid.uuid4())
    prediction = classifier.predict_label(image_filepath=image_filepath.image_filepath)
    logger.info("test %s:%s", job_id, prediction)
    return {"prediction": prediction}
