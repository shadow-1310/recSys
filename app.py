from flask import Flask, render_template, request
from recSys.pipeline.prediction import PredictionPipeline
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    obj = PredictionPipeline()
    data = obj.find_popular_overall()
    
    return render_template('index.html',
            title = list(data['title'].values),
            author = list(data['authors'].values),
            image = list(data['image_url'].values),
            rating = list(data['average_rating'].values)
            )


@app.route('/top_genre')
def genre_ui():
    obj = PredictionPipeline()
    genres = list(obj.params.simple_recommender.genres)
    return render_template('top_in_genre.html',
            options = genres)


@app.route('/recommend_genre', methods=['post'])
def recommend_genre():
    obj = PredictionPipeline()
    genres = list(obj.params.simple_recommender.genres)
    user_input = request.form.get('user_input')
    data = obj.find_popular_in_genre(user_input)

    return render_template('top_in_genre.html',
            options = genres,
            title = list(data['title'].values),
            author = list(data['authors'].values),
            image = list(data['image_url'].values),
            rating = list(data['average_rating'].values)
            )


@app.route('/content_based')
def content_ui():
    obj = PredictionPipeline()
    path = obj.config.model_path.content_based.books
    books = pd.read_csv(path)
    books = list(books['title'].values)

    return render_template('content_based_recommender.html',
            options = books)

@app.route('/content_based_recommender', methods=['post'])
def content_recommender():
    obj = PredictionPipeline()
    path = obj.config.model_path.content_based.books
    books = pd.read_csv(path)
    books = list(books['title'].values)
    user_input = request.form.get('user_input')
    data = obj.content_based_recommender(user_input)

    return render_template('content_based_recommender.html',
            options = books,
            title = list(data['title'].values),
            author = list(data['authors'].values),
            image = list(data['image_url'].values),
            rating = list(data['average_rating'].values)
            )
if __name__ == '__main__':
    app.run(debug=True)



