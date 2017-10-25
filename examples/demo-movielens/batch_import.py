import sys
import datetime

import pytz

from appdata import AppData
import predictionio


def batch_import_task(app_data, client, all_info=False):
    # event_time is an important properties used by the PredictionIO platform. It
    # is particularly useful in generating training and testing set, which uses
    # event_time for splitting. Hence, when we import data, better to make the
    # event_time as approximate to fact as possible.
    #
    # However, in many cases, the data doesn't come with a time. Movie-lens' user
    # data, for example, only reveals the age, gender, occupation, and zip code of
    # a user. It doesn't report when the user is "created". Likewise, for items,
    # it only reports the release date.
    #
    # To remedy this problem, we have to make some assumptions to the data. In
    # this import script, the event_time for user is set to epoch=0, and the
    # event_time for item is set to the release_date + 00:00:00 UTC.

    print("[Info] Importing users to PredictionIO...")
    user_create_time = datetime.datetime.fromtimestamp(0, tz=pytz.utc)
    count = 0
    set_user_request_list = []
    for k, v in app_data.get_users().iteritems():
        count += 1
        if all_info:
            print("[Info] Importing %s..." % v)
        else:
            if count % 32 == 0:
                sys.stdout.write('\r[Info] %s' % count)
                sys.stdout.flush()

        set_user_request_list.append(
            client.aset_user(uid=v.uid, event_time=user_create_time))

    [r.get_response() for r in set_user_request_list]
    sys.stdout.write('\r[Info] %s users were imported.\n' % count)
    sys.stdout.flush()

    print("[Info] Importing items to PredictionIO...")
    count = 0
    set_item_request_list = []
    # event_time is a datetime, hence need to add a time component to the release
    # date.
    midnight_utc = datetime.time(0, 0, 0, tzinfo=pytz.utc)
    epoch = datetime.datetime.fromtimestamp(0, tz=pytz.utc)
    for k, v in app_data.get_items().iteritems():
        count += 1
        if all_info:
            print("[Info] Importing %s..." % v)
        else:
            if count % 32 == 0:
                sys.stdout.write('\r[Info] %s' % count)
                sys.stdout.flush()

        itypes = ("movie",) + v.genres

        release_datetime = datetime.datetime.combine(
            v.release_date,
            midnight_utc)

        # event_time must be after epoch.
        event_time = release_datetime if release_datetime > epoch else epoch

        utf8_name = v.name.decode('utf-8', 'ignore')

        set_item_request = client.aset_item(
            iid=v.iid,
            event_time=event_time,
            properties={
                "itypes": list(itypes),
                "starttime": release_datetime.isoformat(),
                "name": utf8_name,
                "year": v.year})

        set_item_request_list.append(set_item_request)

    [r.get_response() for r in set_item_request_list]
    sys.stdout.write('\r[Info] %s items were imported.\n' % count)
    sys.stdout.flush()

    print("[Info] Importing rate actions to PredictionIO...")
    count = 0
    create_event_request_list = []
    for v in app_data.get_rate_actions():
        count += 1
        if all_info:
            print("[Info] Importing %s..." % v)
        else:
            if count % 32 == 0:
                sys.stdout.write('\r[Info] %s' % count)
                sys.stdout.flush()

        properties = {"rating": int(v.rating)}
        req = client.acreate_event(
            event="rate",
            entity_type="user",
            entity_id=v.uid,
            target_entity_type="item",
            target_entity_id=v.iid,
            properties=properties,
            event_time=v.t.replace(tzinfo=pytz.utc),
        )

        create_event_request_list.append(req)

    [r.get_response() for r in create_event_request_list]
    sys.stdout.write('\r[Info] %s rate actions were imported.\n' % count)
    sys.stdout.flush()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit("Usage: python -m examples.demo-movielens.batch_import "
                 "<access_key> <url>")

    access_key = sys.argv[1]

    client = predictionio.EventClient(
        access_key=access_key,
        url=sys.argv[2],
        threads=5,
        qsize=500)

    # Test connection
    print("Status:", client.get_status())

    app_data = AppData()
    batch_import_task(app_data, client)
    client.close()
