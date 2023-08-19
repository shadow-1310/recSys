from recSys.entity.config_entity import PredictionConfig
from recSys import logger
from recSys.config.configuration import ConfigurationManager
import pandas as pd
from pathlib import Path
import joblib
import os

class PredictionPipeline():
    def __init__(self):
        c = ConfigurationManager()
        self.config = c.get_prediction_config()
        self.params = self.config.params

    def find_popular_overall(self):
        try:
            path = self.config.model_path.simple.top_books
            need = self.params.simple_recommender.show_results
            logger.info(f"Searching for top {need} Popular Books in overall")

            df = pd.read_csv(path, nrows= need)
            logger.info(f"returned top {need} popular books")
            return df
        except Exception as e:
            logger.exception(e)
            raise e

    def find_popular_in_genre(self, genre):
        try:
            need = self.params.simple_recommender.show_results
            root = self.config.model_path.simple.top_genre_root
            path = genre.lower().replace(" ", "-") + '.csv'
            input_path = os.path.join(root, path)

            df = pd.read_csv(input_path, nrows= need)
            return df
        except Exception as e:
            logger.exception(e)
            raise e


    def content_based_recommender(self, title):
        try:
            books_path = self.config.model_path.content_based.books
            sim_matrix_path = self.config.model_path.content_based.model_path

            df_books = pd.read_csv(books_path)
            cosine_sim = joblib.load(Path(sim_matrix_path))

            SIM_WEIGHT = self.params.content_based_recommender.similarity_weight
            POP_WEIGHT = self.params.content_based_recommender.popularity_weight
            N = self.params.content_based_recommender.show_results

            logger.info(f"trying to find recommendation for '{title}' based on similarity include of {SIM_WEIGHT} and popularity weight of {POP_WEIGHT}")

            indices = pd.Series(df_books.index, index=df_books['title'])
            titles = df_books['title']
            idx = indices[title]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:SIM_WEIGHT]
            book_indices = [i[0] for i in sim_scores]
            df = df_books.iloc[book_indices][['title', 'ratings_count', 'average_rating', 'authors','image_url']]

            v = df['ratings_count']
            m = df['ratings_count'].quantile(POP_WEIGHT)
            R = df['average_rating']
            C = df['average_rating'].mean()
            df['weighted_rating'] = (R*v + C*m) / (v + m)
            
            qualified = df[df['ratings_count'] >= m]
            qualified = qualified.sort_values('weighted_rating', ascending=False)

            logger.info(f"Recommendation generated for the title: '{title}', found {qualified.shape[0]} books")
            return qualified.head(N)
        except Exception as e:
            logger.exception(e)
            raise e
