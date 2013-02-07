
import predictionio
import unittest
import threading
import time

import httplib
import urllib


APP_KEY = "eAtwmhBIq4LzCPPlmsTSsgSnkW8IN3O1OXL9bwqFzLTCXtzgbsIhciFtbCpFPP2m" # replace this with your AppKey
API_URL = "http://localhost:8000" # PredictoinIO Server

class TestPredictionIO(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_status(self):
        client = predictionio.Client(APP_KEY, 1, apiurl=API_URL)
        status = client.get_status()
        self.assertEqual(status, "PredictionIO Output API is online.")
        client.close()
        
    def test_user(self):
        client = predictionio.Client(APP_KEY, 1, apiurl=API_URL)
        
        client.create_user(uid="u1", gender="m", latlng="1.2,33.3", bday="1979-01-24")
        client.create_user(uid="u2")
        
        user1 = client.get_user(uid="u1")
        user2 = client.get_user(uid="u2")
        
        self.assertEqual(user1["uid"], "u1")
        self.assertEqual(user1["gender"], "m")
        self.assertEqual(user1["latlng"], [1.2,33.3])
        self.assertEqual(user1["bday"], "1979-01-24")
        
        self.assertEqual(user2["uid"], "u2")
        
        client.delete_user(uid="u1")
        
        try:
            user = client.get_user(uid="u1")
        except predictionio.UserNotFoundError as e:
            pass # expected exception
        except:
            raise
        
        user2 = client.get_user(uid="u2")
        self.assertEqual(user2["uid"], "u2")
        
        client.close()
        
    def test_item(self):
        client = predictionio.Client(APP_KEY, 1, apiurl=API_URL)
        
        client.create_item(iid="i1", itypes=("t1","t2","t3"))
        client.create_item(iid="i2", itypes=("t1",))
        
        item1 = client.get_item(iid="i1")
        item2 = client.get_item(iid="i2")
        
        self.assertEqual(item1["iid"], "i1")
        self.assertEqual(item1["itypes"], "t1,t2,t3")
        
        self.assertEqual(item2["iid"], "i2")
        self.assertEqual(item2["itypes"], "t1")
        
        client.delete_item(iid="i2")
        
        item1 = client.get_item(iid="i1")
        self.assertEqual(item1["iid"], "i1")
        self.assertEqual(item1["itypes"], "t1,t2,t3")
        
        try:
          item2 = client.get_item(iid="i2")
        except predictionio.ItemNotFoundError as e:
            pass # expected exception
        except:
            raise
        
        client.close()
    
    def test_u2iAction(self):
        client = predictionio.Client(APP_KEY, 1, apiurl=API_URL)
        
        client.user_like_item(uid="u1", iid="i1")
        client.user_dislike_item(uid="u2", iid="i2")
        client.user_view_item(uid="u3", iid="i3")
        client.user_rate_item(uid="u4", iid="i4", rate=4)
        client.user_conversion_item(uid="u5", iid="i5")
        
        client.close()
            
    def test_get_itemrec(self):
        client = predictionio.Client(APP_KEY, 1, apiurl=API_URL)
        
        try:
            itemrec = client.get_itemrec(uid="u1", n=10, engine="test-python")
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
    