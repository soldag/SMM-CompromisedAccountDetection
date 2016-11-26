import csv
from datetime import datetime

from .post import Post

DELIMITER = ','
DATE_FORMAT = '%m/%d/%y %I:%M %p'


def parse_dataset(path):
    with open(path, 'r', encoding='latin-1') as file:
        reader = csv.DictReader(file, delimiter=DELIMITER)
        posts = [parse_row(row) for row in reader]

        return posts


def parse_row(row):
    author = row['#AUTHID']
    content = row['STATUS']
    date_time = parse_date(row['DATE'])

    return Post(author, content, date_time)

def parse_date(value, default=datetime.strptime('01/01/01 01:01 AM', DATE_FORMAT)):
    try:
        return datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        return default
