import folium
from gtfsrt import *
from gtfs import load_gtfs
from utils.filesystem.paths import *

timetable = load_gtfs(DOWNLOADS / 'timetable/yorkshire_2025-01-24.zip')

# 9th element is trips.txt file. 5th element is routes.txt file. 
# Merge these together to get some info about the bus from the timetable
bus_detail = timetable[9][['trip_id','trip_headsign', 'route_id']].merge(timetable[5][['route_id', 'route_short_name']], on='route_id', how='inner')

# Load data
data = gtfsrt([DOWNLOADS / 'gtfs-rt/current/locations.bin'])
data.load_raw_data()

# Create dataframe
data.to_df()

# Merge on trip_id with timetable info
df = data.df.merge(bus_detail, on=['trip_id'])

# Add a human-readbale datetime
df['strftime'] = pd.to_datetime(df['timestamp'], unit='s')

print('Number of buses in Yorkshire:', len(df))

# Load the map
m = folium.Map(location=[52, -1.5], zoom_start=7)

# Set keyword dictionary
kw = {"prefix": "fa", "color": "green", "icon": "arrow-up"}

if __name__ == "__main__":
    # Add buses to the map
    for _, row in df.iterrows():
        # Setting config
        icon = folium.Icon(angle=int(row['bearing']), **kw)
        html = f"""
                    <h1>{row['route_short_name']}</h1>
                    <br />Route ID: <code>{row['route_id_x']}</code>
                    <br />Trip ID: <code>{row['trip_id']}</code>
                    <br />Trip Headsign: <code>{row['trip_headsign']}</code>
                    <br />Time: <code>{row['strftime']}</code>
                """
        # Add markers
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            icon=icon,
            tooltip=str(row['bearing']),
            popup=html
        ).add_to(m)
    
    # save the map
    m.save(MAPS / 'index.html')
    print("Done")