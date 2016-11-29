import csv
import uuid
from datetime import datetime

from .status_update import StatusUpdate

DELIMITER = ','
DATE_FORMAT = '%m/%d/%y %I:%M %p'


def get_status_updates(dataset_path):
    with open(dataset_path, 'r', encoding='latin-1') as file:
        reader = csv.DictReader(file, delimiter=DELIMITER)
        status_updates = [parse_row(row) for row in reader]

        return status_updates


def parse_row(row):
    id = str(uuid.uuid4())
    author = row['#AUTHID']
    content = row['STATUS']
    date_time = parse_date(row['DATE'])

    return StatusUpdate(id, author, content, date_time)


def parse_date(value, default=None):
    try:
        return datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        return default
