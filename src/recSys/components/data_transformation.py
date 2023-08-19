import os
from recSys import logger
from recSys.entity.config_entity import DataTransformationConfig
from recSys.utils.common import clean_data


class DataTransformation:
    def __init__(self, config = DataTransformationConfig):
        self.config = config
        self.params = config.params

    def clean_data(self):
        config = self.config
        schema = config.schema
        
        try:
            logger.info("<<<<<<< Data Cleaning Started >>>>>>>")
            book_input = config.unzip_data_dir.books
            books_output = config.transformed_data_dir.books
            books_cols = ['title', 'ratings_count', 'average_rating'] 
            print(books_cols)
            clean_data(book_input, books_output, books_cols)

            ratings_input = config.unzip_data_dir.ratings
            ratings_output = config.transformed_data_dir.ratings
            ratings_cols = list(schema.ratings.keys())
            print(ratings_cols)
            clean_data(ratings_input, ratings_output, ratings_cols)

            genre_input = config.unzip_data_dir.genre
            genre_output = config.transformed_data_dir.genre
            genre_cols = list(schema.genre.keys())
            clean_data(genre_input, genre_output, genre_cols)

            genreid_input = config.unzip_data_dir.genre_meta
            genreid_output = config.transformed_data_dir.genre_meta
            genre_cols = list(schema.genre_meta.keys())
            clean_data(genreid_input, genreid_output, genre_cols)

            logger.info(">>>>>>>data cleaning complete <<<<<<<<")

        except Exception as e:
            logger.exception(e)
            raise e


    def get_trusted_users(self):
        config = self.config

        input_path_books = config.transformed_data_dir.clean_books
        input_path_ratings = config.transformed_data_dir.clean_ratings
        output_path = config.transformed_data_dir.trusted_user
        thresh = self.params.trusted_user.min_ratings

        try:
            df_books = pd.read_csv(input_path_books)
            df_ratings = pd.read_csv(input_path_ratings)

            unwanted_users = df_ratings.groupby('user_id')['user_id'].count()
            unwanted_users = unwanted_users[unwanted_users < thresh]
            trusted_users = df_ratings[~df_ratings['user_id'].isin(unwanted_users.index)]
            final_users = trusted_users.copy()
            final_users['title'] = df_books.set_index('id').title.loc[trusted_users.book_id].values
            final_users.to_csv(output_path, index=False)

        except Exception as e:
            logger.exception(e)
            raise e

