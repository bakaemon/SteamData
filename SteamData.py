import json
import csv
import numpy as np
import pandas as pd
import os


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class SteamData:
    _TARGET_DIR = "files"
    _TARGET_FILE = _TARGET_DIR + "/processed_data.csv"
    _STATUS = False

    def __init__(self):
        print("Reading csv file...")
        self._csvf = pd.read_csv(self._TARGET_DIR + "/steam_games.csv", encoding="ISO-8859-1")
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
            row['original_price'] = 0 if pd.isna(row['original_price']) else row['original_price'].replace("$", "")
            if str(row['original_price']).lower() in ("free to play", "play for free!") or row['original_price'] in (0, "0"):
                row['original_price'] = "Free"
            elif not isfloat(row['original_price']):
                row['original_price'] = "Demo play"
            row['discount_price'] = row['original_price'] if pd.isna(row['discount_price']) else row['discount_price'] \
                .replace("$", "")
            row['achievements'] = 0 if pd.isna(row['achievements']) else row['achievements']
            row['total_languages'] = 0
            languages = str(row['languages']).split(" - ")
            for langs in languages:
                row['total_languages'] += len(langs.split(","))
            genres = str(row['genre']).split(",")
            row['number_of_genre'] = len(genres)
            if fillEmpty:
                for key in row.keys():
                    if row[key] == "" or pd.isna(row[key]):
                        row[key] = "NaN"
            if not allowNulls or len(deleteNullRows) > 0:
                headers = deleteNullRows
                if not allowNulls:
                    headers = list(row.keys())
                for key in headers:
                    if pd.isna(row[key]) or row[key] == "NaN":
                        print('Removing rows...', flush=True, end="\r")
                        del self.dict_data[self.dict_data.index(row)]
                        break
            del row['recent_reviews']
            del row['url']
            del row['mature_content']
            del row['recommended_requirements']
        print("Clean completed.")

        return self

    def process(self, repeat=False):
        """Save the processed data to file."""
        print("Processing...")
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

    def csv_open(self, filetype="saved", force=False):
        if not self._STATUS:
            return
        project_root = os.path.abspath(os.path.dirname(__file__))
        if not force:
            input("Press Enter to open csv file...")
        if filetype == "saved":
            os.startfile(os.path.join(project_root, "files", "processed_data.csv"))
        elif filetype == "raw":
            os.startfile(os.path.join(project_root, "files", "steam_games.csv"))
