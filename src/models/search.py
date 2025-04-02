class SearchDescription:
    def __init__(self, link, title, date, search_type, lat, lon, hq_time, equipage=True):
        self.link = link
        self.title = title
        self.date = date
        self.search_type = search_type
        self.latitude = lat
        self.longitude = lon
        self.hq_time = hq_time
        self.equipage = equipage