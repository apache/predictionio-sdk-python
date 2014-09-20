"""
itemrank quickstart query
"""

import predictionio

client = predictionio.EngineClient("http://localhost:8000")

# Rank item 1 to 5 for each user
item_ids = [str(i) for i in range(1, 6)]
user_ids = [str(x) for x in range(1, 6)] + ["NOT_EXIST_USER"]
for user_id in user_ids:
  print "Rank item 1 to 5 for user", user_id
  try:
    response = client.send_query({
      "uid": user_id,
      "iids": item_ids
    })
    print response
  except predictionio.PredictionIOAPIError as e:
    print 'Caught exception:', e

client.close()
