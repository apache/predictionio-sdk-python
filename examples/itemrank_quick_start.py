"""
itemrank quickstart import data
"""

import random
import sys

import predictionio


def import_itemrank(access_key):
    random.seed()

    client = predictionio.EventClient(access_key)

    print(client.get_status())

    # generate 10 users, with user ids 1,2,....,10
    user_ids = [str(i) for i in range(1, 11)]
    for user_id in user_ids:
        print
        "Set user", user_id
        client.set_user(user_id)

    # generate 50 items, with item ids 1,2,....,50
    # assign type id 1 to all of them
    item_ids = [str(i) for i in range(1, 51)]
    for item_id in item_ids:
        print
        "Set item", item_id
        client.set_item(item_id, {
            "itypes": ['1']
        })

    # each user randomly views 10 items
    for user_id in user_ids:
        for viewed_item in random.sample(item_ids, 10):
            print
            "User", user_id, "views item", viewed_item
            client.record_user_action_on_item("view", user_id, viewed_item)

    client.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage: python -m examples.itemrank_quick_start <access_key>")
    import_itemrank(sys.argv[1])
