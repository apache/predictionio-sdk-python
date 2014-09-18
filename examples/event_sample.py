from predictionio import EventClient
from predictionio import NotFoundError

client = EventClient(app_id=4, url="http://localhost:7070")

# Check status
print("Check status")
print(client.get_status())

# First event
first_event_data = {
  "predictionKey": "my_prediction_key",
  "appId": 4,
  "event": "my_event",
  "entityType": "user",
  "entityId": "uid",
  "properties": {
    "prop1" : 1,
    "prop2" : "value2",
    "prop3" : [1, 2, 3],
    "prop4" : True,
    "prop5" : ["a", "b", "c"],
    "prop6" : 4.56 ,
  },
}
first_event_response = client.create_event(first_event_data)
print("First Event response")
print(first_event_response)
print

# Second event
second_event_data = {
  "appId" : 4,
  "predictionKey" : "my_prediction_key",
  "event" : "my_event",
  "entityType" : "user",
  "entityId" : "uid",
  "targetEntityType" : "item",
  "targetEntityId" : "iid",
  "properties" : {
    "someProperty" : "value1",
    "anotherProperty" : "value2"
  },
  "eventTime" : "2004-12-13T21:39:45.618Z",
  "tags" : ["tag1", "tag2"],
  "creationTime" : "2014-09-01T21:40:45.123+01:00"
}
print("Second Event response")
print(client.create_event(second_event_data))
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
