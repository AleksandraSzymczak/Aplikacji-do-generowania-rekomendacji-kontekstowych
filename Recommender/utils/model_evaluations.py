import pandas as pd
import numpy as np

def calculate_recall(relevant_items, recommended_items):
    merged_df = pd.merge(relevant_items, recommended_items, on='userid', how='inner')

    true_positives = len(merged_df)
    false_negatives = len(relevant_items) - true_positives

    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) != 0 else 0
    return recall


def calculate_mae(user_item_matrix, predicted_matrix):
    mae = np.mean(np.abs(user_item_matrix - predicted_matrix))
    return mae


def calculate_rmse(user_item_matrix, predicted_matrix):
    rmse = np.sqrt(np.mean((user_item_matrix - predicted_matrix)**2))
    return rmse