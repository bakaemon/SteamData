import json
import csv
import numpy as np
import pandas as pd
from subprocess import Popen


class SteamData:
    _TARGET_DIR = "files/"
    _TARGET_FILE = _TARGET_DIR + "processed_data.csv"
    _STATUS = False

    def __init__(self):
        print("Reading csv file...")
        self._csvf = pd.read_csv(self._TARGET_DIR + "steam_games.csv")
        self.dict_data = self._csvf.to_dict('records')

    def json_save(self):
        """Save data to JSON file."""
        with open('files/steam_games.json', 'w+') as f:
            json_string = json.dumps(self.dict_data, indent=4)
            f.write(json_string)

    def get_data(self):
        """Return list of dictionaries of data."""
        return self.dict_data

    def set_data(self, new_data: list):
        """Set new data. DANGEROUS, DO NOT USE IT."""
        self.dict_data = new_data
        return self

    def clean(self, deleteNullRows=None, fillEmpty=True, allowNulls=True):
        """Clean the table."""
        if deleteNullRows is None:
            deleteNullRows = []
        print("Cleaning...")
        for row in self.dict_data[:]:
            if not allowNulls or len(deleteNullRows) > 0:
                headers = deleteNullRows
                if not allowNulls:
                    headers = list(row.keys())
                for key in headers:
                    if pd.isna(row[key]) or row[key] == "NaN":
                        del self.dict_data[self.dict_data.index(row)]
                        print('Removing rows...', flush=True, end="\r")
                        break

            del row['url']
            row['original_price'] = 0 if pd.isna(row['original_price']) else row['original_price'].replace("$", "")
            if str(row['original_price']).lower() == "free to play":
                row['original_price'] = "Free"
            row['discount_price'] = row['original_price'] if pd.isna(row['discount_price']) else row['discount_price']\
                .replace("$", "")
            row['achievements'] = 0 if pd.isna(row['achievements']) else row['achievements']
            row['total_languages'] = 0
            languages = str(row['languages']).split(" - ")
            for langs in languages:
                row['total_languages'] += len(langs.split(","))
            if fillEmpty:
                for key in row.keys():
                    if row[key] == "" or pd.isna(row[key]):
                        row[key] = "NaN"
        print("Clean completed.")

        return self

    def process(self, repeat=False):
        """Save the processed data to file."""
        print("Processing...")
        """Save the processed data to file."""
        dataframe = pd.DataFrame(self.dict_data)
        try:
            dataframe.to_csv(self._TARGET_FILE)
        except PermissionError as e:
            self._STATUS = False
            print("Processing failed:", e)
            if repeat:
                input("Press Enter to retry again, Ctrl + C to cancel...")
                return self.process()
        print("Processed file saved.")
        self._STATUS = True
        return self

    def csv_open(self, office_version=16, force=False):
        if not self._STATUS:
            return
        if not force:
            input("Press Enter to open csv file...")
        Popen(r"C:\Program Files (x86)\Microsoft Office\root\Office" + str(
            office_version) + "\EXCEL.EXE " + self._TARGET_FILE)
