from surprise import AlgoBase
from surprise  import PredictionImpossible
import numpy as np
import heapq
from surprise.prediction_algorithms.knns import SymmetricAlgo
import json


class Pre_filtering(AlgoBase):
    def __init__(self, user_filtered_user_mapping, data, k=40, min_k=1, sim_options={}, verbose=True, **kwargs):

        SymmetricAlgo.__init__(self, sim_options=sim_options, verbose=verbose, **kwargs)

        self.k = k
        self.min_k = min_k
        self.user_filtered_user_mapping = user_filtered_user_mapping
        self.data = data
        self.columns_to_check = data.iloc[:, 2:].columns.tolist()
        self.USER_COL, self.ITEM_COL, self.RATING = data.iloc[:, :3]
        self.columns_to_compare = data.iloc[:, 3:4].columns.tolist()


    def fit(self, trainset):

        SymmetricAlgo.fit(self, trainset)
        self.sim = self.compute_similarities()
        self.user_id_dict = trainset._raw2inner_id_users
        self.item_id_dict = trainset._raw2inner_id_items
        self.means = np.zeros(self.n_x)
        for x, ratings in self.xr.items():
            self.means[x] = np.mean([r for (_, r) in ratings])

        return self


    def filter_users(self, group, user_row):
        return (group[self.user_rows_to_check].eq(user_row[self.user_rows_to_check]).all(axis=1)).any()


    def estimate(self, u, i):

        if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            raise PredictionImpossible("User and/or item is unknown.")

        x, y = u, i # u i lub i u
        x_mapping = list(self.user_id_dict.keys())[list(self.user_id_dict.values()).index(x)]
        y_mapping = list(self.item_id_dict.keys())[list(self.item_id_dict.values()).index(y)]
        result_list = self.user_filtered_user_mapping[(x_mapping, y_mapping)]
        
        mapped_result_list = [self.user_id_dict[x] for x in result_list if x in self.user_id_dict]

        neighbors = [(x2, self.sim[x, x2], r) for (x2, r) in self.yr[y] if x2 in mapped_result_list]
        k_neighbors = heapq.nlargest(self.k, neighbors, key=lambda t: t[1])
        est = self.means[x]

        # compute weighted average
        sum_sim = sum_ratings = actual_k = 0
        for (nb, sim, r) in k_neighbors:
            if sim > 0:
                sum_sim += sim
                sum_ratings += sim * (r - self.means[nb])
                actual_k += 1

        if actual_k < self.min_k:
            sum_ratings = 0

        try:
            est += sum_ratings / sum_sim
        except ZeroDivisionError:
            pass  # return mean

        details = {"actual_k": actual_k}
        return est, details

    
#trzeba to samo co w KNNWithMeans ale neighbor selection ma byc filtrowane tylko