import os
import joblib
from recSys import logger
from recSys.entity.config_entity import ModelTrainConfig
import pandas as pd
from recSys.utils.common import create_directories
from recSys import logger
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

class ModelTrainer:
    def __init__(self, config = ModelTrainConfig):
        self.config = config
        self.params = config.params


    def find_popular_overall(self):
        try:
            logger.info("-----Model training for top popular books started-------")
            THRESH = self.params.simple_recommender.ratings_cutoff
            TOP = self.params.simple_recommender.top
            
            input_path_books = self.config.train_data_path.books
            output_path = self.config.model_path.simple.top_books
     
            logger.info(f"{input_path_books} accessed for model training")
            df_books = pd.read_csv(input_path_books)

            v = df_books['ratings_count']
            m = df_books['ratings_count'].quantile(THRESH)
            R = df_books['average_rating']
            C = df_books['average_rating'].mean()
            W = (R*v + C*m) / (v + m)

            df_books['weighted_rating'] = W
            top_books = df_books.sort_values('weighted_rating', ascending=False).head(TOP)
            top_books = top_books[['title', 'authors', 'average_rating', 'weighted_rating', 'image_url']]
            
            top_books.to_csv(output_path, index=False)
            logger.info(f"------Final output is saved to {output_path} ------")
        except Exception as e:
            logger.exception(e)
            raise e

    def find_popular_in_genre(self):
        try:
            logger.info("MOdel training started for finding top books in given genre")
            GENRES = list(self.params.simple_recommender.genres)
            genres = list(map(str.lower, GENRES))
            THRESH = self.params.simple_recommender.genre_cut_off

            input_path_genre = self.config.train_data_path.genre
            input_path_genre_meta = self.config.train_data_path.genre_meta
            input_path_books = self.config.train_data_path.books
            output_path = self.config.model_path.simple.top_genre_root

            df_books = pd.read_csv(input_path_books)
            df_genreId = pd.read_csv(input_path_genre_meta)
            df_genre = pd.read_csv(input_path_genre)

            available_genres = df_genreId.loc[df_genreId.tag_name.str.lower().isin(genres)]
            available_genres_books = df_genre[df_genre.tag_id.isin(available_genres.tag_id)]
            top_books = available_genres_books.copy()
            top_books['genre'] = available_genres.tag_name.loc[top_books.tag_id].values

            def find_top(genre, percentile= THRESH):
                df = top_books[top_books['genre'] == genre.lower()]
                qualified = df_books.set_index('book_id').loc[df.goodreads_book_id]

                v = qualified['ratings_count']
                m = qualified['ratings_count'].quantile(percentile)
                R = qualified['average_rating']
                C = qualified['average_rating'].mean()
                qualified['weighted_rating'] = (R*v + C*m) / (v + m)

                qualified.sort_values('weighted_rating', ascending=False, inplace=True)
                final = qualified[['title','authors','average_rating', 'weighted_rating', 'image_url']]

                path = genre.lower().replace(" ", "-") + '.csv'
                output_path_genre = os.path.join(output_path, path)
                final.to_csv(output_path_genre, index=False)
                logger.info(f"top books for genre: {genre} is saved to {output_path_genre}")

            for g in GENRES:
                find_top(g, THRESH)

            logger.info("<<<<<<Model training completed for finding top books in given genre>>>>>")
        
        except Exception as e:
            logger.exception(e)
            raise e


    def content_based_recommender(self):
        try:
            logger.info(">>>>>>Model training has started for content_based_recommender<<<<<<<")
            input_path_books = self.config.train_data_path.books
            input_path_genre = self.config.train_data_path.genre
            input_path_genre_meta = self.config.train_data_path.genre_meta
            output_path = self.config.model_path.content_based.model_path

            df_books = pd.read_csv(input_path_books)
            df_genreId = pd.read_csv(input_path_genre_meta)
            df_genre = pd.read_csv(input_path_genre)

            df_books['authors-comb'] = df_books['authors'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x.split(', ')])

            def get_genres(x):
                t = df_genre[df_genre.goodreads_book_id==x]
                return [i.lower().replace(" ", "") for i in df_genreId.tag_name.loc[t.tag_id].values]

            df_books['genres'] = df_books.book_id.apply(get_genres)
            df_books['mix'] = df_books.apply(lambda x: ' '.join([x['title']] + x['authors-comb'] + x['genres']), axis=1)

            count = TfidfVectorizer()
            count_matrix = count.fit_transform(df_books['mix'])
            cosine_sim = cosine_similarity(count_matrix, count_matrix)
            
            joblib.dump(cosine_sim, output_path)
            logger.info(f"similarity matrix has been saved to: {output_path}")

            logger.info(">>>>>>Model training has finished for content_based_recommender<<<<<<<")
        except Exception as e:
            logger.exception(e)
            raise e
