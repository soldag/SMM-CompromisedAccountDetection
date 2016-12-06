import csv
from datetime import datetime

from .status_update import StatusUpdate


class FthProvider:
    DELIMITER = ';'
    DATE_FORMAT = '%Y-%m-%d%H:%M'

    def get_status_updates(self, dataset_path):
        with open(dataset_path, 'r', encoding='latin-1') as file:
            reader = csv.DictReader(file, delimiter=self.DELIMITER)
            status_updates = [self._parse_row(row) for row in reader]

            return status_updates

    def _parse_row(self, row):
        return StatusUpdate(
            id=row['Tweet Id'],
            author=row['Nickname'],
            content=row['Tweet content'],
            date_time=datetime.strptime(row['Date'] + row['Hour'],
                                        self.DATE_FORMAT),
            language=row['Tweet language (ISO 639-1)'],
            country=row['Country'],
            latitude=self._parse_float(row['Latitude']),
            longitude=self._parse_float(row['Longitude']),
            number_of_shares=self._parse_int(row['RTs']),
            number_of_likes=self._parse_int(row['Favs']))


    def _parse_int(self, value, default=0):
        try:
            return int(value)
        except ValueError:
            return default

    def _parse_float(self, value, default=0):
        try:
            return float(value)
        except ValueError:
            return default
