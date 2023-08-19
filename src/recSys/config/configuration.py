from recSys.constants import *
from recSys.utils.common import read_yaml, create_directories
from recSys.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainConfig, PredictionConfig
from recSys import logger

class ConfigurationManager:
    def __init__(
        self,
        config_path = CONFIG_FILE_PATH,
        params_path = PARAMS_FILE_PATH,
        schema_path = SCHEMA_FILE_PATH
    ):
        self.config = read_yaml(config_path)
        self.params = read_yaml(params_path)
        self.schema = read_yaml(schema_path)

        create_directories([self.config.artifacts_root])


    def get_data_ingestion_config(self) -> DataIngestionConfig:
            config = self.config.data_ingestion

            create_directories([config.root_dir])

            data_ingestion_config = DataIngestionConfig(
                root_dir = config.root_dir,
                source_URL = config.source_URL,
                local_data_file = config.local_data_file,
                unzip_dir = config.unzip_dir
            )
            return data_ingestion_config


    def get_data_validation_config(self) -> DataValidationConfig:
            config = self.config.data_validation
            schema = self.schema

            create_directories([config.root_dir])

            data_validation_config = DataValidationConfig(
                root_dir = config.root_dir,
                STATUS_FILE = config.STATUS_FILE,
                unzip_data_dir = config.unzip_data_dir,
                schema = schema)
            
            return data_validation_config



    def get_data_transformation_config(self) -> DataTransformationConfig:
            config = self.config.data_transformation

            create_directories([config.root_dir])

            data_transformation_config = DataTransformationConfig(
                root_dir = config.root_dir,
                unzip_data_dir = config.unzip_data_dir,
                transformed_data_dir = config.transformed_data_dir,
                schema = self.schema,
                params = self.params)

            
            return data_transformation_config


    def get_model_train_config(self) -> ModelTrainConfig:
        config = self.config.model_trainer

        create_directories([config.root_dir, config.model_path.simple.root_dir, config.model_path.simple.top_genre_root, config.model_path.content_based.root_dir])

        model_train_config = ModelTrainConfig(
                root_dir = config.root_dir,
                train_data_path = config.train_data_path,
                model_path = config.model_path,
                schema = self.schema,
                params = self.params,)

        return model_train_config

    def get_prediction_config(self):
        config = self.config.model_prediction

        prediction_config = PredictionConfig(
                model_path = config,
                params = self.params)

        return prediction_config
