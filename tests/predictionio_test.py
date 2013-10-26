"""
Test Python SDK
"""
import predictionio
import unittest
import threading
import time

try:
    import httplib
except ImportError:
    from http import client as httplib
import urllib

APP_KEY = "GToKwk78As0LBp2fAx2YNUBPZFZvtwy6MJkGwRASiD6Q77JjBnTaXBxzBTd52ICE" # replace this with your AppKey
API_URL = "http://localhost:8000" # PredictoinIO Server

MIN_VERSION = '0.6.0'
if predictionio.__version__ < MIN_VERSION:
    err = "Require PredictionIO Python SDK version >= %s" % MIN_VERSION
    raise Exception(err)

#print predictionio.__version__
#predictionio.connection.enable_log()

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

    def _test_user(self, uids):
        client = predictionio.Client(APP_KEY, 1, API_URL)

        uid1 = uids[0]
        uid2 = uids[1]
        uid3 = uids[2]
        uid4 = uids[3]
        uid5 = uids[4]

        # create users and get them back
        client.create_user(uid1)
        # create user with optional attributes
        client.create_user(uid2, { "pio_latlng": [1.2,33.3] })
        client.create_user(uid3, { "pio_latlng": [4.5,67.8], "pio_inactive": True } )
        # create user with custom attributes
        client.create_user(uid4, { "pio_latlng": [1.2,33.3], "custom1": "value1", "custom2": "value2" })
        client.create_user(uid5, { "custom1": "u5c1", "custom2": "u5c2" })

        user1 = client.get_user(uid1)
        user2 = client.get_user(uid2)
        user3 = client.get_user(uid3)
        user4 = client.get_user(uid4)
        user5 = client.get_user(uid5)

        self.assertEqual(user1, {"pio_uid" : uid1})
        self.assertEqual(user2, {"pio_uid" : uid2, "pio_latlng": [1.2,33.3]})
        self.assertEqual(user3, {"pio_uid" : uid3, "pio_latlng" : [4.5,67.8], "pio_inactive" : True})
        self.assertEqual(user4, {"pio_uid" : uid4, "pio_latlng": [1.2,33.3], "custom1": "value1", "custom2": "value2" })
        self.assertEqual(user5, {"pio_uid" : uid5, "custom1": "u5c1", "custom2": "u5c2"  })

        # delete user and then try to get it
        client.delete_user(uid1)

        try:
            user = client.get_user(uid1)
        except predictionio.UserNotFoundError as e:
            pass # expected exception
        except:
            raise

        # other users still exist
        user2 = client.get_user(uid2)
        self.assertEqual(user2, {"pio_uid" : uid2, "pio_latlng": [1.2,33.3]})

        # read, modify, write
        user3 = client.get_user(uid3)
        self.assertEqual(user3, {"pio_uid" : uid3, "pio_latlng" : [4.5,67.8], "pio_inactive" : True})
        del user3["pio_uid"]
        user3["pio_latlng"] = [5.6,10.11]
        user3["pio_inactive"] = False
        user3["custom1"] = "food"
        client.create_user(uid3, user3)
        updated_user3 = client.get_user(uid3)
        self.assertEqual(updated_user3, {"pio_uid" : uid3, "pio_latlng" : [5.6,10.11], "pio_inactive" : False, "custom1" : "food"} )

        user4 = client.get_user(uid4)
        self.assertEqual(user4, {"pio_uid" : uid4, "pio_latlng": [1.2,33.3], "custom1": "value1", "custom2": "value2" })
        del user4["pio_uid"]
        user4["custom1"] = "new value"
        client.create_user(uid4, user4)
        updated_user4 = client.get_user(uid4)
        self.assertEqual(updated_user4, {"pio_uid" : uid4, "pio_latlng": [1.2,33.3], "custom1": "new value", "custom2": "value2" })

        client.close()

    def test_user(self):
        self._test_user(["u1", "u2", "u3", "u4", "u5"])
        # test special characters in uid
        self._test_user(["u1@a.com", "u2@ap/ple", "u3@foo.bar", "u4/a/b", "&^%$()u5"])

    def _test_item(self, iids):
        client = predictionio.Client(APP_KEY, 1, API_URL)

        iid1 = iids[0]
        iid2 = iids[1]
        iid3 = iids[2]
        iid4 = iids[3]
        iid5 = iids[4]

        # create items and read back
        client.create_item(iid1, ("t1","t2","t3"))
        client.create_item(iid2, ("t1",))
        client.create_item(iid3, ("t2",), {"pio_price": 4.99, "pio_profit": 2.0, "pio_startT": 12345667, "pio_endT": 4567788, "pio_latlng": [1.345, 9.876], "pio_inactive": True })
        client.create_item(iid4, ("t2",), {"pio_latlng": [1.2345, 10.11], "custom1": "value1"})
        client.create_item(iid5, ("t1", "t2"), {"custom1": "i5value1", "custom2": "i5value2"} )

        item1 = client.get_item(iid1)
        item2 = client.get_item(iid2)
        item3 = client.get_item(iid3)
        item4 = client.get_item(iid4)
        item5 = client.get_item(iid5)

        del item1["pio_startT"] # pio_startT is automatically inserted, don't compare
        self.assertEqual(item1, {"pio_iid": iid1, "pio_itypes": ("t1", "t2", "t3") } )
        del item2["pio_startT"]
        self.assertEqual(item2, {"pio_iid": iid2, "pio_itypes": ("t1",)} )
        self.assertEqual(item3, {"pio_iid": iid3, "pio_itypes": ("t2",), "pio_price": 4.99, "pio_profit": 2.0, "pio_startT": 12345667, "pio_endT": 4567788, "pio_latlng": [1.345, 9.876], "pio_inactive": True } )
        del item4["pio_startT"]
        self.assertEqual(item4, {"pio_iid": iid4, "pio_itypes": ("t2",), "pio_latlng": [1.2345, 10.11], "custom1": "value1"})
        del item5["pio_startT"]
        self.assertEqual(item5, {"pio_iid": iid5, "pio_itypes": ("t1","t2"), "custom1": "i5value1", "custom2": "i5value2"})

        # delete and then try to get it
        client.delete_item(iid2)

        try:
          item2 = client.get_item(iid2)
        except predictionio.ItemNotFoundError as e:
            pass # expected exception
        except:
            raise

        # others still exist
        item3 = client.get_item(iid3)
        self.assertEqual(item3, {"pio_iid": iid3, "pio_itypes": ("t2",), "pio_price": 4.99, "pio_profit": 2.0, "pio_startT": 12345667, "pio_endT": 4567788, "pio_latlng": [1.345, 9.876], "pio_inactive": True } )

        # read, modify, write
        del item3["pio_iid"]
        item3_itypes = item3.pop("pio_itypes")
        item3["pio_price"] = 6.99
        item3["custom1"] = "some value"
        client.create_item(iid3, item3_itypes, item3)
        updated_item3 = client.get_item(iid3)
        self.assertEqual(updated_item3, {"pio_iid": iid3, "pio_itypes": ("t2",), "pio_price": 6.99, "pio_profit": 2.0, "pio_startT": 12345667, "pio_endT": 4567788, "pio_latlng": [1.345, 9.876], "pio_inactive": True, "custom1": "some value" } )

        client.close()

    def test_item(self):
        self._test_item(["i1", "i2", "i3", "i4", "i5"])
        # test special characters in iid
        self._test_item(["i1@abc.com", "i2/f/bar//@@foo", "$$i3%%$~~", "http://www.i4.com", "``i5/apple/"])

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


        # uid and iid with special characters
        client.identify("u1@a.com")
        client.record_action_on_item("view", "i3@bb.com")
        client.record_action_on_item("view", "http://www.yahoo.com")

        client.close()


    def test_pending_requests(self):
        client = predictionio.Client(APP_KEY, 1, API_URL)

        client.identify("u111")
        for i in range(100):
            client.arecord_action_on_item("like", str(i))

        n = 1
        while n > 0:
            n = client.pending_requests()
            time.sleep(0.1)
            #print n

        client.close()

    def test_qsize(self):
        client = predictionio.Client(APP_KEY, 1, API_URL, qsize=10)

        client.identify("u222")
        for i in range(100):
            client.arecord_action_on_item("like", str(i))

        n = 1
        while n > 0:
            n = client.pending_requests()
            time.sleep(0.1)
            #print n

        client.close()



"""
to run individual test:
$ python -m unittest predictionio_test.TestPredictionIO.test_user

to run ALL tests:
% python predictionio_test.py
"""
if __name__ == "__main__" :
    unittest.main()
