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
            status_updates = [self._parse_row(row) for row in reader]

            return [status_update for status_update in status_updates
                    if status_update.date_time is not None]

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
