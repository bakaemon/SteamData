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
            # delete rows
            del row['recent_reviews']
            del row['url']
            del row['mature_content']
            del row['recommended_requirements']
            # if any cells are null (empty value), fill it with NaN
            for key in row.keys():
                if row[key] == "":
                    row[key] = "NaN"
            # price is filled with 0 if the price cells are either string or NaN, or else remove
            # the dollar sign and convert it to float number
            row['original_price'] = 0.0 \
                if row['original_price'] == "NaN" \
                or not isfloat(row['original_price'].replace("$", "")) \
                else float(row['original_price'].replace("$", ""))
            row['discount_price'] = row['original_price'] \
                if row['discount_price'] == "NaN"  \
                or not isfloat(row['discount_price'].replace("$", ""))\
                else float(row['discount_price'].replace("$", ""))
            # get the first, which is the most popular, tag
            row['popular_tags'] = str(row['popular_tags']).split(",")[0]
            # fill 0 to null cell of achievement columns
            row['achievements'] = 0 if row['achievements'] == "NaN" else row['achievements']
            # get summary of all_review e.g: Most Positive, Mixed
            row['all_reviews'] = str(row['all_reviews']).split(",")[0]

            # split original string into list of string which each string is the language
            # seperated by comma.
            row['total_languages'] = 0
            languages = str(row['languages']).split(" - ")
            for langs in languages:
                # split each substring into smaller list by comma, then update the total_language by the length
                # of smaller list
                row['total_languages'] += len(langs.split(","))
            # split genre string which seperate by comma, then save the length of the list into new columns
            genres = str(row['genre']).split(",")
            row['number_of_genre'] = len(genres)
            # check if any of the columns name in deleteNullRow has cell empty, if there are, delete the row contain
            # that cell.
            if not allowNulls or len(deleteNullRows) > 0:
                headers = deleteNullRows
                # if allowNulls is False, deleteNullRows will contains all the column name of the table
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
