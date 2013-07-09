"""
Test getting itemrec after algo training completes.
"""
import predictionio
import unittest
import threading
import time

import httplib
import urllib

APP_KEY = "zHCx9Xv9sZ9Q21LMINKcrgZNgGJ3oReZA9Zvf0MsyJYDv6FwgHEeEI0XTEY5aEsu" # replace this with your AppKey
API_URL = "http://localhost:8000" # PredictoinIO Server

DEBUG = True

class TestPredictionIO(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_get_itemrec_deprecated(self):
		#TODO
		pass

	def test_get_itemrec(self):
		client = predictionio.Client(APP_KEY, 1, API_URL)

		# request more
		client.identify("u0")
		try:
			itemrec = client.get_itemrec_topn(10, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i3", "i1", "i0"]})

		client.identify("u1")
		try:
			itemrec = client.get_itemrec_topn(10, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i1", "i0", "i3"]})

		client.identify("u2")
		try:
			itemrec = client.get_itemrec_topn(10, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i3", "i0", "i1", "i2"]})

		client.identify("u3")
		try:
			itemrec = client.get_itemrec_topn(6, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i0", "i1", "i2", "i3"]})

		# request less
		client.identify("u0")
		try:
			itemrec = client.get_itemrec_topn(1, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2"]})

		client.identify("u0")
		try:
			itemrec = client.get_itemrec_topn(2, "python-itemrec-engine")
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i2", "i3"]})

		# request with optional attributes

		# pio_itypes
		client.identify("u2")
		try:
			itemrec = client.get_itemrec_topn(10, "python-itemrec-engine", {"pio_itypes": ("t1","t2")})
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i3", "i0", "i1", "i2"]})

		# subset itypes
		client.identify("u2")
		try:
			itemrec = client.get_itemrec_topn(10, "python-itemrec-engine", {"pio_itypes": ("t2",)})
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i1", "i2"]})

		# nonexisting itypes
		client.identify("u2")
		try:
			itemrec = client.get_itemrec_topn(10, "python-itemrec-engine", {"pio_itypes": ("other-itype",)})
		except predictionio.ItemRecNotFoundError as e:
			pass # expected no recommendation
		except:
			raise

		# pio_attributes
		client.identify("u2")
		try:
			itemrec = client.get_itemrec_topn(10, "python-itemrec-engine", {"pio_itypes": ("t1",), "pio_attributes": ["custom1", "custom2"]})
		except predictionio.ItemRecNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemrec
		self.assertEqual(itemrec, {"pio_iids": ["i3", "i0", "i1", "i2"], "custom1": [None, "i0c1", "i1c1", None], "custom2": [None, None, "i1c2", "i2c2"]})

		# TODO pio_latlng
		# TODO pio_within
		# TODO pio_unit

		client.close()

if __name__ == "__main__" :
	unittest.main()
