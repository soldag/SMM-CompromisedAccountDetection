import csv
import uuid
from datetime import datetime

from .status_update import StatusUpdate


class MpProvider:
    DELIMITER = ','
    DATE_FORMAT = '%m/%d/%y %I:%M %p'

    def get_status_updates(self, dataset_path):
        with open(dataset_path, 'r', encoding='latin-1') as file:
            reader = csv.DictReader(file, delimiter=self.DELIMITER)
            status_updates = []
            for row in reader:
                if self._parse_date(row['DATE']) is not None:
                    status_updates.append(self._parse_row(row))

            return status_updates

    def _parse_row(self, row):
        return StatusUpdate(id=str(uuid.uuid4()),
                            author=row['#AUTHID'],
                            content=row['STATUS'],
                            date_time=self._parse_date(row['DATE']))

    def _parse_date(self, value, default=None):
        try:
            return datetime.strptime(value, self.DATE_FORMAT)
        except ValueError:
            return default
