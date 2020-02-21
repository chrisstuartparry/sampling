import pandas as pd


def encode_data_frame(df, domain):
    '''
    Encode data frame into format suitable for regression.
    This maps continuous columns with identity, and one-hot-encodes discrete columns.
    '''
    one_hot = pd.get_dummies(df, drop_first=True)
    column_map = [param.transform_columns() for param in domain.params]
    zero_columns = [column for columns in column_map for column in columns]
    for column in zero_columns:
        if column not in one_hot.columns:
            one_hot[column] = 0.
    return one_hot


def x_y_split(df):
    '''
    Split encoded data frame into regression inputs (X) and outputs (y).
    '''
    y_params = ['tbr', 'tbr_error']
    drop_params = ['sim_time']

    X_params = list(set(df.columns.tolist()) - set(y_params + drop_params))

    return df[X_params].copy(), df[y_params].copy()
