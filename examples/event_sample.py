from predictionio import EventClient
from predictionio import NotFoundError

client = EventClient(app_id=6, url="http://localhost:7070")

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

# "user"-helper methods

# Set user properties implicitly create a user
# This call creates a user "foo", and set the properties of "foo".
print("Create user foo")
foo_properties = {"city": "sunnyvale", "car": "honda fit"}
print(client.set_user("foo", properties=foo_properties))

# This call overrides the existing properties for user "foo", setting "car" to
# a new "honda odyssey" and create a new property "food" to "seafood".
print("Set new properties")
foo_properties = {"car": "honda odyssey", "food": "seafood"}
print(client.set_user("foo", properties=foo_properties))

# This call removes the specified properties. It ignores the value of the dict.
# After this call, the "city" will become an unset field.
print("Unset properties")
foo_properties = {"city": "x"}
print(client.unset_user("foo", properties=foo_properties))

# This call deletes a user
print("Delete user")
print(client.delete_user("foo"))

# "item"-helper methods

# Set item properties implicitly create a item
# This call creates a item "bar", and set the properties of "bar".
print("Create item bar")
bar_properties = {"city": "santa clara", "weight": 6.9}
print(client.set_item("bar", properties=bar_properties))

# Similar to user-methods, we can do the same thing with item
print("Set new properties")
bar_properties = {"weight": 6.2}
print(client.set_item("bar", properties=bar_properties))

# This call removes the specified properties. It ignores the value of the dict.
# After this call, the "city" will become an unset field.
print("Unset properties")
bar_properties = {"city": None}
print(client.unset_item("bar", properties=bar_properties))

# This call deletes a item
print("Delete item")
print(client.delete_item("bar"))


# "record" action helper functions

# This call creates a event between a user and an item. In particular, this set
# the price of the action
print("Record user action")
action_properties = {"price": 10.0}
print(client.record_user_action_on_item("buy", "foo", "bar", action_properties))
