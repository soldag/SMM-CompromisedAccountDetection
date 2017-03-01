class MetaDataFeatures:

    def __init__(self, status_update):
        self.status_update = status_update

    def get_features(self):
        features = [self.status_update.number_of_shares,
                    self.status_update.number_of_likes,
                    self.status_update.date_time.hour,
                    self.status_update.date_time.minute,
                    self.status_update.date_time.date().weekday(),
                    self.status_update.latitude or 0,
                    self.status_update.longitude or 0]

        return features
