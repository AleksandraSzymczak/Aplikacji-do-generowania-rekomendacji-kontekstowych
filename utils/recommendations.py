from surprise import AlgoBase
from surprise  import PredictionImpossible
import numpy as np
import heapq
from surprise.prediction_algorithms.knns import SymmetricAlgo



#In our formalism, contextual pre-filtering is achieved by applying contextual constraints
#to C1 only.
class Prefiltering(AlgoBase):
    def __init__(self, data, k=40, min_k=1, sim_options={}, verbose=True, **kwargs):

        SymmetricAlgo.__init__(self, sim_options=sim_options, verbose=verbose, **kwargs)

        self.k = k
        self.min_k = min_k
        self.data = data
        self.columns_to_check = data.iloc[:, 2:].columns.tolist()
        self.USER_COL, self.ITEM_COL, self.RATING = data.iloc[:, :3]
        self.user_rows_to_check = data.iloc[:, 2:].columns.tolist()

    #def map_user_data(data)
    def fit(self, trainset):

        SymmetricAlgo.fit(self, trainset)
        self.sim = self.compute_similarities()
        self.user_id_dict = trainset._raw2inner_id_users
        self.item_id_dict = trainset._raw2inner_id_items
        self.means = np.zeros(self.n_x)
        for x, ratings in self.xr.items():
            self.means[x] = np.mean([r for (_, r) in ratings])

        self.data_temp = self.data.copy()
        self.data_temp.loc[:, self.USER_COL] = self.data_temp[self.USER_COL].map(self.user_id_dict)
        self.data_temp = self.data_temp.dropna(subset=[self.USER_COL])
        self.data_temp.loc[:, self.USER_COL] = self.data_temp[self.USER_COL].astype(int)

        self.data_temp.loc[:, self.ITEM_COL] = self.data_temp[self.ITEM_COL].map(self.item_id_dict)
        self.data_temp = self.data_temp.dropna(subset=[self.ITEM_COL])
        self.data_temp.loc[:, self.ITEM_COL] = self.data_temp[self.ITEM_COL].astype(object)
        return self


    def filter_users(self, group, user_row):
        return (group[self.user_rows_to_check].eq(user_row[self.user_rows_to_check]).all(axis=1)).any()


    def estimate(self, u, i):

        if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            raise PredictionImpossible("User and/or item is unknown.")

        x, y = u, i # u i lub i u
        user_rows_to_check = self.data_temp[(
            self.data_temp[self.USER_COL] == x) 
            & (self.data_temp[self.ITEM_COL] == y)
            ]
        #print(self.data)
        # Sprawdź, czy istnieją użytkownicy do sprawdzenia
        if not user_rows_to_check.empty:
            # Grupowanie i filtrowanie
            similar_users = self.data_temp.groupby('User').filter(lambda x: self.filter_users(x, user_rows_to_check.iloc[0]))[self.USER_COL].to_list()
            similar_users = list(set(similar_users))
            self.yr = {key: [(x, r) for (x, r) in value if x in similar_users] for key, value in self.yr.items()}
            # Wydrukuj wyniki
            print(similar_users)
        else:
            print(f'Brak danych dla użytkownika {x} i przedmiotu {y}')
        
        
        neighbors = [(x2, self.sim[x, x2], r) for (x2, r) in self.yr[y]]
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