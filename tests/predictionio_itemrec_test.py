"""
Test getting itemrec after algo training completes.
"""
import predictionio
import unittest
import time

APP_KEY = "y2Fk4BACEGYeJnqBF4zL9TmrIBdF9va3gyFaLsnM7PVyUNf0G00zC8vCnyBx5hdA" # replace this with your AppKey
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

	def test_get_itemrec_exception_deprecated(self):
		client = predictionio.Client(APP_KEY, 1, API_URL)

		try:
			itemrec = client.get_itemrec("uidwithoutrec", 10, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			pass # expected exception
		except:
			raise

		client.close()

	def test_get_itemrec_exception(self):
		client = predictionio.Client(APP_KEY, 1, API_URL)

		client.identify("uidwithoutrec")

		try:
			itemrec = client.get_itemrec_topn("python-itemrec-engine", 10)
		except predictionio.ItemRecNotFoundError as e:
			pass # expected exception
		except:
			raise

		try:
			itemrec = client.get_itemrec_topn("python-itemrec-engine", 10, { "pio_itypes": ("t1",), "pio_latlng": [1.34, 5.67], "pio_within": 5.0, "pio_unit": "km", "pio_attributes": ["custom1", "custom2"]  })
		except predictionio.ItemRecNotFoundError as e:
			pass # expected exception
		except:
			raise

		client.close()

	def test_get_itemrec_deprecated(self):
		client = predictionio.Client(APP_KEY, 1, API_URL)

		# request more
		try:
			itemrec = client.get_itemrec("u0", 10, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i3", "i1", "i0"]})

		try:
			itemrec = client.get_itemrec("u1", 10, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertTrue( (itemrec == {"pio_iids": ["i2", "i1", "i0", "i3"]}) or 
						 (itemrec == {"pio_iids": ["i2", "i0", "i1", "i3"]}) )

		try:
			itemrec = client.get_itemrec("u2", 10, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertTrue( (itemrec == {"pio_iids": ["i3", "i0", "i1", "i2"]}) or
						 (itemrec == {"pio_iids": ["i3", "i1", "i0", "i2"]}) )

		try:
			itemrec = client.get_itemrec("u3", 6, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertTrue( (itemrec == {"pio_iids": ["i0", "i1", "i2", "i3"]}) or
						 (itemrec == {"pio_iids": ["i0", "i2", "i1", "i3"]}) )

		# request less
		try:
			itemrec = client.get_itemrec("u0", 1, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2"]})

		try:
			itemrec = client.get_itemrec("u0", 2, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i3"]})

		# request with optional attributes

		# pio_itypes
		try:
			itemrec = client.get_itemrec("u0", 10, "python-itemrec-engine", pio_itypes=("t1","t2"))
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i3", "i1", "i0"]})

		# subset itypes
		try:
			itemrec = client.get_itemrec("u0", 10, "python-itemrec-engine", pio_itypes=("t2",))
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i1"]})

		# nonexisting itypes
		try:
			itemrec = client.get_itemrec("u0", 10, "python-itemrec-engine", pio_itypes=("other-itype",))
		except predictionio.ItemRecNotFoundError as e:
			pass # expected no recommendation
		except:
			raise

		# pio_attributes
		try:
			itemrec = client.get_itemrec("u0", 10, "python-itemrec-engine", pio_itypes=("t1",), pio_attributes=["custom1", "custom2"])
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i3", "i1", "i0"], "custom1": [None, None, "i1c1", "i0c1"], "custom2": ["i2c2", None, "i1c2", None]})

		client.close()


	def test_get_itemrec(self):
		client = predictionio.Client(APP_KEY, 1, API_URL)

		# request more
		client.identify("u0")
		try:
			itemrec = client.get_itemrec_topn("python-itemrec-engine", 10)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i3", "i1", "i0"]})

		client.identify("u1")
		try:
			itemrec = client.get_itemrec_topn("python-itemrec-engine", 10)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertTrue( (itemrec == {"pio_iids": ["i2", "i1", "i0", "i3"]}) or 
						 (itemrec == {"pio_iids": ["i2", "i0", "i1", "i3"]}) )

		client.identify("u2")
		try:
			itemrec = client.get_itemrec_topn("python-itemrec-engine", 10)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertTrue( (itemrec == {"pio_iids": ["i3", "i0", "i1", "i2"]}) or
						 (itemrec == {"pio_iids": ["i3", "i1", "i0", "i2"]}) )

		client.identify("u3")
		try:
			itemrec = client.get_itemrec_topn("python-itemrec-engine", 6)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertTrue( (itemrec == {"pio_iids": ["i0", "i1", "i2", "i3"]}) or
						 (itemrec == {"pio_iids": ["i0", "i2", "i1", "i3"]}) )

		# request less
		client.identify("u0")
		try:
			itemrec = client.get_itemrec_topn("python-itemrec-engine", 1)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2"]})

		client.identify("u0")
		try:
			itemrec = client.get_itemrec_topn("python-itemrec-engine", 2)
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i3"]})

		# request with optional attributes

		# pio_itypes
		client.identify("u0")
		try:
			itemrec = client.get_itemrec_topn("python-itemrec-engine", 10, {"pio_itypes": ("t1","t2")})
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i3", "i1", "i0"]})

		# subset itypes
		client.identify("u0")
		try:
			itemrec = client.get_itemrec_topn("python-itemrec-engine", 10, {"pio_itypes": ("t2",)})
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i1"]})

		# nonexisting itypes
		client.identify("u0")
		try:
			itemrec = client.get_itemrec_topn("python-itemrec-engine", 10, {"pio_itypes": ("other-itype",)})
		except predictionio.ItemRecNotFoundError as e:
			pass # expected no recommendation
		except:
			raise

		# pio_attributes
		client.identify("u0")
		try:
			itemrec = client.get_itemrec_topn("python-itemrec-engine", 10, {"pio_itypes": ("t1",), "pio_attributes": ["custom1", "custom2"]})
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i3", "i1", "i0"], "custom1": [None, None, "i1c1", "i0c1"], "custom2": ["i2c2", None, "i1c2", None]})

		# TODO pio_latlng
		# TODO pio_within
		# TODO pio_unit

		client.close()

if __name__ == "__main__" :
	unittest.main()
