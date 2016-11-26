class Post:
    def __init__(self, author, content, date_time):
        self._author = author
        self._content = content
        self._date_time = date_time

    @property
    def author(self):
        return self._author

    @property
    def content(self):
        return self._content

    @property
    def date_time(self):
        return self._date_time
