import os
from recSys import logger
from recSys.entity.config_entity import DataValidationConfig
from recSys.utils.common import validate_data

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_data(self) -> bool:
        path = self.config.unzip_data_dir
        files = path.keys()
        status_file = self.config.STATUS_FILE
        schema = self.config.schema

        status = True
        
        try:
            with open(status_file, "w") as file:
                    logger.info(f"Accesed file {status_file} for making validation status")
            for f in files:
                curr_status = validate_data(path[f], schema[f])
                with open(status_file, "a") as file:
                    file.write(f"Validation status for {f}: {curr_status}\n")
            
                status = status and curr_status
            
            print(status)
        
        except Exception as e:
            logger.exception(e)
            raise e           
