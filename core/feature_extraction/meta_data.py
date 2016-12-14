class MetaDataFeatures:

    def __init__(self, status_update):
        self.statusUpdate = status_update

    def get_features(self):
        features = [self.statusUpdate.number_of_shares,
                    self.statusUpdate.number_of_likes,
                    self.statusUpdate.date_time.hour,
                    self.statusUpdate.date_time.minute,
                    self.statusUpdate.date_time.date().weekday(),
                    self.statusUpdate.latitude or 0,
                    self.statusUpdate.longitude or 0]

        return features
