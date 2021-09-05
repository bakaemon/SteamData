import csv
import json
import os


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class NoPandasSteamData:
    def __init__(self, filename):
        """Reading file."""
        self._SAVED_FILE = 'secondary_processed.csv'
        self._RAW_FILE_CSV = filename
        with open("files/" + self._RAW_FILE_CSV, "r", encoding="ISO-8859-1") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            self._data = list(reader)

    def to_json(self):
        """Testing method."""
        json.dump(list(self._data), open("files/demo.json", "w+"), sort_keys=True, indent=4)

    def to_csv(self, filename: str = 'secondary_processed.csv'):
        """Export file."""
        self._SAVED_FILE = filename
        keys = self._data[0].keys()
        with open('files/' + filename, 'w+', encoding="ISO-8859-1", newline="") as output_file:
            fc = csv.DictWriter(output_file, fieldnames=keys)
            fc.writeheader()
            fc.writerows(self._data)
        return self

    def clean(self, deleteNullRows=None, allowNulls=True):
        """Clean the table."""
        if deleteNullRows is None:
            deleteNullRows = []
        print("Cleaning...")
        for row in self._data[:]:
            del row['recent_reviews']
            del row['url']
            del row['mature_content']
            del row['recommended_requirements']
            for key in row.keys():
                if row[key] == "":
                    row[key] = "NaN"
            row['original_price'] = 0 if row['original_price'] == "NaN" else row['original_price'].replace("$", "")
            if str(row['original_price']).lower() in ("free to play", "play for free!") or row['original_price'] in (
                    0, "0"):
                row['original_price'] = "Free"
            elif not isfloat(row['original_price']):
                row['original_price'] = "Demo play"
            row['discount_price'] = row['original_price'] if row['discount_price'] == "NaN" else row['discount_price'] \
                .replace("$", "")
            row['achievements'] = 0 if row['achievements'] == "NaN" else row['achievements']
            row['all_reviews'] = str(row['all_reviews']).split(",")[0]
            row['total_languages'] = 0
            languages = str(row['languages']).split(" - ")
            for langs in languages:
                row['total_languages'] += len(langs.split(","))
            genres = str(row['genre']).split(",")
            row['number_of_genre'] = len(genres)
            if not allowNulls or len(deleteNullRows) > 0:
                headers = deleteNullRows
                if not allowNulls:
                    headers = list(row.keys())
                for key in headers:
                    if row[key] == "" or row[key] == "NaN":
                        print('Removing rows...', flush=True, end="\r")
                        del self._data[self._data.index(row)]
                        break
        print("Clean completed.")

        return self

    def csv_open(self, filetype="saved", force=False):
        project_root = os.path.abspath(os.path.dirname(__file__))
        if not force:
            input("Press Enter to open csv file...")
        if filetype == "saved":
            os.startfile(os.path.join(project_root, "files", self._SAVED_FILE))
        elif filetype == "raw":
            os.startfile(os.path.join(project_root, "files", self._RAW_FILE_CSV))
