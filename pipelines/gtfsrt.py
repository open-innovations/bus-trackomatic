from google.transit import gtfs_realtime_pb2
import pandas as pd

class gtfsrt():
    def __init__(self, fpaths:list):
        self.fpaths = [f for f in fpaths]
        self.load_raw_data()
        pass

    def load_raw_data(self):
        '''Load the raw GTFSRT binary files containing 'entities' into lists.'''
        feed = gtfs_realtime_pb2.FeedMessage()
        self.entities = []
        for fp in self.fpaths:
            with open(fp, 'rb') as f:
                feed.ParseFromString(f.read())
            for entity in feed.entity:
                self.entities.append(entity)
    
    def to_df(self, round=5):
        records = []
        print(f"There are {len(self.entities)} entities.")
        for e in self.entities:
            v = e.vehicle
            records.append({
                "trip_id": v.trip.trip_id,
                "start_time": v.trip.start_time,
                "start_date": v.trip.start_date,
                "schedule_relationship": v.trip.schedule_relationship,
                "route_id": v.trip.route_id,
                "latitude": v.position.latitude,
                "longitude": v.position.longitude,
                "bearing": v.position.bearing,
                "stop_sequence": v.current_stop_sequence,
                "status": v.current_status,
                "timestamp": v.timestamp,
                "vehicle_id": v.vehicle.id,
            })

        self.df = pd.DataFrame(records)
        # Store the raw data - useful for debugging.
        self.raw_data = self.df

        # Optionally round coordinates
        if round:
            self.df['longitude'] = self.df['longitude'].round(round)
            self.df['latitude'] = self.df['latitude'].round(round)

        return self.df

    def remove_duplicate_reports(self, subset=['longitude', 'latitude', 'timestamp', 'vehicle_id', 'trip_id'], sortby=['vehicle_id', 'timestamp', 'trip_id']):
        '''Removes duplicate data and sorts the resulting dataframe. Prints the fraction of data that was duplicated.'''
        # Sort the data
        self.df.sort_values(by=sortby, ascending=True, inplace=True)
        with_duplicates = len(self.df) # Count the length of the raw dataframe
        self.df.drop_duplicates(subset=subset, keep='first', inplace=True) # The first/last here shouldn't matter as one of the duplicate fields is timestamp. So these are data points that are for the same point in time too.
        without_duplicates = len(self.df) # Count the length of the de-duplicated dataframe
        fraction_duplicated = round((1 - without_duplicates/with_duplicates)*100, 4)
        print(f"Fraction of data that was duplictaed in 'longitude', 'latitude', 'timestamp', 'vehicle_id', 'trip_id': {fraction_duplicated}%")
