from os.path import splitext
import pandas as pd


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.load()
        self.clean()

    def load(self):
        _, ext = splitext(self.file_path)
        if ext == '.csv':
            return pd.read_csv(self.file_path)
        elif ext == '.tsv':
            return pd.read_csv(self.file_path, sep='\t')
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(self.file_path)
        elif ext == '.json':
            return pd.read_json(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def clean(self):
        self.df.dropna(inplace=True)


    def data(self):
        ...