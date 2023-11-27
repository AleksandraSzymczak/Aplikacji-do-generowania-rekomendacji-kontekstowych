
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from utils.model_evaluations import calculate_mae,calculate_recall,calculate_rmse


class Recommender():
    def __init__(self, data, type = None, form_data={}) -> None:
        self.USER_ID = data.columns[0]
        self.ITEM_ID = data.columns[1]
        self.RATING = data.columns[2]
        self.data = data
        self.type = type
        self.form_data = form_data


    def collaborative_filtering(self, user_item_matrix, userid_number_mapping, itemid_number_mapping):
        user_means = user_item_matrix.mean(axis=1).to_frame(name='mean_values')

        centered_matrix = pd.DataFrame(index=user_item_matrix.index, columns=user_item_matrix.columns)
        centered_matrix = user_item_matrix.sub(user_means['mean_values'], axis=0)

        user_similarity = cosine_similarity(centered_matrix)
        
        predicted_ratings = np.zeros_like(user_item_matrix, dtype=float)

        for a in range(user_item_matrix.shape[0] - 1):
            neighbors = np.where(user_similarity[a] > 0)[0]
            
            for i in range(user_item_matrix.shape[1] - 1):
                if i in itemid_number_mapping.index:
                    context_set = self.data[(self.data[self.ITEM_ID] == itemid_number_mapping.loc[i, self.ITEM_ID]) & (self.data[self.USER_ID] == userid_number_mapping.loc[a, self.USER_ID])]
                    if not context_set.empty:
                        context_set_subset = context_set.iloc[:, 2:]
                        data_subset = self.data.iloc[:, 2:]
                        matching_rows = pd.merge(context_set, self.data, left_on=context_set_subset.columns.tolist(), right_on=data_subset.columns.tolist(), how='inner', suffixes=('', '_suffix'))
                        matching_rows = matching_rows[~((matching_rows[self.ITEM_ID] == context_set[self.ITEM_ID].iloc[0]) & (matching_rows[self.USER_ID] == context_set[self.USER_ID].iloc[0]))]

                        unique_itemids = matching_rows[self.ITEM_ID].unique()
                        index_itemids = matching_rows[matching_rows[self.ITEM_ID].isin(unique_itemids)].index
                        unique_userids = matching_rows[self.USER_ID].unique()
                        index_userids = matching_rows[matching_rows[self.USER_ID].isin(unique_userids)].index
                        filtered_neighbors = np.intersect1d(neighbors, np.union1d(index_itemids, index_userids))

                        numerator = np.sum(user_similarity[a, filtered_neighbors] * centered_matrix.iloc[filtered_neighbors, i])
                        denominator = np.sum(user_similarity[a, filtered_neighbors])
                        if denominator != 0:
                            predicted_ratings[a, i] = user_means.iloc[a] + (numerator / (denominator))
                    #else:
                #else:
        return predicted_ratings


    def collaborative_filtering_relaxation(self, user_item_matrix, userid_number_mapping, itemid_number_mapping):
        user_means = user_item_matrix.mean(axis=1).to_frame(name='mean_values')

        centered_matrix = pd.DataFrame(index=user_item_matrix.index, columns=user_item_matrix.columns)
        centered_matrix = user_item_matrix.sub(user_means['mean_values'], axis=0)

        user_similarity = cosine_similarity(centered_matrix)

        predicted_ratings = np.zeros_like(user_item_matrix, dtype=float)

        for a in range(user_item_matrix.shape[0] - 1):
            neighbors = np.where(user_similarity[a] > 0)[0]
            
            for i in range(user_item_matrix.shape[1] - 1):
                if i in itemid_number_mapping.index:
                    context_set = self.data[(self.data[self.ITEM_ID] == itemid_number_mapping.loc[i, self.ITEM_ID]) & (self.data[self.USER_ID] == userid_number_mapping.loc[a, self.USER_ID])]
                    if not context_set.empty:
                        context_set_subset = context_set[self.form_data["c1_choices"]]
                        data_subset = self.data[self.form_data["c1_choices"]]
                        matching_rows = pd.merge(context_set, self.data, left_on=context_set_subset.columns.tolist(), right_on=data_subset.columns.tolist(), how='inner', suffixes=('', '_suffix'))
                        matching_rows = matching_rows[~((matching_rows[self.ITEM_ID] == context_set[self.ITEM_ID].iloc[0]) & (matching_rows[self.USER_ID] == context_set[self.USER_ID].iloc[0]))]

                        unique_itemids = matching_rows[self.ITEM_ID].unique()
                        index_itemids = matching_rows[matching_rows[self.ITEM_ID].isin(unique_itemids)].index
                        unique_userids = matching_rows[self.USER_ID].unique()
                        index_userids = matching_rows[matching_rows[self.USER_ID].isin(unique_userids)].index
                        filtered_neighbors = np.intersect1d(neighbors, np.union1d(index_itemids, index_userids))

                        numerator = np.sum(user_similarity[a, filtered_neighbors] * centered_matrix.iloc[filtered_neighbors, i])
                        denominator = np.sum(user_similarity[a, filtered_neighbors])
                        if denominator != 0:
                            predicted_ratings[a, i] = user_means.iloc[a] + (numerator / (denominator))
 
        return predicted_ratings


    def perform_calculations(self):
        user_item_matrix = self.data.pivot_table(index=self.USER_ID, columns=self.ITEM_ID, values=self.RATING, fill_value=0)
        userid_number_mapping = pd.DataFrame(user_item_matrix.index, columns=[self.USER_ID])
        itemid_number_mapping = pd.DataFrame(user_item_matrix.columns, columns=[self.ITEM_ID])
        if self.type == "DCR":
            predicted_ratings = self.collaborative_filtering_relaxation(
            user_item_matrix, 
            userid_number_mapping, 
            itemid_number_mapping
        )
        else:
            predicted_ratings = self.collaborative_filtering(
                user_item_matrix, 
                userid_number_mapping, 
                itemid_number_mapping
            )
        predicted_ratings_df = pd.DataFrame(
            predicted_ratings, 
            index=user_item_matrix.index, 
            columns=user_item_matrix.columns
            )

        flat_user_item_matrix = user_item_matrix.values.flatten()
        flat_predicted_matrix = predicted_ratings_df.values.flatten()
        mae = calculate_mae(flat_user_item_matrix, flat_predicted_matrix)
        rmse = calculate_rmse(flat_user_item_matrix, flat_predicted_matrix)
        recall_result = calculate_recall(user_item_matrix, predicted_ratings_df)
        return {"mae": mae, "rmse": rmse, "recall_result": recall_result}
