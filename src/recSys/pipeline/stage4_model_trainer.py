
from recSys.entity.config_entity import ModelTrainConfig
from recSys import logger
from recSys.components.model_trainer import ModelTrainer
from recSys.config.configuration import ConfigurationManager

STAGE_NAME = "Model Training Stage"

class ModelTrainerPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_train_config = config.get_model_train_config()
        
        model_trainer = ModelTrainer(config = model_train_config)
        model_trainer.find_popular_overall()
        model_trainer.find_popular_in_genre()
        model_trainer.content_based_recommender()


if __name__ == '__main__':
    try:
        logger.info(f"<<<<< {STAGE_NAME} started >>>>>")
        obj = ModelTrainerPipeline()
        obj.main()
        logger.info(f">>>>>> {STAGE_NAME} completed successfully <<<<<<")

    except Exception as e:
        logger.exception(e)
        raise e

