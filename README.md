# When is the bus coming?

Query the City of Edmonton's live bus update deef to check when the bus is coming.

## Usage

`pip install datetime pytz google-api-core`

`python main.py [-h] [-s stop] [-r route]`

## How it works

I compiled google's PrototypeBuffer file for GTFS using `protoc` into the file `gtfs_realtime_pb2.py`. Then, I download the City of Edmonton's pb file from the URL https://gtfs.edmonton.ca/TMGTFSRealTimeWebService/TripUpdate/TripUpdates.pb which has the departure updates for all busses in real time. I interpret the pb file and parse it for updates corresponding to the route and stop of interest (if passed). If nothing is passed then all updates are passed.
