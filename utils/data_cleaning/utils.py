from scipy import stats


def scale_ratings(ratings, new_min, new_max):
    old_min = min(ratings)
    old_max = max(ratings)

    scaled_ratings = [
        ((rating - old_min) * (new_max - new_min) / (old_max - old_min)) + new_min
        for rating in ratings
    ]

    return scaled_ratings


def z_score_normalisation(RATING_Z_SCORE, threshold):
    z_scores = stats.zscore(RATING_Z_SCORE)
    outliers = (z_scores > threshold) | (z_scores < -threshold)
    return outliers

def drop_duplicates(df, USER_COL, ITEM_COL):
    duplicates = df[df.duplicated(subset=[USER_COL, ITEM_COL], keep='first')]
    df.to_csv('check_duplicates.csv', index=False)
    if not duplicates.empty:
        print("Powtarzające się pary UserID+ItemID:")
        print(duplicates)
    else:
        print("Brak powtórzeń w parze UserID+ItemID.")