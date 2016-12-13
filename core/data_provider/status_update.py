from datetime import datetime

class StatusUpdate:
    def __init__(self, id, author, content, date_time=None, language=None, country=None,
                 latitude=None, longitude=None, number_of_shares=None, number_of_likes=None):
        self._id = id
        self._author = author
        self._content = content
        self._date_time = date_time
        self._language = language
        self._country = country
        self._latitude = latitude
        self._longitude = longitude
        self._number_of_shares = number_of_shares
        self._number_of_likes = number_of_likes

    @property
    def id(self):
        return self._id

    @property
    def author(self):
        return self._author

    @property
    def content(self):
        return self._content

    @property
    def date_time(self):
        return self._date_time

    @property
    def language(self):
        return self._language

    @property
    def country(self):
        return self._country

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def number_of_shares(self):
        return self._number_of_shares

    @property
    def number_of_likes(self):
        return self._number_of_likes

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "date_time": self.date_time,
            "language": self.language,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "number_of_shares": self.number_of_shares,
            "number_of_likes": self.number_of_likes
        }

    @classmethod
    def from_dict(cls, obj):
        return StatusUpdate(id=obj["id"],
                            author=obj["author"],
                            content=obj["content"],
                            date_time=datetime.strptime(obj["date_time"], "%Y-%m-%d %H:%M:%S"),
                            language=obj["language"],
                            country=obj["country"],
                            latitude=obj["latitude"],
                            longitude=obj["longitude"],
                            number_of_shares=obj["number_of_shares"],
                            number_of_likes=obj["number_of_likes"])
