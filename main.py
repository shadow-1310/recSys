from recSys import logger
from recSys.pipeline.stage1_data_ingestion import DataIngestionPipeline
from  recSys.pipeline.stage2_data_validation import DataValidationPipeline

STAGE_NAME = "DATA Ingestion Stage"

try:
    logger.info(f"<<<<< {STAGE_NAME} started >>>>>")
    obj = DataIngestionPipeline()
    obj.main()
    logger.info(f">>>>>> {STAGE_NAME} completed successfully <<<<<<")

except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = "Data Validation Stage"

try:
    logger.info(f"<<<<< {STAGE_NAME} started >>>>>")
    obj = DataValidationPipeline()
    obj.main()
    logger.info(f">>>>>> {STAGE_NAME} completed successfully <<<<<<")

except Exception as e:
    logger.exception(e)
    raise e

