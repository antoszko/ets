# When is the bus coming?

Query the City of Edmonton's live bus update deef to check when the bus is coming.

## Usage

`pip install datetime pytz google-api-core`

`python main.py [-h] [-s stop] [-r route]`

### Example

When is the 4 coming to University? (2002 is the stop the 4 stops at when going eastward)

```
% python main.py -s 2002 -r 4
Namespace(stop='2002', route='004')
Got response 200 from gtfs.edmonton.ca
  Content-Type: application/protocol-buffer
  Content-Length: 839792
Parsed response
route, bus_label, stop, departure_time
004 7106 2002 2024-03-14 15:57:00-06:00
004 4391 2002 2024-03-14 16:02:00-06:00
004 4542 2002 2024-03-14 16:07:00-06:00
004 7064 2002 2024-03-14 16:12:00-06:00
004 4501 2002 2024-03-14 16:17:00-06:00
004 7171 2002 2024-03-14 16:27:00-06:00
004 4634 2002 2024-03-14 16:37:00-06:00
004 7042 2002 2024-03-14 16:47:00-06:00
004 4382 2002 2024-03-14 17:25:00-06:00
004 4622 2002 2024-03-14 17:27:00-06:00
004 4461 2002 2024-03-14 17:27:00-06:00
004 7016 2002 2024-03-14 17:37:00-06:00
004 7038 2002 2024-03-14 17:47:00-06:00
004 4390 2002 2024-03-14 17:57:00-06:00
Done
```

## How it works

I compiled google's PrototypeBuffer file for GTFS using `protoc` into the file `gtfs_realtime_pb2.py`. Then, I download the City of Edmonton's pb file which has the departure updates for all busses in real time. I interpret the pb file and parse it for updates corresponding to the route and stop of interest (if passed). If nothing is passed then all updates are passed.

## Whats PrototypeBuffer?

Its google's standard of sending data over the internet. Its in binary format so its faster and smaller compared to json. The binary data is send in **.pb** file. To interpret it, you need to know the schema which is defined in a text **.proto** file. In order to make using the proto file easier, there is a compiler **protoc** which "compiles" the text proto file into a script which will read .pb files and make it easier to work with in your programming language.

[proto file](https://gtfs.org/realtime/proto/)
[Edmonton's pb file](https://gtfs.edmonton.ca/TMGTFSRealTimeWebService/TripUpdate/TripUpdates.pb)
[protoc](https://github.com/protocolbuffers/protobuf/releases)

To compile the proto file into the python script I ran `protoc --python_out=. gtfs-realtime.proto`.
