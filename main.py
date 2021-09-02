from SteamData import SteamData
from MenuInterface import MenuInterface

if __name__ == '__main__':
    print("Start!")
    instance_data = SteamData()
    instance_data\
        .clean(deleteNullRows=["publisher", "popular_tags"])\
        .process()\
        .csv_open()
    print("Done!")


