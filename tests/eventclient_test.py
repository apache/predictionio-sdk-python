import pytz
import subprocess
import unittest

from datetime import datetime
from predictionio import EventClient
from predictionio import NotFoundError
from predictionio import InvalidArgumentError

app_name ='EventClientApp'
access_key = 'EVENT_CLIENT_TEST'
channel = 'Test'

class EventClientTest(unittest.TestCase):

    def setUp(self):
        subprocess.call(['pio', 'app', 'new', '--access-key', access_key, app_name])
        subprocess.call(['pio', 'app', 'show', app_name])

    def tearDown(self):
        subprocess.call(['pio', 'app', 'delete', '-f', app_name])

    def test_eventclient(self):
        client = EventClient(access_key=access_key, url="http://127.0.0.1:7070")

        # Check status
        print("Check status")
        print(client.get_status())
        self.assertEqual(client.get_status(), {'status': 'alive'})

        # First event
        first_event_properties = {
            "prop1": 1,
            "prop2": "value2",
            "prop3": [1, 2, 3],
            "prop4": True,
            "prop5": ["a", "b", "c"],
            "prop6": 4.56,
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
        self.assertEqual(first_event_response.status, 201)

        # Second event
        second_event_properties = {
            "someProperty": "value1",
            "anotherProperty": "value2",
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
        self.assertEqual(second_event_response.status, 201)


        # Get the first event from Event Server
        first_event_id = first_event_response.json_body["eventId"]
        print("Get Event")
        event = client.get_event(first_event_id)
        print(event)
        self.assertEqual(event.get('eventId'), first_event_id)


        # Delete the first event from Event Server
        print("Delete Event")
        delete_response = client.delete_event(first_event_id)
        print(delete_response)
        self.assertEqual(delete_response.decode('utf-8'), '{"message":"Found"}')


        # Delete the first event from Event Server again should yield exception.
        print("Delete Event Again")
        try:
            delete_response = client.delete_event(first_event_id)
            self.fail()
        except NotFoundError as ex:
            print("The expected error: {0}".format(ex))


        # "user"-helper methods

        # Set user properties implicitly create a user
        # This call creates a user "foo", and set the properties of "foo".
        print("Create user foo")
        foo_properties = {"city": "sunnyvale", "car": "honda fit"}
        response = client.set_user("foo", properties=foo_properties)
        print(response)
        self.assertEqual(response.status, 201)

        # This call overrides the existing properties for user "foo", setting "car" to
        # a new "honda odyssey" and create a new property "food" to "seafood".
        print("Set new properties")
        foo_properties = {"car": "honda odyssey", "food": "seafood"}
        response = client.set_user("foo", properties=foo_properties)
        print(response)
        self.assertEqual(response.status, 201)

        # This call removes the specified properties. It ignores the value of the dict.
        # After this call, the "city" will become an unset field.
        print("Unset properties")
        foo_properties = {"city": "x"}
        response = client.unset_user("foo", properties=foo_properties)
        print(response)
        self.assertEqual(response.status, 201)

        # This call deletes a user
        print("Delete user")
        response = client.delete_user("foo")
        print(response)
        self.assertEqual(response.status, 201)

        # The SDK also support specifying the eventTime. It is useful for importing
        # events happened in the past.
        foo_time = datetime(2014, 8, 31, 4, 56, tzinfo=pytz.timezone('US/Pacific'))
        print("Create user at " + str(foo_time))
        response = client.set_user("Jarvis", {}, foo_time)
        print(response)
        self.assertEqual(response.status, 201)

        # "item"-helper methods

        # Set item properties implicitly create a item
        # This call creates a item "bar", and set the properties of "bar".
        print("Create item bar")
        bar_properties = {"city": "santa clara", "weight": 6.9}
        response = client.set_item("bar", properties=bar_properties)
        print(response)
        self.assertEqual(response.status, 201)

        # Similar to user-methods, we can do the same thing with item
        print("Set new properties")
        bar_properties = {"weight": 6.2}
        response = client.set_item("bar", properties=bar_properties)
        print(response)
        self.assertEqual(response.status, 201)

        # This call removes the specified properties. It ignores the value of the dict.
        # After this call, the "city" will become an unset field.
        print("Unset properties")
        bar_properties = {"city": None}
        response = client.unset_item("bar", properties=bar_properties)
        print(response)
        self.assertEqual(response.status, 201)

        # This call deletes a item
        print("Delete item")
        response = client.delete_item("bar")
        print(response)
        self.assertEqual(response.status, 201)


        # "record" action helper functions

        # This call creates a event between a user and an item. In particular, this set
        # the price of the action
        print("Record user action")
        action_properties = {"price": 10.0}
        response = client.record_user_action_on_item("buy", "foo", "bar", action_properties)
        print(response)
        self.assertEqual(response.status, 201)


    def test_eventclient_channel(self):
        subprocess.call(['pio', 'app', 'channel-new', app_name, channel])

        client = EventClient(access_key=access_key, url="http://127.0.0.1:7070",
                             channel=channel)

        # Check status
        print("Check status")
        print(client.get_status())
        self.assertEqual(client.get_status(), {'status': 'alive'})

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
        self.assertEqual(first_event_response.status, 201)

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
        self.assertEqual(second_event_response.status, 201)


        # Get the first event from Event Server
        first_event_id = first_event_response.json_body["eventId"]
        print("Get Event")
        event = client.get_event(first_event_id)
        print(event)
        self.assertEqual(event.get('eventId'), first_event_id)

        # Delete the first event from Event Server
        print("Delete Event")
        delete_response = client.delete_event(first_event_id)
        print(delete_response)
        self.assertEqual(delete_response.decode('utf-8'), '{"message":"Found"}')

        # Delete the first event from Event Server again should yield exception.
        print("Delete Event Again")
        try:
            delete_response = client.delete_event(first_event_id)
            self.fail()
        except NotFoundError as ex:
            print("The expected error: {0}".format(ex))

    def test_invalidurl(self):
        try:
            EventClient(access_key=access_key, url="invalid")
            self.fail()
        except InvalidArgumentError as ex:
            print("The expected error: {0}".format(ex))


if __name__ == "__main__":
    unittest.main()
