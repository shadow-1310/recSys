from recSys import logger
from recSys.pipeline.stage1_data_ingestion import DataIngestionPipeline
from  recSys.pipeline.stage2_data_validation import DataValidationPipeline
from recSys.pipeline.stage3_data_transformation import DataTransformationPipeline
from recSys.pipeline.stage4_model_trainer import ModelTrainerPipeline
from recSys.pipeline.prediction import PredictionPipeline

# STAGE_NAME = "DATA Ingestion Stage"

# try:
#     logger.info(f"<<<<< {STAGE_NAME} started >>>>>")
#     obj = DataIngestionPipeline()
#     obj.main()
#     logger.info(f">>>>>> {STAGE_NAME} completed successfully <<<<<<")

# except Exception as e:
#     logger.exception(e)
#     raise e



# STAGE_NAME = "Data Validation Stage"

# try:
#     logger.info(f"<<<<< {STAGE_NAME} started >>>>>")
#     obj = DataValidationPipeline()
#     obj.main()
#     logger.info(f">>>>>> {STAGE_NAME} completed successfully <<<<<<")

# except Exception as e:
#     logger.exception(e)
#     raise e


# STAGE_NAME = "Data Transformation Stage"

# try:
#     logger.info(f"<<<<< {STAGE_NAME} started >>>>>")
#     obj = DataTransformationPipeline()
#     obj.main()
#     logger.info(f">>>>>> {STAGE_NAME} completed successfully <<<<<<")

# except Exception as e:
#     logger.exception(e)
#     raise e



# STAGE_NAME = "Model Training Stage"

# try:
#     logger.info(f"<<<<< {STAGE_NAME} started >>>>>")
#     obj = ModelTrainerPipeline()
#     obj.main()
#     logger.info(f">>>>>> {STAGE_NAME} completed successfully <<<<<<")

# except Exception as e:
#     logger.exception(e)
#     raise e



try:
    obj = PredictionPipeline()
    # print(obj.find_popular_in_genre("Mystery"))
    # TITLE = "Pines (Wayward Pines, #1)"
    TITLE = "Ready Player One"
    print(obj.content_based_recommender(TITLE))

except Exception as e:
    logger.exception(e)
    raise e
