# When is the bus coming?

Query the City of Edmonton's live bus update deef to check when the bus is coming.

## Usage

`pip install datetime pytz google-api-core`

`python main.py [-h] [-s stop] [-r route]`

## How it works

I compiled google's PrototypeBuffer file for GTFS using `protoc` into the file `gtfs_realtime_pb2.py`. Then, I download the City of Edmonton's pb file which has the departure updates for all busses in real time. I interpret the pb file and parse it for updates corresponding to the route and stop of interest (if passed). If nothing is passed then all updates are passed.

## Whats PrototypeBuffer?

Its google's standard of sending data over the internet. Its in binary format so its faster and smaller compared to json. The binary data is send in **.pb** file. To interpret it, you need to know the schema which is defined in a text **.proto** file. In order to make using the proto file easier, there is a compiler **protoc** which "compiles" the text proto file into a script which will read .pb files and make it easier to work with in your programming language.

[proto file](https://gtfs.org/realtime/proto/)
[Edmonton's pb file](https://gtfs.edmonton.ca/TMGTFSRealTimeWebService/TripUpdate/TripUpdates.pb)
[protoc](https://github.com/protocolbuffers/protobuf/releases)

To compile the proto file into the python script I ran `protoc --python_out=. gtfs-realtime.proto`.
