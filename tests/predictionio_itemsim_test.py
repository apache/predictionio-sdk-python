"""
Test getting itemsim after algo training completes (pdio-itemsimcf with cosine sim).
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

	def test_get_itemsim_exception(self):
		client = predictionio.Client(APP_KEY, 1, API_URL)

		try:
			itemsim = client.get_itemsim_topn("python-itemsim-engine", "iidwithoutsim", 10)
		except predictionio.ItemSimNotFoundError as e:
			pass # expected exception
		except:
			raise

		try:
			itemsim = client.get_itemsim_topn("python-itemsim-engine", "iidwithoutsim", 10, { "pio_itypes": ("t1",), "pio_latlng": [1.34, 5.67], "pio_within": 5.0, "pio_unit": "km", "pio_attributes": ["custom1", "custom2"]  })
		except predictionio.ItemSimNotFoundError as e:
			pass # expected exception
		except:
			raise

		client.close()

	def test_get_itemsim(self):
		client = predictionio.Client(APP_KEY, 1, API_URL)

		# request more than what is available
		try:
			itemsim = client.get_itemsim_topn("python-itemsim-engine", "i0", 10)
		except predictionio.ItemSimNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemsim
		self.assertTrue( (itemsim == {"pio_iids": ["i1", "i2", "i3"]}) or
						 (itemsim == {"pio_iids": ["i1", "i3", "i2"]}) )

		try:
			itemsim = client.get_itemsim_topn("python-itemsim-engine", "i1", 10)
		except predictionio.ItemSimNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemsim
		self.assertTrue( (itemsim == {"pio_iids": ["i2", "i3", "i0"]}) )

		try:
			itemsim = client.get_itemsim_topn("python-itemsim-engine", "i2", 10)
		except predictionio.ItemSimNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemsim
		self.assertTrue( (itemsim == {"pio_iids": ["i1", "i3", "i0"]}) )

		try:
			itemsim = client.get_itemsim_topn("python-itemsim-engine", "i3", 10)
		except predictionio.ItemSimNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemsim
		self.assertTrue( (itemsim == {"pio_iids": ["i1", "i2", "i0"]}) )

		# request less
		try:
			itemsim = client.get_itemsim_topn("python-itemsim-engine", "i1", 1)
		except predictionio.ItemSimNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemsim
		self.assertEqual(itemsim, {"pio_iids": ["i2"]})

		try:
			itemsim = client.get_itemsim_topn("python-itemsim-engine", "i1", 2)
		except predictionio.ItemSimNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemsim
		self.assertEqual(itemsim, {"pio_iids": ["i2", "i3"]})

		# request with optional attributes

		# pio_itypes
		try:
			itemsim = client.get_itemsim_topn("python-itemsim-engine", "i1", 10, {"pio_itypes": ("t1","t2")})
		except predictionio.ItemSimNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemsim
		self.assertEqual(itemsim, {"pio_iids": ["i2", "i3", "i0"]})

		# subset itypes
		try:
			itemsim = client.get_itemsim_topn("python-itemsim-engine", "i1", 10, {"pio_itypes": ("t2",)})
		except predictionio.ItemSimNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemsim
		self.assertEqual(itemsim, {"pio_iids": ["i2"]})

		# nonexisting itypes
		try:
			itemsim = client.get_itemsim_topn("python-itemsim-engine", "i0", 10, {"pio_itypes": ("other-itype",)})
		except predictionio.ItemSimNotFoundError as e:
			pass # expected no recommendation
		except:
			raise

		# pio_attributes
		try:
			itemsim = client.get_itemsim_topn("python-itemsim-engine", "i1", 10, {"pio_itypes": ("t1",), "pio_attributes": ["custom1", "custom2"]})
		except predictionio.ItemSimNotFoundError as e:
			print "ERROR: have you run import_testdata.py and then wait for the algorithm training completion?"
			raise
		except:
			raise
		if DEBUG: print itemsim
		self.assertEqual(itemsim, {"pio_iids": ["i2", "i3", "i0"], "custom1": [None, None, "i0c1"], "custom2": ["i2c2", None, None]})

		# TODO pio_latlng
		# TODO pio_within
		# TODO pio_unit

		client.close()

if __name__ == "__main__" :
	unittest.main()
