import csv
from datetime import datetime

from .status_update import StatusUpdate

DELIMITER = ';'
DATE_FORMAT = '%Y-%m-%d%H:%M'


def get_status_updates(dataset_path):
    with open(dataset_path, 'r', encoding='latin-1') as file:
        reader = csv.DictReader(file, delimiter=DELIMITER)
        status_updates = [parse_row(row) for row in reader]

        return status_updates


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

    return StatusUpdate(id, author, content, date_time, language, country,
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
