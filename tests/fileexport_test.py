import pytz
import re
import subprocess
import unittest

from datetime import datetime
import predictionio
from predictionio import EventClient

app_name ='FileExporterApp'
access_key = 'FILE_EXPORT_TEST'
filename = 'export_events.json'

class FileExporterTest(unittest.TestCase):

    def setUp(self):
        subprocess.call(['pio', 'app', 'new', '--access-key', access_key, app_name])

    def tearDown(self):
        subprocess.call(['pio', 'app', 'delete', '-f', app_name])

    def test_export(self):
        app_info = subprocess.check_output(['pio', 'app', 'show', app_name])
        app_id = re.search('App ID: ([0-9]+)', app_info.decode('utf-8')).group(1)
        print(app_id)

        exporter = predictionio.FileExporter(file_name=filename)

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
        exporter.create_event(
            event="my_event",
            entity_type="user",
            entity_id="uid",
            properties=first_event_properties,
            event_time=first_event_time,
            )

        # Second event
        second_event_properties = {
            "someProperty" : "value1",
            "anotherProperty" : "value2",
            }
        exporter.create_event(
            event="my_event",
            entity_type="user",
            entity_id="uid",
            target_entity_type="item",
            target_entity_id="iid",
            properties=second_event_properties,
            event_time=datetime(2014, 12, 13, 21, 38, 45, 618000, pytz.utc))

        exporter.close()

        subprocess.call(['pio', 'import', '--appid', app_id, '--input ', filename])

        # TODO
        # client = EventClient(access_key=access_key, url="http://127.0.0.1:7070")
        #
        # print("Get Event")
        # event = client.get_event(event_id)
        # print(event)
        # self.assertEqual(event.get('eventId'), event_id)

if __name__ == "__main__":
    unittest.main()
