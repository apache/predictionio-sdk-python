"""PredictoinIO Python SDK

The PredictoinIO Python SDK provides easy-to-use functions for integrating
Python applications with PredictionIO REST API services.
"""

__author__ = "The PredictionIO Team"
__email__ = "help@tappingstone.com"
__copyright__ = "Copyright 2013, TappingStone, Inc."
__license__ = "Apache License, Version 2.0"

__version__ = "0.6.0"


# import packages
import re
import httplib
import json
import urllib

from predictionio.connection import Connection
from predictionio.connection import AsyncRequest
from predictionio.connection import AsyncResponse
from predictionio.connection import PredictionIOAPIError

"""Error exception defined for this API

Should be handled by the user
"""
class ServerStatusError(PredictionIOAPIError):
    "Error happened when tried to get status of the API server"
    pass

class UserNotCreatedError(PredictionIOAPIError):
    "Error happened when tried to create user"
    pass

class UserNotFoundError(PredictionIOAPIError):
    "Error happened when tried to get user"
    pass

class UserNotDeletedError(PredictionIOAPIError):
    "Error happened when tried to delete user"
    pass

class ItemNotCreatedError(PredictionIOAPIError):
    "Error happened when tried to create item"
    pass

class ItemNotFoundError(PredictionIOAPIError):
    "Error happened when tried to get item"
    pass

class ItemNotDeletedError(PredictionIOAPIError):
    "Error happened when tried to delete item"
    pass

class U2IActionNotCreatedError(PredictionIOAPIError):
    "Error happened when tried to create user-to-item action"
    pass

class ItemRecNotFoundError(PredictionIOAPIError):
    "Error happened when tried to get item recommendation"
    pass

class ItemSimNotFoundError(PredictionIOAPIError):
    "Error happened when tried to get similar items"
    pass

class InvalidArgumentError(PredictionIOAPIError):
    "Arguments are not valid"
    pass

# map to API
LIKE_API = "like"
DISLIKE_API = "dislike"
VIEW_API = "view"
CONVERSION_API = "conversion"
RATE_API = "rate"

