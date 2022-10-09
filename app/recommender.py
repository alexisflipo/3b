import os
import pymysql
from yellowbrick.cluster import KElbowVisualizer, InterclusterDistance
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv
import pickle
from sqlalchemy import create_engine
import mlflow
import logging
import traceback
from flask_mail import Message
from flask import jsonify

def connect_db() -> pd.DataFrame:
    load_dotenv()
    user = os.environ.get("MYSQL_USER")
    db = os.environ.get("MYSQL_DATABASE")
    passwd = os.environ.get("MYSQL_PASSWORD")
    host = "mysql_db"
    sqlEngine = create_engine(f"mysql+pymysql://{user}:{passwd}@{host}/{db}")
    dbConnection = sqlEngine.connect()

    df = pd.read_sql_query("SELECT * FROM final_project.books", con=dbConnection)
    df_copy = df.copy()
    df_copy = df_copy.drop(["id"], axis=1)
    return df_copy


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    genre_df_dummies = pd.get_dummies(df["genres"])
    df_copy_cleaned = df.drop(
        [
            "author",
            "description",
            "language",
            "coverImg",
            "likedPercent",
            "isbn",
            "title",
            "genres",
        ],
        axis=1,
    )
    df_copy_merged = pd.concat([genre_df_dummies, df_copy_cleaned], axis=1)
    return df_copy_merged


def normalize_data(data: pd.DataFrame) -> pd.DataFrame:
    min_max_scaler = MinMaxScaler()
    features_encoded = min_max_scaler.fit_transform(data)
    return features_encoded


def generate_df_for_training(encoded_data: np.ndarray):
    df_kmeans = pd.DataFrame(
        encoded_data,
        columns=[
            "comedy",
            "environment",
            "fantasy",
            "fiction",
            "health",
            "horror",
            "literature",
            "nonfiction",
            "romance",
            "tech",
            "food",
            "thriller",
            "war",
            "rating",
            "numRatings",
        ],
    )
    return df_kmeans


def kmeans_model_elaboration(data: pd.DataFrame):
    kmeans = KMeans(n_clusters=5, random_state=0).fit(data)
    return kmeans


def predict(
    data: pd.DataFrame, df_kmeans: pd.DataFrame, encoded_data: pd.DataFrame, kmeans
) -> pd.DataFrame:
    data["category"] = kmeans.predict(encoded_data)
    df_kmeans["category"] = kmeans.predict(encoded_data)
    return data


def nearest_neighbors_modelisation(data: pd.DataFrame):
    model = NearestNeighbors(n_neighbors=10, algorithm="ball_tree")
    model.fit(data)
    dist, idlist = model.kneighbors(data)
    with open("./distance.sav", "wb") as f:
        pickle.dump(dist, f)
    with open("./idlist.sav", "wb") as f:
        pickle.dump(idlist, f)
    return dist, idlist


def insert_to_db(df: pd.DataFrame):
    load_dotenv()
    df = df.reset_index().rename(columns={"index": "id"})
    user = os.environ.get("MYSQL_USER")
    db = os.environ.get("MYSQL_DATABASE")
    passwd = os.environ.get("MYSQL_PASSWORD")
    host = "mysql_db"
    sqlEngine = create_engine(
        f"mysql+pymysql://{user}:{passwd}@{host}/{db}?charset=utf8mb4"
    )
    dbConnection = sqlEngine.connect()
    df.to_sql(name="books", con=dbConnection, if_exists="replace", chunksize=1000)


def serialize_kmeans(kmeans):
    with open("./finalized_kmeans.sav", "wb") as f:
        pickle.dump(kmeans, f)


def unserialize_kmeans(path):
    with open(path, "rb") as f:
        loaded_model = pickle.load(f)
    return loaded_model


def unserialize_list(path: os.PathLike):
    with open(path, "rb") as f:
        return pickle.load(f)


def set_experiment_if_not_exists(experiment_name):
    existing_exp = mlflow.get_experiment_by_name(experiment_name)
    if not existing_exp:
        mlflow.create_experiment(experiment_name)
    mlflow.set_experiment(experiment_name)


def generate_silhouette_img(encoded_data):
    fig = plt.figure(figsize=(15, 10))
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(2, 10), metric="silhouette")

    visualizer.fit(encoded_data)  # Fit the data to the visualizer
    visualizer.show()
    kmeans_img = "silhouette.jpg"
    fig.savefig(kmeans_img)


def generate_interclusterdistance_img(encoded_data):
    fig = plt.figure(figsize=(15, 10))
    model = KMeans(5)
    visualizer = InterclusterDistance(model)
    visualizer.fit(encoded_data)  # Fit the data to the visualizer
    visualizer.show()
    distance_img = "interclusterdistance.jpg"
    fig.savefig(distance_img)


from run import application, mail
    
def send_mail(text):
    msg = Message("Hello",
                  sender="support@beginsbetter.com",
                  recipients=["alexis.flipo1@gmail.com"])
    msg.body = f"{text}"
    msg.html = f"<b>{text}</b>"
    mail.send(msg)
    return jsonify(status_code=200, content={"message": "email has been sent"})

@application.before_first_request
def main():
    if not os.path.exists("./finalized_kmeans.sav"):
        df_copy = connect_db()
        X = preprocess_data(df_copy)
        X = X.drop(["category"], axis=1)
        encoded_data = normalize_data(X)
        generate_silhouette_img(encoded_data)
        generate_interclusterdistance_img(encoded_data)
        df_kmeans = generate_df_for_training(encoded_data)
        kmeans = kmeans_model_elaboration(encoded_data)
        serialize_kmeans(kmeans)
        score = kmeans.score(df_kmeans)
        category_predictions = predict(df_copy, df_kmeans, encoded_data, kmeans)
        nearest_neighbors_modelisation(df_kmeans)
        insert_to_db(df_copy)
        try:
            mlflow.set_tracking_uri("https://mlflow-app.beginsbetter.com:80")
            set_experiment_if_not_exists("books-recommender-1")
            experiment = mlflow.get_experiment_by_name("books-recommender-1")
            with mlflow.start_run(experiment_id=experiment.experiment_id):
                mlflow.log_metric("Score sklearn", score)
                mlflow.log_artifact("./silhouette.jpg", artifact_path="silhouette")
                mlflow.log_artifact(
                    "./interclusterdistance.jpg", artifact_path="interclusterdistance"
                )
                mlflow.sklearn.log_model(
                    sk_model=kmeans, artifact_path="", registered_model_name="kmeans"
                )
            send_mail('Training finished successfully')   
        except Exception as e:
            logging.error(traceback.format_exc())
            send_mail(f"An error occured, the training did not success. Error:  {e}. {traceback.format_exc()}")   
