import pandas as pd


def transform_dataset(df, domain):
    one_hot = pd.get_dummies(df, drop_first=True)
    column_map = [param.transform_columns() for param in domain.params]
    zero_columns = [column for columns in column_map for column in columns]
    for column in zero_columns:
        if column not in one_hot.columns:
            one_hot[column] = 0.
    return one_hot
