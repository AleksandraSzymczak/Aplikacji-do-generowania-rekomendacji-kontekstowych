from django.shortcuts import render
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from utils.model_evaluations import calculate_mae,calculate_recall,calculate_rmse
from MainPage.models import UploadedFile


def prefiltering_page(request):
    pierwszy_plik = UploadedFile.objects.first()
    file_path = pierwszy_plik.get_file_path()
    df = pd.read_csv(file_path) 
    context_var_list = df.columns[3:].tolist()
    #result = perform_calculations(selected_file)
    #print(result)
    return render(request, 'Prefiltering/prefiltering_page.html', {'context_list': context_var_list})


def perform_calculations(data):
    user_item_matrix = data.pivot_table(index='userid', columns='itemid', values='rating', fill_value=0)
    userid_number_mapping = pd.DataFrame(user_item_matrix.index, columns=['userid'])
    itemid_number_mapping = pd.DataFrame(user_item_matrix.columns, columns=['itemid'])

    predicted_ratings = collaborative_filtering(user_item_matrix, data, userid_number_mapping,itemid_number_mapping)
    predicted_ratings = collaborative_filtering(user_item_matrix, data, userid_number_mapping,itemid_number_mapping)
    predicted_ratings_df = pd.DataFrame(predicted_ratings, index=user_item_matrix.index, columns=user_item_matrix.columns)

    flat_user_item_matrix = user_item_matrix.values.flatten()
    flat_predicted_matrix = predicted_ratings_df.values.flatten()
    mae = calculate_mae(flat_user_item_matrix - flat_predicted_matrix)
    rmse = calculate_rmse(flat_user_item_matrix - flat_predicted_matrix)
    recall_result = calculate_recall(user_item_matrix, predicted_ratings_df)
    return {"mae": mae, "rmse": rmse, "recall_result": recall_result}


def collaborative_filtering(user_item_matrix, data, userid_number_mapping, itemid_number_mapping):
    user_means = user_item_matrix.mean(axis=1).to_frame(name='mean_values')

    centered_matrix = pd.DataFrame(index=user_item_matrix.index, columns=user_item_matrix.columns)
    centered_matrix = user_item_matrix.sub(user_means['mean_values'], axis=0)

    user_similarity = cosine_similarity(centered_matrix)

    predicted_ratings = np.zeros_like(user_item_matrix, dtype=float)

    for a in range(user_item_matrix.shape[0]):

        neighbors = np.where(user_similarity[a] > 0)[0]

        for i in range(user_item_matrix.shape[1]):
            context_set = data[(data['itemid'] == itemid_number_mapping.loc[i, 'itemid']) & (data['userid'] == userid_number_mapping.loc[a, 'userid'])]
            if not context_set.empty:
                matching_rows = data[
                    (data['Time'] == context_set['Time'].values[0]) &
                    (data['Location'] == context_set['Location'].values[0]) &
                    (data['Companion'] == context_set['Companion'].values[0])
                ]
                unique_itemids = matching_rows['itemid'].unique()
                index_itemids = matching_rows[matching_rows['itemid'].isin(unique_itemids)].index
                unique_userids = matching_rows['userid'].unique()
                index_userids = matching_rows[matching_rows['userid'].isin(unique_userids)].index
                filtered_neighbors = np.intersect1d(neighbors, np.union1d(index_itemids, index_userids))
                
                numerator = np.sum(user_similarity[a, filtered_neighbors] * centered_matrix.iloc[filtered_neighbors, i])
                denominator = np.sum(user_similarity[a, filtered_neighbors])
                if denominator != 0:
                    predicted_ratings[a, i] = user_means.iloc[a] + (numerator / (denominator))
    return predicted_ratings