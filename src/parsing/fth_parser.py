import csv
from datetime import datetime

from .tweet import Tweet

DELIMITER = ';'
DATE_FORMAT = '%Y-%m-%d%H:%M'


def parse_dataset(path):
    with open(path, 'r', encoding='latin-1') as file:
        reader = csv.DictReader(file, delimiter=DELIMITER)
        posts = [parse_row(row) for row in reader]

        return posts


def parse_row(row):
    id = row['Tweet Id']
    author = row['Nickname']
    content = row['Tweet content']
    date_time = datetime.strptime(row['Date'] + row['Hour'], DATE_FORMAT)
    language = row['Tweet language (ISO 639-1)']
    country = row['Country']
    latitude = parse_float(row['Latitude'])
    longitude = parse_float(row['Longitude'])
    number_of_retweets = parse_int(row['RTs'])
    number_of_favorites = parse_int(row['Favs'])

    return Tweet(id, author, content, date_time, language, country,
                 latitude, longitude, number_of_retweets, number_of_favorites)


def parse_int(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default


def parse_float(value, default=0):
    try:
        return float(value)
    except ValueError:
        return default
