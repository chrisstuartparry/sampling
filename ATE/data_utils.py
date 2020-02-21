import pandas as pd


def transform_dataset(df, domain):
    '''
    Transform data set to encode discrete columns into one-hot format.
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
    Split transformed data set into regression inputs (X) and outputs (y).
    '''
    y_params = ['tbr', 'tbr_error']
    drop_params = ['sim_time']

    X_params = list(set(df.columns.tolist()) - set(y_params + drop_params))

    return df[X_params].copy(), df[y_params].copy()
