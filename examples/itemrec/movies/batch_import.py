
from appdata import AppData
import predictionio
import sys

from app_config import APP_KEY, API_URL

def batch_import_task(app_data, client, all_info=False):

	print "[Info] Importing users to PredictionIO..."
	count = 0 
	for k, v in app_data.get_users().iteritems():
		count += 1
		if all_info:
			print "[Info] Importing %s..." % v
		else:
			if (count % 32 == 0):
				sys.stdout.write('\r[Info] %s' % count)
				sys.stdout.flush()

		client.create_user(v.uid)
	
	sys.stdout.write('\r[Info] %s users were imported.\n' % count)
	sys.stdout.flush()

	print "[Info] Importing items to PredictionIO..."
	count = 0
	for k, v in app_data.get_items().iteritems():
		count += 1
		if all_info:
			print "[Info] Importing %s..." % v
		else:
			if (count % 32 == 0):
				sys.stdout.write('\r[Info] %s' % count)
				sys.stdout.flush()

		client.create_item(v.iid, ("movie",))
	
	sys.stdout.write('\r[Info] %s items were imported.\n' % count)
	sys.stdout.flush()

	print "[Info] Importing rate actions to PredictionIO..."
	count = 0
	for v in app_data.get_rate_actions():
		count += 1
		if all_info:
			print "[Info] Importing %s..." % v
		else:
			if (count % 32 == 0):
				sys.stdout.write('\r[Info] %s' % count)
				sys.stdout.flush()

		client.identify(v.uid)
		client.record_action_on_item("rate", v.iid, { "pio_rate": v.rating, "pio_t": v.t })

	sys.stdout.write('\r[Info] %s rate actions were imported.\n' % count)
	sys.stdout.flush()


if __name__ == '__main__':

	app_data = AppData()
	client = predictionio.Client(APP_KEY, 1, API_URL)
	batch_import_task(app_data, client)
	client.close()

