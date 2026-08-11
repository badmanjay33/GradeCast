from os.path import splitext
import pandas as pd
import warnings


class DataLoader:
    vital_columns = ['Semester', 'Units', 'Grade']
    allowed_columns = ['Semester', 'Course Code', 'Course Title', 'Units', 'Grade']

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
        initial_len = len(self.df)
        cols = self.df.columns.tolist()

        # Ensure vital rows are present
        missing_vitals = []
        for vital_column in self.vital_columns:
            if vital_column not in cols:
                missing_vitals.append(vital_column)
        if missing_vitals:
            raise ValueError(f"Column {missing_vitals} not found in data")

        # Drop unnecessary columns
        for col in cols:
            if col not in self.allowed_columns:
                self.df.drop(col, axis=1, inplace=True)

        # Drop rows with null values
        self.df.dropna(inplace=True)
        new_length = len(self.df)
        if initial_len > new_length:
            warnings.warn(f'{initial_len - new_length} row(s) were deleted due to missing data!', UserWarning)


    def data(self):
        return self.df