class Client:
    """PredictionIO client object.

    This is an object representing a PredictionIO's client. This object provides methods for making PredictionIO API requests.

    :param appkey: the App Key provided by PredictionIO.
    :param threads: number of threads to handle PredictionIO API requests. Must be >= 1.
    :param apiurl: the PredictionIO API URL path.
    :param apiversion: the PredictionIO API version. (optional) (eg. "", or "/v1")


    """
    def __init__(self, appkey, threads=1, apiurl="http://localhost:8000", apiversion = ""):
        """Constructor of Client object.

        :param appkey: the appkey
        :param threads: number of threads for handling requests
        :param apiurl: the PredictionIO API URL path.
        :param apiversion: the PredictionIO API version. (optional) (eg. "", or "/v1")

        """
        self.appkey = appkey
        self.threads = threads
        self.apiurl = apiurl
        self.apiversion = apiversion

        # check connection type
        https_pattern = r'^https://(.*)'
        http_pattern = r'^http://(.*)'
        m = re.match(https_pattern, apiurl)
        self.https = True
        if m is None: # not matching https
            m = re.match(http_pattern, apiurl)
            self.https = False
            if m is None: # not matching http either
                raise InvalidArgumentError("apiurl is not valid: %s" % apiurl)
        self.host = m.group(1)

        self._uid = None # identified uid
        self._connection = Connection(host=self.host, threads=self.threads, https=self.https)

    def close(self):
        """Close this client and the connection.

        Call this method when you want to completely terminate the connection with PredictionIO.
        It will wait for all pending requests to finish.
        """
        self._connection.close()

    def identify(self, uid):
        """Identify the uid

        :param uid: user id. type str.
        """
        self._uid = uid

    def get_status(self):
        """Get the status of the PredictionIO API Server

        :returns:
            status message.

        :raises:
            ServerStatusError.
        """
        path = "/"
        request = AsyncRequest("GET", path)
        request.set_rfunc(self._aget_status_resp)
        self._connection.make_request(request)
        result = self.aresp(request)
        return result

    def _aget_status_resp(self, response):
        """Handle the AsyncResponse of get status request"""
        if response.error is not None:
            raise ServerStatusError("Exception happened: %s for request %s" % \
                                    (response.error, response.request))
        elif response.status != httplib.OK:
            raise ServerStatusError("request: %s status: %s body: %s" % \
                                    (response.request, response.status, response.body))

        #data = json.loads(response.body) # convert json string to dict
        return response.body

    def acreate_user(self, uid, params={}):
        """Asynchronously create a user.

        :param uid: user id. type str.
        :param params: optional attributes. type dictionary.
                For example, { 'custom': 'value', 'pio_inactive' : True, 'pio_latlng': [4.5,67.8] }
                
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.

        """
        
        if "pio_latlng" in params:
            params["pio_latlng"] = ",".join(map(str, params["pio_latlng"]))
        if "pio_inactive" in params:
            params["pio_inactive"] = str(params["pio_inactive"]).lower()

        path = "%s/users.json" % self.apiversion
        request = AsyncRequest("POST", path, pio_appkey=self.appkey, pio_uid=uid, **params)
        request.set_rfunc(self._acreate_user_resp)
        self._connection.make_request(request)

        return request

    def _acreate_user_resp(self, response):
        """Private function to handle the AsyncResponse of the acreate_user request.

        :param response: AsyncResponse object.

        :returns:
            None.

        :raises:
            UserNotCreatedError.

        """
        if response.error is not None:
            raise UserNotCreatedError("Exception happened: %s for request %s" % \
                                      (response.error, response.request))
        elif response.status != httplib.CREATED:
            raise UserNotCreatedError("request: %s status: %s body: %s" % \
                                      (response.request, response.status, response.body))

        return None

    def aget_user(self, uid):
        """Asynchronously get user.

        :param uid: user id. type str.

        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        
        enc_uid = urllib.quote(uid,"") # replace special char with %xx
        path = "%s/users/%s.json" % (self.apiversion, enc_uid)
        request = AsyncRequest("GET", path, pio_appkey=self.appkey)
        request.set_rfunc(self._aget_user_resp)
        self._connection.make_request(request)

        return request

    def _aget_user_resp(self, response):
        """Private function to handle the AsyncResponse of the aget_user request .

        :param response: AsyncResponse object.

        :returns:
            User data in Dictionary format.

        :rasies:
            UserNotFoundError.

        """
        if response.error is not None:
            raise UserNotFoundError("Exception happened: %s for request %s" % \
                                    (response.error, response.request))
        elif response.status != httplib.OK:
            raise UserNotFoundError("request: %s status: %s body: %s" % \
                                    (response.request, response.status, response.body))

        data = json.loads(response.body) # convert json string to dict
        return data

    def adelete_user(self, uid):
        """Asynchronously delete user.

        :param uid: user id. type str.

        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        
        enc_uid = urllib.quote(uid,"") # replace special char with %xx
        path = "%s/users/%s.json" % (self.apiversion, enc_uid)
        request = AsyncRequest("DELETE", path, pio_appkey=self.appkey)
        request.set_rfunc(self._adelete_user_resp)
        self._connection.make_request(request)

        return request

    def _adelete_user_resp(self, response):
        """Private function to handle the AsyncResponse of the adelete_user request.

        :param response: AsyncResponse object.

        :returns:
            None.

        :raises:
            UserNotDeletedError.

        """
        if response.error is not None:
            raise UserNotDeletedError("Exception happened: %s for request %s" % \
                                      (response.error, response.request))
        elif response.status != httplib.OK:
            raise UserNotDeletedError("request: %s status: %s body: %s" % \
                                      (response.request, response.status, response.body))
        return None

    def acreate_item(self, iid, itypes, params={}):
        """Asynchronously create item.

        :param iid: item id. type str.
        :param itypes: item types. Tuple of Str.
                For example, if this item belongs to item types "t1", "t2", "t3", "t4",
                then itypes=("t1", "t2", "t3", "t4").
                NOTE: if this item belongs to only one itype, use tuple of one element, eg. itypes=("t1",)
        :param params: optional attributes. type dictionary.
                For example, { 'custom': 'value', 'pio_inactive' : True, 'pio_latlng': [4.5,67.8] }
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        itypes_str = ",".join(itypes) # join items with ","

        if "pio_latlng" in params:
            params["pio_latlng"] = ",".join(map(str, params["pio_latlng"]))
        if "pio_inactive" in params:
            params["pio_inactive"] = str(params["pio_inactive"]).lower()

        path = "%s/items.json" % self.apiversion
        request = AsyncRequest("POST", path, pio_appkey=self.appkey, pio_iid=iid, pio_itypes=itypes_str, **params)
        request.set_rfunc(self._acreate_item_resp)
        self._connection.make_request(request)
        return request

    def _acreate_item_resp(self, response):
        """Private function to handle the AsyncResponse of the acreate_item request

        :param response: AsyncResponse object.

        :returns:
            None
        :raises:
            ItemNotCreatedError

        """
        if response.error is not None:
            raise ItemNotCreatedError("Exception happened: %s for request %s" % \
                                      (response.error, response.request))
        elif response.status != httplib.CREATED:
            raise ItemNotCreatedError("request: %s status: %s body: %s" % \
                                      (response.request, response.status, response.body))
        return None

    def aget_item(self, iid):
        """Asynchronously get item

        :param iid: item id. type str.

        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        enc_iid = urllib.quote(iid, "")
        path = "%s/items/%s.json" % (self.apiversion, enc_iid)
        request = AsyncRequest("GET", path, pio_appkey=self.appkey)
        request.set_rfunc(self._aget_item_resp)
        self._connection.make_request(request)
        return request

    def _aget_item_resp(self, response):
        """Private function to handle the AsyncResponse of the aget_item request

        :param response: AsyncResponse object.

        :returns:
            item data in dictionary format.

        :raises:
            ItemNotFoundError.

        """
        if response.error is not None:
            raise ItemNotFoundError("Exception happened: %s for request %s" % \
                                    (response.error, response.request))
        elif response.status != httplib.OK:
            raise ItemNotFoundError("request: %s status: %s body: %s" % \
                                    (response.request, response.status, response.body))

        data = json.loads(response.body) # convert json string to dict
        if "pio_itypes" in data:
            data["pio_itypes"] = tuple(data["pio_itypes"]) # convert from list to tuple

        return data

    def adelete_item(self, iid):
        """Asynchronously delete item

        :param iid: item id. type str.

        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        
        enc_iid = urllib.quote(iid, "")
        path = "%s/items/%s.json" % (self.apiversion, enc_iid)
        request = AsyncRequest("DELETE", path, pio_appkey=self.appkey)
        request.set_rfunc(self._adelete_item_resp)
        self._connection.make_request(request)
        return request

    def _adelete_item_resp(self, response):
        """Private function to handle the AsyncResponse of the adelete_item request

        :param response: AsyncResponse object

        :returns:
            None

        :raises:
            ItemNotDeletedError
        """
        if response.error is not None:
            raise ItemNotDeletedError("Exception happened: %s for request %s" % \
                                      (response.error, response.request))
        elif response.status != httplib.OK:
            raise ItemNotDeletedError("request: %s status: %s body: %s" % \
                                      (response.request, response.status, response.body))
        return None

    def _aget_user_itemrec_topn(self, engine, uid, n, params={}):
        """Private function to asynchronously get recommendations for user

        :param engine: name of the prediction engine. type str.
        :param uid: user id. type str.
        :param n: number of recommendation. type int.
        :param params: optional parameters. type dictionary
                For example, { 'pio_itypes' : ("t1","t2") }
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        if "pio_itypes" in params:
            params["pio_itypes"] = ",".join(params["pio_itypes"])
        if "pio_latlng" in params:
            params["pio_latlng"] = ",".join(map(str, params["pio_latlng"]))
        if "pio_attributes" in params:
            params["pio_attributes"] = ",".join(params["pio_attributes"])

        enc_uid = urllib.quote(uid,"") # replace special char with %xx
        path = "%s/engines/itemrec/%s/topn.json" % (self.apiversion, engine)
        request = AsyncRequest("GET", path, pio_appkey=self.appkey, pio_uid=enc_uid, pio_n=n, **params)
        request.set_rfunc(self._aget_user_itemrec_topn_resp)
        self._connection.make_request(request)
        return request

    def _aget_user_itemrec_topn_resp(self, response):
        """Private function to handle the AsyncResponse of the aget_itemrec request

        :param response: AsyncResponse object

        :returns:
            data in dictionary format.

        :raises:
            ItemRecNotFoundError.
        """
        if response.error is not None:
            raise ItemRecNotFoundError("Exception happened: %s for request %s" % \
                                               (response.error, response.request))
        elif response.status != httplib.OK:
            raise ItemRecNotFoundError("request: %s status: %s body: %s" % \
                                               (response.request, response.status, response.body))

        data = json.loads(response.body) # convert json string to dict
        return data

    def aget_itemrec_topn(self, engine, n, params={}):
        """Asynchronously get recommendations for the identified user

        :param engine: name of the prediction engine. type str.
        :param n: number of recommendation. type int.
        :param params: optional parameters. type dictionary
                For example, { 'pio_itypes' : ("t1",) }
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """

        if self._uid is None:
            raise InvalidArgumentError("uid is not identified. Please call identify(uid) first.")

        request = self._aget_user_itemrec_topn(engine, self._uid, n, params)
        return request

    def aget_itemrec(self, uid, n, engine, **params):
        """Deprecated. Asynchronously get recommendations

        :param uid: user id. type str.
        :param n: number of recommendation. type int.
        :param engine: name of the prediction engine. type str.
        :param params: keyword arguments for optional attributes.
                For example, pio_latlng="123.4, 56.7"
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        request = self._aget_user_itemrec_topn(engine, uid, n, params)
        return request

    def _aget_itemsim_topn(self, engine, iid, n, params={}):
        """Private function to asynchronously get top n similar items of the item

        :param engine: name of the prediction engine. type str.
        :param iid: item id. type str.
        :param n: number of similar items. type int.
        :param params: optional parameters. type dictionary
                For example, { 'pio_itypes' : ("t1","t2") }
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        if "pio_itypes" in params:
            params["pio_itypes"] = ",".join(params["pio_itypes"])
        if "pio_latlng" in params:
            params["pio_latlng"] = ",".join(map(str, params["pio_latlng"]))
        if "pio_attributes" in params:
            params["pio_attributes"] = ",".join(params["pio_attributes"])

        enc_iid = urllib.quote(iid,"") # replace special char with %xx
        path = "%s/engines/itemsim/%s/topn.json" % (self.apiversion, engine)
        request = AsyncRequest("GET", path, pio_appkey=self.appkey, pio_iid=enc_iid, pio_n=n, **params)
        request.set_rfunc(self._aget_itemsim_topn_resp)
        self._connection.make_request(request)
        return request

    def _aget_itemsim_topn_resp(self, response):
        """Private function to handle the AsyncResponse of the aget_itemsim request

        :param response: AsyncResponse object

        :returns:
            data in dictionary format.

        :raises:
            ItemSimNotFoundError.
        """
        if response.error is not None:
            raise ItemSimNotFoundError("Exception happened: %s for request %s" % \
                                               (response.error, response.request))
        elif response.status != httplib.OK:
            raise ItemSimNotFoundError("request: %s status: %s body: %s" % \
                                               (response.request, response.status, response.body))

        data = json.loads(response.body) # convert json string to dict
        return data

    def aget_itemsim_topn(self, engine, iid, n, params={}):
        """Asynchronously get top n similar items of the item

        :param engine: name of the prediction engine. type str.
        :param iid: item id. type str.
        :param n: number of similar items. type int.
        :param params: optional parameters. type dictionary
                For example, { 'pio_itypes' : ("t1",) }
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """

        request = self._aget_itemsim_topn(engine, iid, n, params)
        return request

    def _auser_action_on_item(self, action, uid, iid, params):
        """Private function to asynchronously create an user action on an item

        :param action: action type. type str. ("like", "dislike", "conversion", "rate", "view")
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param params: optional attributes. type dictionary.
                For example, { 'pio_rate' : 4, 'pio_latlng' : [1.23,4.56] }
                NOTE: For "rate" action, pio_rate attribute is required. integer value of 1-5 (1 is least preferred and 5 is most preferred)

        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        if "pio_latlng" in params:
            params["pio_latlng"] = ",".join(map(str, params["pio_latlng"]))

        path = "%s/actions/u2i.json" % (self.apiversion)
        request = AsyncRequest("POST", path, pio_appkey=self.appkey, pio_action=action, pio_uid=uid, pio_iid=iid, **params)
        request.set_rfunc(self._auser_action_on_item_resp)
        self._connection.make_request(request)
        return request

    def _auser_action_on_item_resp(self, response):
        """Private function to handle the AsyncResponse of the _auser_action_on_item request

        :param response: AsyncResponse object

        :returns:
            None

        :raises:
            U2IActionNotCreatedError
        """
        if response.error is not None:
            raise U2IActionNotCreatedError("Exception happened: %s for request %s" % \
                                           (response.error, response.request))
        elif response.status != httplib.CREATED:
            raise U2IActionNotCreatedError("request: %s status: %s body: %s" % \
                                           (response.request, response.status, response.body))
        return None

    def arecord_action_on_item(self, action, iid, params={}):
        """Asynchronously create action on item

        :param action: action name. type String. For example, "rate", "like", etc
        :param iid: item id. type str or int.
        :param params: optional attributes. type dictionary.
                For example, { 'pio_rate' : 4, 'pio_latlng': [4.5,67.8] }
                NOTE: For "rate" action, pio_rate attribute is required. integer value of 1-5 (1 is least preferred and 5 is most preferred)
        
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.

        :raises:
            U2IActionNotCreatedError
        """

        if self._uid is None:
            raise InvalidArgumentError("uid is not identified. Please call identify(uid) first.")

        request = self._auser_action_on_item(action, self._uid, iid, params)
        return request

    def auser_conversion_item(self, uid, iid, **params):
        """Deprecated. Asynchronously create an user conversion action on an item

        :param uid: user id. type str.
        :param iid: item id. type str.
        :param params: keyword arguments for optional attributes.
                For example, pio_latlng=[123.4, 56.7]
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        request = self._auser_action_on_item(CONVERSION_API, uid, iid, params)
        return request

    def auser_dislike_item(self, uid, iid, **params):
        """Deprecated. Asynchronously create an user dislike action on an item

        :param uid: user id. type str.
        :param iid: item id. type str.
        :param params: keyword arguments for optional attributes.
                For example, pio_latlng=[123.4, 56.7]
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        request = self._auser_action_on_item(DISLIKE_API, uid, iid, params)
        return request

    def auser_like_item(self, uid, iid, **params):
        """Deprecated. Asynchronously create an user like action on an item

        :param uid: user id. type str.
        :param iid: item id. type str.
        :param params: keyword arguments for optional attributes.
                For example, pio_latlng=[123.4, 56.7]
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        request = self._auser_action_on_item(LIKE_API, uid, iid, params)
        return request

    def auser_rate_item(self, uid, iid, rate, **params):
        """Deprecated. Asynchronously create an user rate action on an item

        :param uid: user id. type str.
        :param iid: item id. type str.
        :param rate: rating. integer value of 1-5 (1 is least preferred and 5 is most preferred)
        :param params: keyword arguments for optional attributes.
                For example, pio_latlng=[123.4, 56.7]
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """

        params['pio_rate'] = rate
        request = self._auser_action_on_item(RATE_API, uid, iid, params)
        return request

    def auser_view_item(self, uid, iid, **params):
        """Deprecated. Asynchronously create an user view action on an item

        :param uid: user id. type str.
        :param iid: item id. type str.
        :param params: keyword arguments for optional attributes.
                For example, pio_latlng=[123.4, 56.7]
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        request = self._auser_action_on_item(VIEW_API, uid, iid, params)
        return request

    def aresp(self, request):
        """Get the result of the asynchronous request

        :param request: AsyncRequest object. This object must be returned by the asynchronous request function
                For example, to get the result of a aget_user() request, call this aresp() with the argument of
                AsyncRequest object returned by aget_user().

        :returns:
            The result of this AsyncRequest. The return type is the same as the return type of corresponding blocking request.

            For example,

            Calling aresp() with acreate_user() AsyncRequest returns the same type as create_user(), which is None.

            Calling aresp() with aget_user() AsyncRequest returns the same type as get_user(), which is dictionary data.

        :raises:
            Exception may be raised if there is error happened. The type of exception is the same as exception type
            of the correspdoning blocking request.

            For example,

            Calling aresp() with acreate_user() AsyncRequest may raise UserNotCreatedError exception.

            Calling aresp() with aget_user() AsyncRequest may raise UserNotFoundError exception.

        """
        response = request.get_response()
        result = request.rfunc(response)
        return result

    def create_user(self, uid, params={}):
        """Blocking request to create user

        :param uid: user id. type str.
        :param params: optional attributes. type dictionary.
                For example, { 'custom': 'value', 'pio_inactive' : True, 'pio_latlng': [4.5,67.8] }

        :returns:
            None.

        :raises:
            UserNotCreatedError.

        """
        request = self.acreate_user(uid, params)
        result = self.aresp(request)
        return result

    def get_user(self, uid):
        """Blocking request to get user

        :param uid: user id. type str or int.

        :returns:
            User data in Dictionary format.

        :rasies:
            UserNotFoundError.

        """
        request = self.aget_user(uid)
        result = self.aresp(request)
        return result

    def delete_user(self, uid):
        """Blocking request to delete the user

        :param uid: user id. type str.

        :returns:
            None.

        :raises:
            UserNotDeletedError.

        """
        request = self.adelete_user(uid)
        result = self.aresp(request)
        return result

    def create_item(self, iid, itypes, params={}):
        """Blocking request to create item

        :param iid: item id. type str.
        :param itypes: item types. Tuple of Str.
                For example, if this item belongs to item types "t1", "t2", "t3", "t4",
                then itypes=("t1", "t2", "t3", "t4").
                NOTE: if this item belongs to only one itype, use tuple of one element, eg. itypes=("t1",)
        :param params: optional attributes. type dictionary.
                For example, { 'custom': 'value', 'pio_inactive' : True, 'pio_latlng': [4.5,67.8] }

        :returns:
            None

        :raises:
            ItemNotCreatedError

        """
        request = self.acreate_item(iid, itypes, params)
        result = self.aresp(request)
        return result

    def get_item(self, iid):
        """Blocking request to get item

        :param iid: item id. type str.

        :returns:
            item data in dictionary format.

        :raises:
            ItemNotFoundError.

        """
        request = self.aget_item(iid)
        result = self.aresp(request)
        return result

    def delete_item(self, iid):
        """Blocking request to delete item

        :param iid: item id. type str.

        :returns:
            None

        :raises:
            ItemNotDeletedError

        """
        request = self.adelete_item(iid)
        result = self.aresp(request)
        return result

    def get_itemrec_topn(self, engine, n, params={}):
        """Blocking request to get recommendations for the identified user

        :param engine: name of the prediction engine. type str.
        :param n: number of recommendation. type int.
        :param params: optional parameters. type dictionary
                For example, { 'pio_itypes' : ("t1", "t2") }
        :returns:
            data in dictionary format.

        :raises:
            ItemRecNotFoundError.
        """
        request = self.aget_itemrec_topn(engine, n, params)
        result = self.aresp(request)
        return result

    def get_itemrec(self, uid, n, engine, **params):
        """Deprecated. Blocking request to get recommendations

        :param uid: user id. type str or int.
        :param n: number of recommendation. type int.
        :param engine: name of the prediction engine. type str.
        :param params: keyword arguments for optional attributes.
                For example, pio_latlng=[123.4, 56.7]

        :returns:
            data in dictionary format.

        :raises:
            ItemRecNotFoundError.

        """
        request = self.aget_itemrec(uid, n, engine, **params)
        result = self.aresp(request)
        return result

    def get_itemsim_topn(self, engine, iid, n, params={}):
        """Blocking request to get top n similar items of the item

        :param engine: name of the prediction engine. type str.
        :param iid: item id. type str.
        :param n: number of similar items. type int.
        :param params: optional parameters. type dictionary
                For example, { 'pio_itypes' : ("t1",) }
        :returns:
            data in dictionary format.

        :raises:
            ItemSimNotFoundError.
        """

        request = self.aget_itemsim_topn(engine, iid, n, params)
        result = self.aresp(request)
        return result

    def record_action_on_item(self, action, iid, params={}):
        """Blocking request to create action on an item

        :param action: action name. type String. For example, "rate", "like", etc
        :param iid: item id. type str.
        :param params: optional attributes. type dictionary.
                For example, { 'pio_rate' : 4, 'pio_latlng' : [1.23,4.56] }
                NOTE: For "rate" action, pio_rate attribute is required. integer value of 1-5 (1 is least preferred and 5 is most preferred)

        :returns:
            None

        :raises:
            U2IActionNotCreatedError
        """
        request = self.arecord_action_on_item(action, iid, params)
        result = self.aresp(request)
        return result

    def user_conversion_item(self, uid, iid, **params):
        """Deprecated. Blocking request to create user conversion action on an item

        :param uid: user id. type str.
        :param iid: item id. type str.
        :param params: keyword arguments for optional attributes.
                For example, pio_latlng=[123.4, 56.7]

        :returns:
            None

        :raises:
            U2IActionNotCreatedError
        """
        request = self.auser_conversion_item(uid, iid, **params)
        result = self.aresp(request)
        return result

    def user_dislike_item(self, uid, iid, **params):
        """Deprecated. Blocking request to create user dislike action on an item

        :param uid: user id. type str.
        :param iid: item id. type str.
        :param params: keyword arguments for optional attributes.
                For example, pio_latlng=[123.4, 56.7]

        :returns:
            None

        :raises:
            U2IActionNotCreatedError
        """
        request = self.auser_dislike_item(uid, iid, **params)
        result = self.aresp(request)
        return result

    def user_like_item(self, uid, iid, **params):
        """Deprecated. Blocking request to create user like action on an item

        :param uid: user id. type str.
        :param iid: item id. type str.
        :param params: keyword arguments for optional attributes.
                For example, pio_latlng=[123.4, 56.7]

        :returns:
            None

        :raises:
            U2IActionNotCreatedError
        """
        request = self.auser_like_item(uid, iid, **params)
        result = self.aresp(request)
        return result

    def user_rate_item(self, uid, iid, rate, **params):
        """Deprecated. Blocking request to create user rate action on an item

        :param uid: user id. type str.
        :param iid: item id. type str.
        :param rate: rating. integer value of 1-5 (1 is least preferred and 5 is most preferred)
        :param params: keyword arguments for optional attributes.
                For example, pio_latlng=[123.4, 56.7]

        :returns:
            None

        :raises:
            U2IActionNotCreatedError
        """
        request = self.auser_rate_item(uid, iid, rate, **params)
        result = self.aresp(request)
        return result

    def user_view_item(self, uid, iid, **params):
        """Deprecated. Blocking request to create user view action on an item

        :param uid: user id. type str.
        :param iid: item id. type str.
        :param params: keyword arguments for optional attributes.
                For example, pio_latlng=[123.4, 56.7]

        :returns:
            None

        :raises:
            U2IActionNotCreatedError
        """
        request = self.auser_view_item(uid, iid, **params)
        result = self.aresp(request)
        return result
