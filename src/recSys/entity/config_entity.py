from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir : Path
    source_URL : str
    local_data_file : Path
    unzip_dir : Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir : Path
    STATUS_FILE : str
    unzip_data_dir : Path
    schema : dict



@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir : Path
    unzip_data_dir : Path
    transformed_data_dir: Path
    schema: dict
    params: dict



@dataclass(frozen=True)
class ModelTrainConfig:
    root_dir : Path
    train_data_path : Path
    model_path: Path
    schema: dict
    params: dict


@dataclass(frozen=True)
class PredictionConfig:
    model_path: dict
    params: dict
