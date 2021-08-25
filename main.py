from SteamData import SteamData

if __name__ == '__main__':
    print("Start!")
    instance_data = SteamData()
    instance_data\
        .clean(deleteRows=['publisher', 'popular_tags'])\
        .process()\
        .csv_open()
    print("Done!")