# this is example of import events to a specific channel of an App

from predictionio import EventClient
from predictionio import NotFoundError
from datetime import datetime
import pytz
import sys

access_key = None
channel = None

assert access_key is not None, "Please create an access key with 'pio app new'"
# Need to create channel first before
assert channel is not None, "Please create new channel with 'pio app channel-new'"

client = EventClient(access_key=access_key, url="http://localhost:7070",
  channel=channel)

# Check status
print("Check status")
print(client.get_status())

# First event
first_event_properties = {
    "prop1" : 1,
    "prop2" : "value2",
    "prop3" : [1, 2, 3],
    "prop4" : True,
    "prop5" : ["a", "b", "c"],
    "prop6" : 4.56 ,
    }
first_event_time = datetime(
    2004, 12, 13, 21, 39, 45, 618000, pytz.timezone('US/Mountain'))
first_event_response = client.create_event(
    event="my_event",
    entity_type="user",
    entity_id="uid",
    properties=first_event_properties,
    event_time=first_event_time,
    )
print("First Event response")
print(first_event_response)
print

# Second event
second_event_properties = {
    "someProperty" : "value1",
    "anotherProperty" : "value2",
    }
second_event_response = client.create_event(
    event="my_event",
    entity_type="user",
    entity_id="uid",
    target_entity_type="item",
    target_entity_id="iid",
    properties=second_event_properties,
    event_time=datetime(2014, 12, 13, 21, 38, 45, 618000, pytz.utc))
print("Second Event response")
print(second_event_response)
print


# Get the first event from Event Server
first_event_id = first_event_response.json_body["eventId"]
print("Get Event")
event = client.get_event(first_event_id)
print(event)
print

# Delete the first event from Event Server
print("Delete Event")
delete_response = client.delete_event(first_event_id)
print(delete_response)
print

# Delete the first event from Event Server again should yield exception.
print("Delete Event Again")
try:
  delete_response = client.delete_event(first_event_id)
except NotFoundError, ex:
  print("The expected error: {0}".format(ex))
print
