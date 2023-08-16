from recSys.entity.config_entity import DataValidationConfig
from recSys import logger
from recSys.components.data_validation import DataValidation
from recSys.config.configuration import ConfigurationManager

STAGE_NAME = "Data Validation Stage"

class DataValidationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        
        data_validation = DataValidation(config = data_validation_config)
        data_validation.validate_data()



if __name__ == '__main__':
    try:
        logger.info(f"<<<<< {STAGE_NAME} started >>>>>")
        obj = DataValidationPipeline()
        obj.main()
        logger.info(f">>>>>> {STAGE_NAME} completed successfully <<<<<<")

    except Exception as e:
        logger.exception(e)
        raise e

