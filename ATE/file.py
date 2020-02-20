import pandas as pd


class CSVFile:
    def __init__(self, path):
        self.path = path
        self.data = pd.read_csv(path)
