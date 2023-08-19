from recSys.entity.config_entity import DataTransformationConfig
from recSys import logger
from recSys.components.data_transformation import DataTransformation
from recSys.config.configuration import ConfigurationManager

STAGE_NAME = "Data Transformation Stage"

class DataTransformationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        
        data_transformation = DataTransformation(config = data_transformation_config)
        data_transformation.clean_data()



if __name__ == '__main__':
    try:
        logger.info(f"<<<<< {STAGE_NAME} started >>>>>")
        obj = DataTransformationPipeline()
        obj.main()
        logger.info(f">>>>>> {STAGE_NAME} completed successfully <<<<<<")

    except Exception as e:
        logger.exception(e)
        raise e

