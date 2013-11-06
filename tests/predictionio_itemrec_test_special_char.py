"""
Test getting itemrec after algo training completes.
"""
import predictionio
import unittest
import time

APP_KEY = "GToKwk78As0LBp2fAx2YNUBPZFZvtwy6MJkGwRASiD6Q77JjBnTaXBxzBTd52ICE" # replace this with your AppKey
API_URL = "http://localhost:8000" # PredictoinIO Server

DEBUG = True

MIN_VERSION = '0.6.0'
if predictionio.__version__ < MIN_VERSION:
	err = "Require PredictionIO Python SDK version >= %s" % MIN_VERSION
	raise Exception(err)

class TestPredictionIO(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_get_itemrec_deprecated(self):
		client = predictionio.Client(APP_KEY, 1, API_URL)

		uid0 = "u0@u.n"
		uid1 = "u1@u.n"
		uid2 = "http://u2.com"
		uid3 = "u3@u.n"

		iid0 = "http://i0.com"
		iid1 = "i1@i1"
		iid2 = "i2.org"
		iid3 = "i3"

		engine_name = "itemrec"

		# request more
		try:
			itemrec = client.get_itemrec(uid0, 10, engine_name)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": [iid2, iid3, iid1, iid0]})

		try:
			itemrec = client.get_itemrec(uid1, 10, engine_name)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertTrue( (itemrec == {"pio_iids": [iid2, iid1, iid0, iid3]}) or 
						 (itemrec == {"pio_iids": [iid2, iid0, iid1, iid3]}) )

		try:
			itemrec = client.get_itemrec(uid2, 10, engine_name)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertTrue( (itemrec == {"pio_iids": [iid3, iid0, iid1, iid2]}) or
						 (itemrec == {"pio_iids": [iid3, iid1, iid0, iid2]}) )

		try:
			itemrec = client.get_itemrec(uid3, 6, engine_name)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertTrue( (itemrec == {"pio_iids": [iid0, iid1, iid2, iid3]}) or
						 (itemrec == {"pio_iids": [iid0, iid2, iid1, iid3]}) )

		# request less
		try:
			itemrec = client.get_itemrec(uid0, 1, engine_name)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": [iid2]})

		try:
			itemrec = client.get_itemrec(uid0, 2, engine_name)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": [iid2, iid3]})

		# request with optional attributes

		# pio_itypes
		try:
			itemrec = client.get_itemrec(uid0, 10, engine_name, pio_itypes=("t1","t2"))
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": [iid2, iid3, iid1, iid0]})

		# subset itypes
		try:
			itemrec = client.get_itemrec(uid0, 10, engine_name, pio_itypes=("t2",))
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": [iid2, iid1]})

		# nonexisting itypes
		try:
			itemrec = client.get_itemrec(uid0, 10, engine_name, pio_itypes=("other-itype",))
		except predictionio.ItemRecNotFoundError as e:
			pass # expected no recommendation
		except:
			raise

		# pio_attributes
		try:
			itemrec = client.get_itemrec(uid0, 10, engine_name, pio_itypes=("t1",), pio_attributes=["custom1", "custom2"])
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": [iid2, iid3, iid1, iid0], "custom1": [None, None, "i1c1", "i0c1"], "custom2": ["i2c2", None, "i1c2", None]})

		client.close()


	def test_get_itemrec(self):
		client = predictionio.Client(APP_KEY, 1, API_URL)

		uid0 = "u0@u.n"
		uid1 = "u1@u.n"
		uid2 = "http://u2.com"
		uid3 = "u3@u.n"

		iid0 = "http://i0.com"
		iid1 = "i1@i1"
		iid2 = "i2.org"
		iid3 = "i3"

		engine_name = "itemrec"
		
		# request more
		client.identify(uid0)
		try:
			itemrec = client.get_itemrec_topn(engine_name, 10)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": [iid2, iid3, iid1, iid0]})

		client.identify(uid1)
		try:
			itemrec = client.get_itemrec_topn(engine_name, 10)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertTrue( (itemrec == {"pio_iids": [iid2, iid1, iid0, iid3]}) or 
						 (itemrec == {"pio_iids": [iid2, iid0, iid1, iid3]}) )

		client.identify(uid2)
		try:
			itemrec = client.get_itemrec_topn(engine_name, 10)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertTrue( (itemrec == {"pio_iids": [iid3, iid0, iid1, iid2]}) or
						 (itemrec == {"pio_iids": [iid3, iid1, iid0, iid2]}) )

		client.identify(uid3)
		try:
			itemrec = client.get_itemrec_topn(engine_name, 6)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertTrue( (itemrec == {"pio_iids": [iid0, iid1, iid2, iid3]}) or
						 (itemrec == {"pio_iids": [iid0, iid2, iid1, iid3]}) )

		# request less
		client.identify(uid0)
		try:
			itemrec = client.get_itemrec_topn(engine_name, 1)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": [iid2]})

		client.identify(uid0)
		try:
			itemrec = client.get_itemrec_topn(engine_name, 2)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": [iid2, iid3]})

		# request with optional attributes

		# pio_itypes
		client.identify(uid0)
		try:
			itemrec = client.get_itemrec_topn(engine_name, 10, {"pio_itypes": ("t1","t2")})
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": [iid2, iid3, iid1, iid0]})

		# subset itypes
		client.identify(uid0)
		try:
			itemrec = client.get_itemrec_topn(engine_name, 10, {"pio_itypes": ("t2",)})
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": [iid2, iid1]})

		# nonexisting itypes
		client.identify(uid0)
		try:
			itemrec = client.get_itemrec_topn(engine_name, 10, {"pio_itypes": ("other-itype",)})
		except predictionio.ItemRecNotFoundError as e:
			pass # expected no recommendation
		except:
			raise

		# pio_attributes
		client.identify(uid0)
		try:
			itemrec = client.get_itemrec_topn(engine_name, 10, {"pio_itypes": ("t1",), "pio_attributes": ["custom1", "custom2"]})
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": [iid2, iid3, iid1, iid0], "custom1": [None, None, "i1c1", "i0c1"], "custom2": ["i2c2", None, "i1c2", None]})

		# TODO pio_latlng
		# TODO pio_within
		# TODO pio_unit

		client.close()

if __name__ == "__main__" :
	unittest.main()
