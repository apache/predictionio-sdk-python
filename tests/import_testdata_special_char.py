"""
Import simple test data (id with special characters) for testing getting itemrec
"""
import predictionio

APP_KEY = "GToKwk78As0LBp2fAx2YNUBPZFZvtwy6MJkGwRASiD6Q77JjBnTaXBxzBTd52ICE"
API_URL = "http://localhost:8000"

MIN_VERSION = '0.5.0'
if predictionio.__version__ < MIN_VERSION:
    err = "Require PredictionIO Python SDK version >= %s" % MIN_VERSION
    raise Exception(err)

if __name__ == "__main__":
	client = predictionio.Client(APP_KEY, 1, API_URL)

	client.create_user("u0@u.n")
	client.create_user("u1@u.n")
	client.create_user("http://u2.com")
	client.create_user("u3@u.n")

	client.create_item("http://i0.com", ("t1",), {"custom1": "i0c1"})
	client.create_item("i1@i1", ("t1","t2"), {"custom1": "i1c1", "custom2": "i1c2"})
	client.create_item("i2.org", ("t1","t2"), {"custom2": "i2c2"})
	client.create_item("i3", ("t1",))

	client.identify("u0@u.n")
	client.record_action_on_item("rate", "http://i0.com", { "pio_rate": 2 })
	client.record_action_on_item("rate", "i1@i1", { "pio_rate": 3 })
	client.record_action_on_item("rate", "i2.org", { "pio_rate": 4 })
	
	client.identify("u1@u.n")
	client.record_action_on_item("rate", "i2.org", { "pio_rate": 4 })
	client.record_action_on_item("rate", "i3", { "pio_rate": 1 })

	client.identify("http://u2.com")
	client.record_action_on_item("rate", "i1@i1", { "pio_rate": 2 })
	client.record_action_on_item("rate", "i2.org", { "pio_rate": 1 })
	client.record_action_on_item("rate", "i3", { "pio_rate": 3 })

	client.identify("u3@u.n")
	client.record_action_on_item("rate", "http://i0.com", { "pio_rate": 5 })
	client.record_action_on_item("rate", "i1@i1", { "pio_rate": 3 })
	client.record_action_on_item("rate", "i3", { "pio_rate": 2 })

	client.close()
	

	



