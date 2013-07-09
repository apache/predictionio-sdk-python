"""
Test Python SDK
"""
import predictionio
import unittest
import threading
import time

import httplib
import urllib


APP_KEY = "zHCx9Xv9sZ9Q21LMINKcrgZNgGJ3oReZA9Zvf0MsyJYDv6FwgHEeEI0XTEY5aEsu" # replace this with your AppKey
API_URL = "http://localhost:8000" # PredictoinIO Server

class TestPredictionIO(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_status(self):
        client = predictionio.Client(APP_KEY, 1, API_URL)
        status = client.get_status()
        self.assertEqual(status, "PredictionIO Output API is online.")
        client.close()

    def test_user(self):
        client = predictionio.Client(APP_KEY, 1, API_URL)

        # create users and get them back
        client.create_user("u1")
        # create user with optional attributes
        client.create_user("u2", { "pio_latlng": [1.2,33.3] })
        client.create_user("u3", { "pio_latlng": [4.5,67.8], "pio_inactive": True } )
        # create user with custom attributes
        client.create_user("u4", { "pio_latlng": [1.2,33.3], "custom1": "value1", "custom2": "value2" })
        client.create_user("u5", { "custom1": "u5c1", "custom2": "u5c2" })

        user1 = client.get_user("u1")
        user2 = client.get_user("u2")
        user3 = client.get_user("u3")
        user4 = client.get_user("u4")
        user5 = client.get_user("u5")

        self.assertEqual(user1, {"pio_uid" : "u1"})
        self.assertEqual(user2, {"pio_uid" : "u2", "pio_latlng": [1.2,33.3]})
        self.assertEqual(user3, {"pio_uid" : "u3", "pio_latlng" : [4.5,67.8], "pio_inactive" : True})
        self.assertEqual(user4, {"pio_uid" : "u4", "pio_latlng": [1.2,33.3], "custom1": "value1", "custom2": "value2" })
        self.assertEqual(user5, {"pio_uid" : "u5", "custom1": "u5c1", "custom2": "u5c2"  })

        # delete user and then try to get it
        client.delete_user("u1")

        try:
            user = client.get_user("u1")
        except predictionio.UserNotFoundError as e:
            pass # expected exception
        except:
            raise

        # other users still exist
        user2 = client.get_user("u2")
        self.assertEqual(user2, {"pio_uid" : "u2", "pio_latlng": [1.2,33.3]})

        # read, modify, write
        user3 = client.get_user("u3")
        self.assertEqual(user3, {"pio_uid" : "u3", "pio_latlng" : [4.5,67.8], "pio_inactive" : True})
        del user3["pio_uid"] 
        user3["pio_latlng"] = [5.6,10.11]
        user3["pio_inactive"] = False
        user3["custom1"] = "food"
        client.create_user("u3", user3)
        updated_user3 = client.get_user("u3")
        self.assertEqual(updated_user3, {"pio_uid" : "u3", "pio_latlng" : [5.6,10.11], "pio_inactive" : False, "custom1" : "food"} )

        user4 = client.get_user("u4")
        self.assertEqual(user4, {"pio_uid" : "u4", "pio_latlng": [1.2,33.3], "custom1": "value1", "custom2": "value2" })
        del user4["pio_uid"]
        user4["custom1"] = "new value"
        client.create_user("u4", user4)
        updated_user4 = client.get_user("u4")
        self.assertEqual(updated_user4, {"pio_uid" : "u4", "pio_latlng": [1.2,33.3], "custom1": "new value", "custom2": "value2" })

        client.close()

    def test_item(self):
        client = predictionio.Client(APP_KEY, 1, API_URL)

        # create items and read back
        client.create_item("i1", ("t1","t2","t3"))
        client.create_item("i2", ("t1",))
        client.create_item("i3", ("t2",), {"pio_price": 4.99, "pio_profit": 2.0, "pio_startT": 12345667, "pio_endT": 4567788, "pio_latlng": [1.345, 9.876], "pio_inactive": True })
        client.create_item("i4", ("t2",), {"pio_latlng": [1.2345, 10.11], "custom1": "value1"})
        client.create_item("i5", ("t1", "t2"), {"custom1": "i5value1", "custom2": "i5value2"} )

        item1 = client.get_item("i1")
        item2 = client.get_item("i2")
        item3 = client.get_item("i3")
        item4 = client.get_item("i4")
        item5 = client.get_item("i5")
        
        del item1["pio_startT"] # pio_startT is automatically inserted, don't compare
        self.assertEqual(item1, {"pio_iid": "i1", "pio_itypes": ("t1", "t2", "t3") } )
        del item2["pio_startT"]
        self.assertEqual(item2, {"pio_iid": "i2", "pio_itypes": ("t1",)} )
        self.assertEqual(item3, {"pio_iid": "i3", "pio_itypes": ("t2",), "pio_price": 4.99, "pio_profit": 2.0, "pio_startT": 12345667, "pio_endT": 4567788, "pio_latlng": [1.345, 9.876], "pio_inactive": True } )
        del item4["pio_startT"]
        self.assertEqual(item4, {"pio_iid": "i4", "pio_itypes": ("t2",), "pio_latlng": [1.2345, 10.11], "custom1": "value1"})
        del item5["pio_startT"]
        self.assertEqual(item5, {"pio_iid": "i5", "pio_itypes": ("t1","t2"), "custom1": "i5value1", "custom2": "i5value2"})

        # delete and then try to get it
        client.delete_item("i2")

        try:
          item2 = client.get_item("i2")
        except predictionio.ItemNotFoundError as e:
            pass # expected exception
        except:
            raise

        # others still exist
        item3 = client.get_item("i3")
        self.assertEqual(item3, {"pio_iid": "i3", "pio_itypes": ("t2",), "pio_price": 4.99, "pio_profit": 2.0, "pio_startT": 12345667, "pio_endT": 4567788, "pio_latlng": [1.345, 9.876], "pio_inactive": True } )
        
        # read, modify, write
        del item3["pio_iid"]
        item3_itypes = item3.pop("pio_itypes")
        item3["pio_price"] = 6.99
        item3["custom1"] = "some value"
        client.create_item("i3", item3_itypes, item3)
        updated_item3 = client.get_item("i3")
        self.assertEqual(updated_item3, {"pio_iid": "i3", "pio_itypes": ("t2",), "pio_price": 6.99, "pio_profit": 2.0, "pio_startT": 12345667, "pio_endT": 4567788, "pio_latlng": [1.345, 9.876], "pio_inactive": True, "custom1": "some value" } )
        
        client.close()

    def test_u2iAction_deprecated(self):
        client = predictionio.Client(APP_KEY, 1, API_URL)

        client.user_like_item("u1", "i1")
        client.user_dislike_item("u2", "i2")
        client.user_view_item("u3", "i3")
        client.user_rate_item("u4", "i4", 4)
        client.user_conversion_item("u5", "i5")

        client.close()

    def test_u2iAction(self):
        client = predictionio.Client(APP_KEY, 1, API_URL)

        client.identify("u101")

        # required param
        client.record_action_on_item("like", "i1")
        client.record_action_on_item("dislike", "i2")
        client.record_action_on_item("view", "i3")
        client.record_action_on_item("rate", "i4", { "pio_rate": 1 })
        client.record_action_on_item("conversion", "i5")

        client.identify("u102")

        # with optional param
        client.record_action_on_item("like", "i1", { "pio_latlng": [1.23, 4.56] })
        client.record_action_on_item("dislike", "i2", { "pio_t": 1234567689 })
        client.record_action_on_item("view", "i3", { "pio_latlng": [4.67, 1.44], "pio_t": 3445566778})
        client.record_action_on_item("rate", "i4", { "pio_rate": 1, "pio_latlng": [66.78, 9.10] })
        client.record_action_on_item("conversion", "i5", { "pio_price" : 12.5 })

        client.close()

    def test_get_itemrec_deprecated(self):
        client = predictionio.Client(APP_KEY, 1, API_URL)

        try:
            itemrec = client.get_itemrec("u1", 10, "test-python-engine")
        except predictionio.ItemRecNotFoundError as e:
            pass # expected exception
        except:
            raise

        client.close()

    def test_get_itemrec_topn(self):
        client = predictionio.Client(APP_KEY, 1, API_URL)

        client.identify("u103")

        try:
            itemrec = client.get_itemrec_topn(10, "test-python-engine")
        except predictionio.ItemRecNotFoundError as e:
            pass # expected exception
        except:
            raise

        try:
            itemrec = client.get_itemrec_topn(10, "test-python-engine", { "pio_itypes": ("t1",), "pio_latlng": [1.34, 5.67], "pio_within": 5.0, "pio_unit": "km", "pio_attributes": ["custom1", "custom2"]  })
        except predictionio.ItemRecNotFoundError as e:
            pass # expected exception
        except:
            raise

        client.close()

"""
to run individual test:
$ python -m unittest predictionio_test.TestPredictionIO.test_user

to run ALL tests:
% python predictionio_test.py
"""
if __name__ == "__main__" :
    unittest.main()
