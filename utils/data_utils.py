from .recommendations import Prefiltering
from surprise import Dataset, Reader, accuracy
import pandas as pd
from surprise.model_selection import KFold


def handle_recommender(data):
    reader = Reader(rating_scale=(1, 5))
    data_rating_item_user = data.iloc[:, :3]
    data_preprocessed = Dataset.load_from_df(data_rating_item_user, reader)
    kf = KFold(n_splits=2)
    algo = Prefiltering(data, k=40, min_k=1, sim_options={"user_based":True}, verbose=True)

    mse, mae, rmse = [], [], []
    for trainset, testset in kf.split(data_preprocessed):
        # train and test algorithm.
        algo.fit(trainset)
        predictions = algo.test(testset)
        rmse.append(accuracy.rmse(predictions, verbose=True))
        mae.append(accuracy.mae(predictions, verbose=True))
        mse.append(accuracy.mse(predictions, verbose=True))
        print(mse)
    return {"rmse":rmse, "mae": mae, "mse": mse}