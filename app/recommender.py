import os
import pymysql
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv
import pickle
from sqlalchemy import create_engine
def connect_db() -> pd.DataFrame:
    load_dotenv()
    conn = pymysql.connect(
        host='mysql_db',
        port=3306,
        user=os.environ.get("MYSQL_USER"),
        db = os.environ.get("MYSQL_DATABASE"),
        passwd=os.environ.get("MYSQL_PASSWORD"))

    df = pd.read_sql_query("SELECT * FROM final_project.books",
    conn)
    df_copy = df.copy()
    df_copy = df_copy.drop(['id'], axis=1)
    conn.close()
    return df_copy

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    genre_df_dummies = pd.get_dummies(df['genres'])
    df_copy_cleaned = df.drop(['author', 'description', 'language', 'coverImg', 'likedPercent', 'isbn', 'title', 'genres'], axis=1)
    df_copy_merged = pd.concat([genre_df_dummies, df_copy_cleaned], axis=1)
    return df_copy_merged

def normalize_data(data:pd.DataFrame) -> pd.DataFrame:
    min_max_scaler = MinMaxScaler()
    features_encoded = min_max_scaler.fit_transform(data)
    return features_encoded

def generate_df_for_training(encoded_data: np.ndarray):
    df_kmeans = pd.DataFrame(encoded_data, columns = ['comedy', 'environment', 'fantasy', 'fiction', 'health', 'horror',
           'literature', 'nonfiction', 'romance', 'tech', 'food', 'thriller', 'war',
           'rating', 'numRatings'])
    return df_kmeans

def kmeans_model_elaboration(data:pd.DataFrame):
    kmeans = KMeans(n_clusters=5, random_state=0).fit(data)
    return kmeans

def predict(data:pd.DataFrame, df_kmeans: pd.DataFrame ,encoded_data: pd.DataFrame, kmeans) -> pd.DataFrame:
    data['category'] = kmeans.predict(encoded_data)
    df_kmeans['category'] = kmeans.predict(encoded_data)
    return data

def nearest_neighbors_modelisation(data:pd.DataFrame):
    model = NearestNeighbors(n_neighbors=10, algorithm='ball_tree')
    model.fit(data)
    dist, idlist = model.kneighbors(data)
    with open ('./distance.sav', 'wb') as f:
        pickle.dump(dist, f)
    with open ('./idlist.sav', 'wb') as f:
        pickle.dump(idlist, f)
    return dist, idlist

def book_recommendation_engine(book_name):
    book_list_name = []
    book_list_id = []
    book_id = df_copy[df_copy['title'].str.contains(book_name, case=False)].index
    book_id = book_id[0]
    for newid in idlist[book_id]:
        book_list_name.append(df_copy.loc[newid].title)
#     return book_list_name
    return df_copy.iloc[idlist[book_id]]

def insert_to_db(df:pd.DataFrame):
    load_dotenv()
    df = df.reset_index().rename(columns={'index': 'id'})
    df.id = df.id.apply(lambda x : x+1)
    user=os.environ.get("MYSQL_USER")
    db = os.environ.get("MYSQL_DATABASE")
    passwd=os.environ.get("MYSQL_PASSWORD")
    sqlEngine       = create_engine(f"mysql+pymysql://{user}:{passwd}@mysql_db/{db}?charset=utf8mb4")
    dbConnection    = sqlEngine.connect()
    df.to_sql(name='books', con = dbConnection, if_exists = 'replace', chunksize = 1000)
    
def serialize_kmeans(kmeans):
    with open ('./finalized_kmeans.sav', 'wb') as f:
        pickle.dump(kmeans, f)
 
def unserialize_kmeans():
    with open('./finalized_kmeans.sav', 'rb') as f:
        loaded_model = pickle.load(f)
    return loaded_model
    
    
def main():
    if not os.path.exists("./finalized_kmeans.sav"):
        df_copy = connect_db()
        X = preprocess_data(df_copy)
        X = X.drop(['category'], axis=1)
        encoded_data = normalize_data(X)
        df_kmeans = generate_df_for_training(encoded_data)
        kmeans = kmeans_model_elaboration(encoded_data)
        serialize_kmeans(kmeans)
        category_predictions = predict(df_copy, df_kmeans, encoded_data, kmeans)
        dist, idlist = nearest_neighbors_modelisation(df_kmeans)
        insert_to_db(df_copy)
   


if __name__ == '__main__':
    main()
