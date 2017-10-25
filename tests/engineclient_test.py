import random
import subprocess
import unittest

from predictionio import EventClient

app_name ='EngineClientApp'
access_key = 'FILE_EXPORT_TEST'

class EngineClientTest(unittest.TestCase):

    def setUp(self):
        subprocess.call(['pio', 'app', 'new', '--access-key', access_key, app_name])

    def tearDown(self):
        subprocess.call(['pio', 'app', 'delete', '-f', app_name])

    def test_query(self):
        random.seed()

        client = EventClient(access_key=access_key, url="http://127.0.0.1:7070")

        # Check status
        print("Check status")
        print(client.get_status())
        self.assertEqual(client.get_status(), {'status': 'alive'})

        user_ids = [str(i) for i in range(1, 3)]
        for user_id in user_ids:
            print("Set user", user_id)
            client.set_user(user_id)
            # TODO assert

        item_ids = [str(i) for i in range(1, 5)]
        for item_id in item_ids:
            print("Set item", item_id)
            client.set_item(item_id, {"itypes": ['1']})
            # TODO assert

            # each user randomly views 10 items
            for user_id in user_ids:
                for viewed_item in random.sample(item_ids, 2):
                    print("User", user_id, "views item", viewed_item)
                    client.record_user_action_on_item("view", user_id, viewed_item)
                    # TODO assert

        client.close()

