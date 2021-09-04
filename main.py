from SteamData import SteamData
from csv_version import NoPandasSteamData as SteamData

if __name__ == '__main__':
    print("Start!")
    # instance_data = SteamData() #Using pandas
    instance_data = SteamData("steam_games.csv")  # not using pandas
    instance_data \
        .clean(deleteNullRows=["publisher", "popular_tags"]) \
        .to_csv("demo.csv") \
        .csv_open(force=True)
    # instance_data\
    #     .clean(deleteNullRows=["publisher", "popular_tags"])\
    #     .process()\
    #     .csv_open(force=True)
    print("Done!")
