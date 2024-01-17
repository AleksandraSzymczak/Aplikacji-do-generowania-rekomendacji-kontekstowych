from surprise import AlgoBase
from surprise  import PredictionImpossible
import numpy as np
import heapq
from surprise.prediction_algorithms.knns import SymmetricAlgo



#In our formalism, contextual pre-filtering is achieved by applying contextual constraints
#to C1 only.
class DCR(AlgoBase):
    def __init__(self, user_filtered_user_mapping_c1, user_filtered_user_mapping_c2, rating_filtered_mapping_c2, user_filtered_user_mapping_c3, data, k=40, min_k=1, sim_options={}, verbose=True, **kwargs):

        SymmetricAlgo.__init__(self, sim_options=sim_options, verbose=verbose, **kwargs)

        self.k = k
        self.min_k = min_k
        self.data = data
        self.columns_to_check = data.iloc[:, 2:].columns.tolist()
        self.USER_COL, self.ITEM_COL, self.RATING = data.iloc[:, :3]
        self.user_rows_to_check = data.iloc[:, 2:].columns.tolist()
        self.C1 = user_filtered_user_mapping_c1
        self.C2 = user_filtered_user_mapping_c2
        self.C3 = user_filtered_user_mapping_c3
        self.rating_filtered_mapping_c2 = rating_filtered_mapping_c2


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
        result_list = self.C1[(x_mapping, y_mapping)]
        
        mapped_result_list = [self.user_id_dict[x] for x in result_list if x in self.user_id_dict]

        neighbors = [(x2, self.sim[x, x2], r) for (x2, r) in self.yr[y] if x2 in mapped_result_list]
        k_neighbors = heapq.nlargest(self.k, neighbors, key=lambda t: t[1])
        #est = self.means[x]
        est = self.C3.get((x_mapping, y_mapping), 0)
        # compute weighted average
        sum_sim = sum_ratings = actual_k = 0
        denominator = self.C2.get((x_mapping, y_mapping), 0)
        mapped_denominator = [self.user_id_dict[x] for x in denominator if x in self.user_id_dict]

        for (nb, sim, r) in k_neighbors:
            if sim > 0:
                sum_sim += sim
                if nb in mapped_denominator:
                  nb_mapping = list(self.user_id_dict.keys())[list(self.user_id_dict.values()).index(nb)]
                  sum_ratings += sim * (r - self.rating_filtered_mapping_c2.get((nb_mapping, y_mapping), 0))
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