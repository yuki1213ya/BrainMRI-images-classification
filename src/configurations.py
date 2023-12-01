"""モデルとAPIの設定ファイル"""
import os
from logging import getLogger
from dataclasses import dataclass

logger = getLogger(__name__)

@dataclass
class ModelConfigurations:
    """分類モデルの設定クラス"""
    model_filepath: str = os.getenv("MODEL_FILEPATH")
    label_filepath: str = os.getenv("LABEL_FILEPATH")

@dataclass
class APIConfigurations:
    """APIの設定クラス"""
    title: str = os.getenv("API_TITLE", "image-classification-API")
    description: str = os.getenv("API_DESCRIPTION", "BrainMRI-image-classification")
    version: str = os.getenv("API_VERSION", "0.1")
